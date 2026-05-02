// Generic chat shell. Renders core entry kinds itself; experiments inject a
// `renderExtra` callback for any additional kinds (e.g. pair/'s `options`).
//
// Layout: <Static> for committed past entries (Ink writes them once, never
// re-renders, so layout can't corrupt while streaming), live region below
// for the currently-streaming assistant block / running tool pill, input
// row pinned at the bottom with thin grey rule lines above and below.

import React, { useCallback, useEffect, useRef, useState, type ReactNode } from 'react';
import { Box, Static, Text } from 'ink';
import { Spinner } from '@inkjs/ui';
import { ChatInput } from './components/Input.js';
import { type Session } from './Session.js';
import { type CoreAgentEvent } from './types.js';
import {
  AssistantBlock,
  ErrorLine,
  StepFooter,
  ToolPillRunning,
  ToolResult,
  UserLine,
} from './components/Entries.js';


// "Committed" entries — already past, won't change. Subset of AgentEvent
// kinds plus the entry envelope.
type CoreFrozenEntry =
  | { kind: 'user'; text: string }
  | { kind: 'assistant'; text: string }
  | {
      kind: 'tool';
      name: string;
      input: unknown;
      result: { text: string; isError: boolean } | null;
    }
  | { kind: 'footer'; elapsedSec: number }
  | { kind: 'error'; message: string };

// "Live" entries — currently streaming.
type CoreLiveEntry =
  | { kind: 'assistant'; text: string }
  | { kind: 'tool'; id: string; name: string; input: unknown }
  | null;

/**
 * Optional extension point for experiments: when the session emits an event
 * with a kind core doesn't handle, the App passes it to `renderExtraEvent`,
 * which can:
 *   - Return an `ExtraEntry` to freeze in the transcript.
 *   - Return `null` to ignore the event.
 *   - Return a `{ render: ReactNode }` directly to render once-only (rare).
 *
 * The extra entries are then rendered via `renderExtra(entry)`.
 */
export type ExtraExtension<E, X> = {
  reduce: (event: E) => X | null;
  render: (entry: X, index: number) => ReactNode;
};


const LOADING_WORDS = [
  'Thinking', 'Pondering', 'Cogitating', 'Musing', 'Ruminating',
  'Brewing', 'Brainstorming', 'Mulling', 'Deliberating', 'Reflecting',
  'Considering', 'Distilling', 'Crystallizing', 'Reasoning', 'Plotting',
  'Galloping', 'Simmering', 'Percolating', 'Noodling',
];

function pickLoadingWord(): string {
  return LOADING_WORDS[Math.floor(Math.random() * LOADING_WORDS.length)]!;
}


