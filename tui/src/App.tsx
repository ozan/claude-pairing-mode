// ChatApp — full-screen alt-screen Ink layout matching `claude` CLI.
//
// Architecture:
//   - One long-running `Session` (in agent/runner.ts) owns a single SDK
//     `query()` call for the entire app lifetime, so conversation history
//     persists across user turns. Submitting pushes a user message into the
//     session's queue; events flow back through a listener.
//   - Transcript is plain React state (not <Static>) — re-renders are cheap
//     at chat scale and Static's "above-the-current-frame" semantics don't
//     play well with alt-screen.
//   - The loader only shows when we're waiting on the model AND nothing is
//     currently streaming on screen — otherwise we'd see "Pondering…" stuck
//     under a fully-rendered response, which is wrong.

import React, { useCallback, useEffect, useRef, useState } from 'react';
import { Box, Static, Text, useStdout } from 'ink';
import { Spinner } from '@inkjs/ui';
import { ChatInput } from './components/Input.js';
import { Session, type AgentEvent } from './agent/runner.js';
import {
  AssistantBlock,
  ErrorLine,
  OptionsBlock,
  StepFooter,
  ToolPillRunning,
  ToolResult,
  UserLine,
} from './components/Entries.js';

type FrozenEntry =
  | { kind: 'user'; text: string }
  | { kind: 'assistant'; text: string }
  | { kind: 'tool'; name: string; input: unknown; result: { text: string; isError: boolean } | null }
  | { kind: 'options'; options: { title: string; body: string }[] }
  | { kind: 'footer'; elapsedSec: number }
  | { kind: 'error'; message: string };

type LiveEntry =
  | { kind: 'assistant'; text: string }
  | { kind: 'tool'; id: string; name: string; input: unknown }
  | null;

const LOADING_WORDS = [
  'Thinking', 'Pondering', 'Cogitating', 'Musing', 'Ruminating',
  'Brewing', 'Brainstorming', 'Mulling', 'Deliberating', 'Reflecting',
  'Considering', 'Distilling', 'Crystallizing', 'Reasoning', 'Plotting',
  'Galloping', 'Simmering', 'Percolating', 'Noodling',
];

function pickLoadingWord(): string {
  return LOADING_WORDS[Math.floor(Math.random() * LOADING_WORDS.length)]!;
}

