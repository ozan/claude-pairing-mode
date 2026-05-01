// PairApp wires the didactic 2-option pair-programmer experiment into the
// generic core App: registers the propose_options MCP tool + system prompt
// with a Session, and provides an extension renderer that turns the
// synthesized `options` event into the 2-column OptionsBlock.

import React, { useMemo } from 'react';
import { App } from '../core/App.js';
import { Session } from '../core/Session.js';
import { OptionsBlock } from './OptionsBlock.js';
import {
  FULL_PROPOSE_TOOL_NAME,
  pairMcpServer,
  proposeOptionsHandler,
  MCP_SERVER_NAME,
  type OptionsEvent,
} from './proposeOptions.js';
import { SYSTEM_PROMPT } from './systemPrompt.js';

type OptionsEntry = { options: { title: string; body: string }[] };

export function PairApp() {
  // One Session for the whole app lifetime (so the model remembers across
  // turns). Memoize so React doesn't recreate on each render.
  const session = useMemo(
    () =>
      new Session<OptionsEvent>({
        systemPrompt: SYSTEM_PROMPT,
        mcpServers: { [MCP_SERVER_NAME]: pairMcpServer },
        allowedTools: ['Read', 'Glob', 'Grep', 'Edit', 'Write', 'Bash'],
        customToolHandlers: {
          [FULL_PROPOSE_TOOL_NAME]: proposeOptionsHandler,
        },
      }),
    [],
  );

  return (
    <App<OptionsEvent, OptionsEntry>
      session={session}
      extra={{
        reduce: (event) => {
          if (event.kind === 'options') {
            return { options: event.options };
          }
          return null;
        },
        render: (entry, i) => <OptionsBlock key={`extra-${i}`} options={entry.options} />,
      }}
    />
  );
}