export function App<E = never, X = never>({
  session,
  extra,
}: {
  session: Session<E>;
  extra?: ExtraExtension<E, X>;
}) {
  const [frozen, setFrozen] = useState<Array<CoreFrozenEntry | { kind: '__extra__'; entry: X }>>([]);
  const [live, setLive] = useState<CoreLiveEntry>(null);
  const [busy, setBusy] = useState(false);
  const [loadingWord, setLoadingWord] = useState(() => pickLoadingWord());
  const [inputKey, setInputKey] = useState(0);
  const [history, setHistory] = useState<string[]>([]);
  const turnStartRef = useRef<number>(0);
  // Mirror of `live` we can read SYNCHRONOUSLY inside event handlers. React
  // would otherwise queue setLive callbacks behind direct setFrozen calls,
  // producing wrong-order commits (we hit a real bug where the step footer
  // was queued before the assistant text it should follow). All `freeze`
  // calls now run in raw call order; `setLive` and `liveRef.current` are
  // kept in lockstep via a wrapper.
  const liveRef = useRef<CoreLiveEntry>(null);

  const updateLive = useCallback((next: CoreLiveEntry) => {
    liveRef.current = next;
    setLive(next);
  }, []);

  const freeze = useCallback(
    (entry: CoreFrozenEntry | { kind: '__extra__'; entry: X }) => {
      setFrozen((prev) => [...prev, entry]);
    },
    [],
  );

  const handleEvent = useCallback(
    (ev: CoreAgentEvent | E) => {
      const e = ev as { kind: string };
      if (e.kind === 'text_delta') {
        const t = (ev as { text: string }).text;
        const cur = liveRef.current;
        if (cur && cur.kind === 'assistant') {
          updateLive({ ...cur, text: cur.text + t });
        } else {
          updateLive({ kind: 'assistant', text: t });
        }
        return;
      }
      if (e.kind === 'text_block_done') {
        const cur = liveRef.current;
        if (cur && cur.kind === 'assistant') {
          updateLive(null);
          freeze({ kind: 'assistant', text: cur.text });
        }
        return;
      }
      if (e.kind === 'tool_use_start') {
        const t = ev as { id: string; name: string; input: unknown };
        const cur = liveRef.current;
        if (cur && cur.kind === 'assistant') {
          freeze({ kind: 'assistant', text: cur.text });
        }
        updateLive({ kind: 'tool', id: t.id, name: t.name, input: t.input });
        return;
      }
      if (e.kind === 'tool_use_done') {
        const t = ev as { id: string; input: unknown };
        const cur = liveRef.current;
        if (cur && cur.kind === 'tool' && cur.id === t.id) {
          updateLive({ ...cur, input: t.input });
        }
        return;
      }
      if (e.kind === 'tool_result') {
        const t = ev as { toolUseId: string; name: string; text: string; isError: boolean };
        const cur = liveRef.current;
        if (cur && cur.kind === 'tool' && cur.id === t.toolUseId) {
          updateLive(null);
          freeze({
            kind: 'tool',
            name: cur.name,
            input: cur.input,
            result: { text: t.text, isError: t.isError },
          });
        } else {
          freeze({
            kind: 'tool',
            name: t.name,
            input: {},
            result: { text: t.text, isError: t.isError },
          });
        }
        return;
      }
      if (e.kind === 'result') {
        const cur = liveRef.current;
        if (cur && cur.kind === 'assistant') {
          updateLive(null);
          freeze({ kind: 'assistant', text: cur.text });
        }
        const elapsed = (Date.now() - turnStartRef.current) / 1000;
        freeze({ kind: 'footer', elapsedSec: elapsed });
        setBusy(false);
        return;
      }
      if (e.kind === 'error') {
        const t = ev as { message: string };
        freeze({ kind: 'error', message: t.message });
        setBusy(false);
        return;
      }
      // Unknown kind — try the experiment extension.
      if (extra) {
        const x = extra.reduce(ev as E);
        if (x !== null && x !== undefined) {
          const cur = liveRef.current;
          if (cur && cur.kind === 'assistant') {
            updateLive(null);
            freeze({ kind: 'assistant', text: cur.text });
          }
          freeze({ kind: '__extra__', entry: x });
        }
      }
    },
    [extra, freeze, updateLive],
  );

  // Wire session.
  useEffect(() => {
    session.onEvent(handleEvent);
    session.start();
    return () => session.close();
  }, [session, handleEvent]);

  // Rotate loader word every ~2.2s while busy.
  useEffect(() => {
    if (!busy) return;
    const t = setInterval(() => setLoadingWord(pickLoadingWord()), 2200);
    return () => clearInterval(t);
  }, [busy]);

  const onSubmit = useCallback(
    (text: string) => {
      const trimmed = text.trim();
      if (!trimmed || busy) return;
      setInputKey((k) => k + 1);
      setBusy(true);
      setLoadingWord(pickLoadingWord());
      setHistory((h) => (h[h.length - 1] === trimmed ? h : [...h, trimmed]));
      freeze({ kind: 'user', text: trimmed });
      turnStartRef.current = Date.now();
      session.send(trimmed);
    },
    [busy, freeze, session],
  );

  // Show the spinner whenever the model is doing something but there's
  // nothing visible streaming yet — i.e. before the first event of a turn
  // AND in the gaps between tool_result and the next assistant block (the
  // model is "thinking up" a follow-up).
  const showLoader = busy && live === null;

  return (
    <>
      <Static items={frozen.map((entry, i) => ({ entry, i }))}>
        {({ entry, i }) => {
          if (entry.kind === '__extra__') {
            if (extra) return <React.Fragment key={i}>{extra.render(entry.entry, i)}</React.Fragment>;
            return null;
          }
          if (entry.kind === 'user') return <UserLine key={i} text={entry.text} />;
          if (entry.kind === 'assistant') return <AssistantBlock key={i} text={entry.text} />;
          if (entry.kind === 'tool') {
            if (entry.result) {
              return (
                <ToolResult
                  key={i}
                  name={entry.name}
                  input={entry.input}
                  text={entry.result.text}
                  isError={entry.result.isError}
                />
              );
            }
            return <ToolPillRunning key={i} name={entry.name} input={entry.input} />;
          }
          if (entry.kind === 'footer') return <StepFooter key={i} elapsedSec={entry.elapsedSec} />;
          if (entry.kind === 'error') return <ErrorLine key={i} message={entry.message} />;
          return null;
        }}
      </Static>

      {live && live.kind === 'assistant' ? <AssistantBlock text={live.text} /> : null}
      {live && live.kind === 'tool' ? <ToolPillRunning name={live.name} input={live.input} /> : null}

      {showLoader ? (
        <Box marginTop={1}>
          <Box marginRight={1}>
            <Spinner />
          </Box>
          <Text color="#ff875f">{loadingWord}…</Text>
        </Box>
      ) : null}

      <Box
        marginTop={1}
        flexDirection="column"
        borderStyle="single"
        borderLeft={false}
        borderRight={false}
        borderColor="#808080"
      >
        <ChatInput key={inputKey} isDisabled={busy} onSubmit={onSubmit} history={history} />
      </Box>
    </>
  );
}
