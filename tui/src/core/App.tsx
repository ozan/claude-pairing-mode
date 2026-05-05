// Generic chat shell. Renders core entry kinds itself; experiments inject a
// `renderExtra` callback for any additional kinds (e.g. pair/'s `options`).
//
// Layout: <Static> for committed past entries (Ink writes them once, never
// re-renders, so layout can't corrupt while streaming), live region below
// for the currently-streaming assistant block / running tool pill, input
// row pinned at the bottom with thin grey rule lines above and below.

import React, { useCallback, useEffect, useRef, useState, type ReactNode } from 'react';
import { appendFileSync } from 'node:fs';
import { Box, Static, Text, useInput, useStdout } from 'ink';
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


// Streaming-commit policy. Ink's live region redraw leaks stale copies into
// scrollback once it can't reach the top of the previous render — even
// growing by a single row causes leakage when the static area above is tall
// (which it gets after a few turns). The robust fix: commit complete lines
// to <Static> (write-once, never redrawn → safe) as soon as a `\n` arrives,
// keeping only the in-progress partial line in the live region. The live
// region stays ≤ 1 visual row in normal cases.
//
// Edge case: a long single-line paragraph (no `\n` yet) can grow the live
// region past 1 visual row. We force-commit when its visual rows exceed
// FORCE_COMMIT_AT_VISUAL_ROWS, splitting at the last word boundary.
// Markdown for the split paragraph may render slightly differently across
// the seam, but that's far better than the duplication.
//
// Code fences: split markdown inside a fence renders broken on both halves,
// so while inside a fence (odd `\`\`\`` count) we suppress committing and
// just accumulate. Fences close within a few lines in practice.
const FORCE_COMMIT_AT_VISUAL_ROWS = 1;


function estimatedVisualRows(text: string, cols: number): number {
  if (cols <= 0) return text.split('\n').length;
  return text.split('\n').reduce(
    (sum, line) => sum + Math.max(1, Math.ceil(line.length / cols)),
    0,
  );
}


// TUI live-region duplication diagnostic. Appends to /tmp/tui-debug.log.
// Toggle by setting TUI_DEBUG=1 in the environment.
const DEBUG = process.env.TUI_DEBUG === '1';
function dbg(tag: string, info: unknown = {}): void {
  if (!DEBUG) return;
  try {
    appendFileSync('/tmp/tui-debug.log', `${new Date().toISOString().slice(11, 23)} ${tag} ${JSON.stringify(info)}\n`);
  } catch {}
}


// "Committed" entries — already past, won't change. Subset of AgentEvent
// kinds plus the entry envelope. assistant.isFirst lets soft-committed
// continuation chunks render without the leading ⏺ marker so they stack
// visually as one logical block.
type CoreFrozenEntry =
  | { kind: 'user'; text: string }
  | { kind: 'assistant'; text: string; isFirst: boolean }
  | {
      kind: 'tool';
      name: string;
      input: unknown;
      result: { text: string; isError: boolean } | null;
    }
  | { kind: 'footer'; elapsedSec: number }
  | { kind: 'error'; message: string };

// "Live" entries — currently streaming. isFirst is true for the very first
// chunk of a streaming block, false for any continuation chunks that follow
// a soft-commit.
type CoreLiveEntry =
  | { kind: 'assistant'; text: string; isFirst: boolean }
  | { kind: 'tool'; id: string; name: string; input: unknown }
  | null;