export function App() {
  const { stdout } = useStdout();
  const rows = stdout.rows;

  const [frozen, setFrozen] = useState<FrozenEntry[]>([]);
  const [live, setLive] = useState<LiveEntry>(null);
  const [busy, setBusy] = useState(false);
  // True only between submit and the first agent event for this turn. Once
  // any content arrives we hide the loader — even if the turn continues
  // (e.g., the model keeps streaming or runs more tools after options).
  const [waitingForFirst, setWaitingForFirst] = useState(false);
  const [loadingWord, setLoadingWord] = useState(() => pickLoadingWord());
  const [inputKey, setInputKey] = useState(0);
  const turnStartRef = useRef<number>(0);
  const sessionRef = useRef<Session | null>(null);

  const freeze = useCallback((entry: FrozenEntry) => {
    setFrozen((prev) => [...prev, entry]);
  }, []);

  const handleEvent = useCallback(
    (ev: AgentEvent) => {
      // Hide the loader on the first visible event of the turn. Tool starts
      // count too, since the running tool pill is itself the progress
      // indicator. (We filter ToolSearch upstream so it doesn't trigger this
      // prematurely.)
      if (
        ev.kind === 'text_delta' ||
        ev.kind === 'tool_use_start' ||
        ev.kind === 'tool_result' ||
        ev.kind === 'options'
      ) {
        setWaitingForFirst(false);
      }

      if (ev.kind === 'text_delta') {
        setLive((cur) => {
          if (cur && cur.kind === 'assistant') {
            return { ...cur, text: cur.text + ev.text };
          }
          return { kind: 'assistant', text: ev.text };
        });
        return;
      }
      if (ev.kind === 'text_block_done') {
        setLive((cur) => {
          if (cur && cur.kind === 'assistant') {
            freeze({ kind: 'assistant', text: cur.text });
            return null;
          }
          return cur;
        });
        return;
      }
      if (ev.kind === 'tool_use_start') {
        setLive((cur) => {
          if (cur && cur.kind === 'assistant') {
            freeze({ kind: 'assistant', text: cur.text });
          }
          return { kind: 'tool', id: ev.id, name: ev.name, input: ev.input };
        });
        return;
      }
      if (ev.kind === 'tool_use_done') {
        setLive((cur) => {
          if (cur && cur.kind === 'tool' && cur.id === ev.id) {
            return { ...cur, input: ev.input };
          }
          return cur;
        });
        return;
      }
      if (ev.kind === 'tool_result') {
        setLive((cur) => {
          if (cur && cur.kind === 'tool' && cur.id === ev.toolUseId) {
            freeze({
              kind: 'tool',
              name: cur.name,
              input: cur.input,
              result: { text: ev.text, isError: ev.isError },
            });
            return null;
          }
          freeze({
            kind: 'tool',
            name: ev.name,
            input: {},
            result: { text: ev.text, isError: ev.isError },
          });
          return cur;
        });
        return;
      }
      if (ev.kind === 'options') {
        setLive((cur) => {
          if (cur && cur.kind === 'assistant') {
            freeze({ kind: 'assistant', text: cur.text });
          }
          freeze({ kind: 'options', options: ev.options });
          return null;
        });
        return;
      }
      if (ev.kind === 'result') {
        setLive((cur) => {
          if (cur && cur.kind === 'assistant') {
            freeze({ kind: 'assistant', text: cur.text });
          }
          return null;
        });
        const elapsed = (Date.now() - turnStartRef.current) / 1000;
        freeze({ kind: 'footer', elapsedSec: elapsed });
        setBusy(false);
        return;
      }
      if (ev.kind === 'error') {
        freeze({ kind: 'error', message: ev.message });
        setBusy(false);
        return;
      }
    },
    [freeze],
  );

  // Boot the long-running Session once.
  useEffect(() => {
    const s = new Session();
    s.onEvent(handleEvent);
    s.start();
    sessionRef.current = s;
    return () => {
      s.close();
    };
  }, [handleEvent]);

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
      const s = sessionRef.current;
      if (!s) return;
      setInputKey((k) => k + 1);
      setBusy(true);
      setWaitingForFirst(true);
      setLoadingWord(pickLoadingWord());
      freeze({ kind: 'user', text: trimmed });
      turnStartRef.current = Date.now();
      s.send(trimmed);
    },
    [busy, freeze],
  );

  // Show the loader only while we're waiting on the FIRST event of the
  // current turn. Once anything arrives (text, tool call, options) the
  // loader hides — even if the turn continues for a while afterwards.
  const showLoader = busy && waitingForFirst;

  return (
    <>
      {/* Static commits past entries permanently — Ink writes them once and
          never re-renders them. This prevents the layout corruption we saw
          with plain state (where streaming text deltas would re-render the
          whole transcript on each tick and Ink couldn't reliably clear
          previous frames). */}
      <Static items={frozen.map((entry, i) => ({ entry, i }))}>
        {({ entry, i }) => {
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
          if (entry.kind === 'options') return <OptionsBlock key={i} options={entry.options} />;
          if (entry.kind === 'footer') return <StepFooter key={i} elapsedSec={entry.elapsedSec} />;
          if (entry.kind === 'error') return <ErrorLine key={i} message={entry.message} />;
          return null;
        }}
      </Static>

      {/* Live region: streaming assistant block / running tool pill */}
      {live && live.kind === 'assistant' ? <AssistantBlock text={live.text} /> : null}
      {live && live.kind === 'tool' ? <ToolPillRunning name={live.name} input={live.input} /> : null}

      {/* Loader: only when busy AND nothing is on screen yet for this turn */}
      {showLoader ? (
        <Box marginTop={1}>
          <Box marginRight={1}>
            <Spinner />
          </Box>
          <Text color="#ff875f">{loadingWord}…</Text>
        </Box>
      ) : null}

      {/* Input area with thin grey rule lines above and below — matches CC. */}
      <Box
        marginTop={1}
        flexDirection="column"
        borderStyle="single"
        borderLeft={false}
        borderRight={false}
        borderColor="#808080"
      >
        <ChatInput key={inputKey} isDisabled={busy} onSubmit={onSubmit} />
      </Box>
    </>
  );
}
