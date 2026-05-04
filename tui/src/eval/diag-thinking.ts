// Probe whether Sonnet returns thinking blocks via the agent SDK and whether
// includePartialMessages emits them in the stream. Goal: see if we can
// surface the model's reasoning about tool-use decisions.

import { query } from '@anthropic-ai/claude-agent-sdk';
import { mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import {
  FULL_PROPOSE_TOOL_NAME,
  pairMcpServer,
  MCP_SERVER_NAME,
} from '../pair/proposeOptions.js';
import { SYSTEM_PROMPT } from '../pair/systemPrompt.js';

const cwd = mkdtempSync(join(tmpdir(), 'diag-thinking-'));

const q = query({
  prompt: "I'm working on Project Euler #6: find the difference between the square of the sum and the sum of the squares of the first 100 natural numbers.",
  options: {
    model: 'claude-sonnet-4-6',
    systemPrompt: SYSTEM_PROMPT,
    mcpServers: { [MCP_SERVER_NAME]: pairMcpServer },
    allowedTools: ['Read', 'Glob', 'Grep', 'Edit', 'Write', 'Bash', FULL_PROPOSE_TOOL_NAME],
    disallowedTools: ['AskUserQuestion'],
    permissionMode: 'bypassPermissions',
    includePartialMessages: true,
    cwd,
  },
});

const blockTypes = new Map<string, number>();
const deltaTypes = new Map<string, number>();

for await (const msg of q) {
  const m = msg as {
    type?: string;
    event?: { type?: string; content_block?: { type?: string }; delta?: { type?: string } };
  };
  if (m.type === 'stream_event' && m.event) {
    const et = m.event.type;
    if (et === 'content_block_start' && m.event.content_block) {
      const t = m.event.content_block.type ?? '?';
      blockTypes.set(t, (blockTypes.get(t) ?? 0) + 1);
    }
    if (et === 'content_block_delta' && m.event.delta) {
      const t = m.event.delta.type ?? '?';
      deltaTypes.set(t, (deltaTypes.get(t) ?? 0) + 1);
    }
  }
  if (m.type === 'result') break;
}

console.log('content_block types seen:');
for (const [t, n] of blockTypes) console.log(`  ${t}: ${n}`);
console.log('\ndelta types seen:');
for (const [t, n] of deltaTypes) console.log(`  ${t}: ${n}`);

process.exit(0);