// True if the accumulated streaming text currently has an UNCLOSED ```fence
// — soft-committing inside a code block would split the fence and break
// markdown rendering for both halves. We just keep accumulating until the
// fence closes.
function insideCodeFence(text: string): boolean {
  const m = text.match(/```/g);
  return m !== null && m.length % 2 === 1;
}

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

  // Track terminal cols so soft-commit's visual-row estimate stays accurate
  // across resize. Subtract a couple cols for the assistant marker indent.
  const { stdout } = useStdout();
  const [cols, setCols] = useState<number>(() => stdout?.columns ?? 80);
  useEffect(() => {
    if (!stdout) return;
    const onResize = () => setCols(stdout.columns ?? 80);
    stdout.on('resize', onResize);
    return () => { stdout.off('resize', onResize); };
  }, [stdout]);
  const colsRef = useRef(cols);
  useEffect(() => { colsRef.current = cols; }, [cols]);

  const updateLive = useCallback((next: CoreLiveEntry) => {
    liveRef.current = next;
    setLive(next);
    dbg('updateLive', {
      kind: next?.kind ?? null,
      textLen: next && next.kind === 'assistant' ? next.text.length : undefined,
      head: next && next.kind === 'assistant' ? next.text.slice(0, 60) : undefined,
    });
  }, []);

  const freeze = useCallback(
    (entry: CoreFrozenEntry | { kind: '__extra__'; entry: X }) => {
      setFrozen((prev) => {
        const next = [...prev, entry];
        dbg('freeze', {
          newLen: next.length,
          kind: entry.kind,
          textLen: 'text' in entry ? entry.text.length : undefined,
          head: 'text' in entry ? entry.text.slice(0, 60) : undefined,
        });
        return next;
      });
    },
    [],
  );

  const handleEvent = useCallback(
    (ev: CoreAgentEvent | E) => {
      const e = ev as { kind: string };
      if (DEBUG) dbg('event', { kind: e.kind });
      if (e.kind === 'text_delta') {
        const t = (ev as { text: string }).text;
        const cur = liveRef.current;
        const isFirst = cur && cur.kind === 'assistant' ? cur.isFirst : true;
        const newText = cur && cur.kind === 'assistant' ? cur.text + t : t;
        const inFence = insideCodeFence(newText);
        const lastNl = newText.lastIndexOf('\n');

        // Inside a code fence: don't commit yet; the fence will close in a
        // few lines and we'll get a chance then. Avoids splitting code mid-block.
        if (inFence) {
          updateLive({ kind: 'assistant', text: newText, isFirst });
          return;
        }

        // Have at least one newline: commit everything up to the last newline,
        // keep the partial trailing line in the live region.
        if (lastNl >= 0) {
          const committed = newText.slice(0, lastNl);
          const remainder = newText.slice(lastNl + 1);
          if (committed) {
            freeze({ kind: 'assistant', text: committed, isFirst });
          }
          updateLive({ kind: 'assistant', text: remainder, isFirst: committed ? false : isFirst });
          return;
        }

        // No newline yet — partial line is growing in the live region. If
        // it's getting too tall (long paragraph wrapping past N rows), force
        // a commit at the last word boundary so the live region resets.
        const visualRows = estimatedVisualRows(newText, Math.max(20, colsRef.current - 2));
        if (visualRows > FORCE_COMMIT_AT_VISUAL_ROWS) {
          const lastSpace = newText.lastIndexOf(' ');
          const cutAt = lastSpace > 0 ? lastSpace : newText.length;
          const committed = newText.slice(0, cutAt);
          const remainder = newText.slice(cutAt + (lastSpace > 0 ? 1 : 0));
          freeze({ kind: 'assistant', text: committed, isFirst });
          updateLive({ kind: 'assistant', text: remainder, isFirst: false });
          return;
        }

        updateLive({ kind: 'assistant', text: newText, isFirst });
        return;
      }
      if (e.kind === 'text_block_done') {
        const cur = liveRef.current;
        dbg('text_block_done', { curKind: cur?.kind ?? null, curTextLen: cur && cur.kind === 'assistant' ? cur.text.length : undefined });
        if (cur && cur.kind === 'assistant') {
          updateLive(null);
          freeze({ kind: 'assistant', text: cur.text, isFirst: cur.isFirst });
        }
        return;
      }
      if (e.kind === 'tool_use_start') {
        const t = ev as { id: string; name: string; input: unknown };
        const cur = liveRef.current;
        if (cur && cur.kind === 'assistant') {
          freeze({ kind: 'assistant', text: cur.text, isFirst: cur.isFirst });
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
          freeze({ kind: 'assistant', text: cur.text, isFirst: cur.isFirst });
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
            freeze({ kind: 'assistant', text: cur.text, isFirst: cur.isFirst });
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

  // Interrupt handler: Escape cancels a running turn.
  useInput(
    (input, key) => {
      if (key.escape && busy) {
        session.abort();
        setBusy(false);
      }
    },
    { isActive: busy },
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
          if (entry.kind === 'assistant') return <AssistantBlock key={i} text={entry.text} isFirst={entry.isFirst} />;
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

      {live && live.kind === 'assistant' ? <AssistantBlock text={live.text} isFirst={live.isFirst} /> : null}
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
