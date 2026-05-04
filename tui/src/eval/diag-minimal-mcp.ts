// Most minimal MCP tool repro. Goal: prove that the SDK CAN dispatch a
// custom MCP tool to our body and return its result. No Session wrapper,
// no propose_options, no schema gymnastics. One tool, one prompt, full
// raw stream dumped.
//
// If the model calls it and we see `[BODY] called with input=...` followed
// by a non-error tool_result, dispatch works. If the body never runs but
// we see "No such tool available", dispatch is fundamentally broken in
// our setup.
//
// Run: bun run src/eval/diag-minimal-mcp.ts

import { query, createSdkMcpServer, tool } from '@anthropic-ai/claude-agent-sdk';
import { mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { z } from 'zod';

const echoTool = tool(
  'echo_back',
  'Echo back the provided message. Use this when the user asks you to echo, repeat, or test the tool.',
  {
    message: z.string().describe('The text to echo back, verbatim.'),
  },
  async (args: { message: string }) => {
    process.stderr.write(`[BODY] echo_back invoked  message="${args.message}"\n`);
    return {
      content: [{ type: 'text' as const, text: `ECHO: ${args.message}` }],
    };
  },
);

const echoServer = createSdkMcpServer({
  name: 'minimal',
  version: '0.1.0',
  tools: [echoTool],
});

const FULL_TOOL_NAME = 'mcp__minimal__echo_back';
const sandbox = mkdtempSync(join(tmpdir(), 'diag-minimal-'));

console.log('Sending prompt...\n');
const q = query({
  prompt: 'Please call the echo_back tool with message="hello world", then reply with just "done".',
  options: {
    model: 'claude-sonnet-4-6',
    systemPrompt: 'You are a test agent. Use the echo_back tool when asked.',
    mcpServers: { minimal: echoServer },
    permissionMode: 'bypassPermissions',
    allowedTools: [FULL_TOOL_NAME],
    cwd: sandbox,
    includePartialMessages: false,
  },
});

let toolUseSeen = false;
let toolResultSeen = false;
let toolResultIsError = false;
let toolResultContent = '';

for await (const msg of q) {
  const m = msg as { type?: string };

  if (m.type === 'assistant') {
    const am = msg as { message: { content: Array<{ type: string; name?: string; input?: unknown; id?: string }> } };
    for (const block of am.message.content) {
      if (block.type === 'tool_use') {
        toolUseSeen = true;
        console.log(`[STREAM] assistant tool_use  name=${block.name}  input=${JSON.stringify(block.input)}`);
      } else if (block.type === 'text') {
        const t = (block as { text?: string }).text ?? '';
        console.log(`[STREAM] assistant text: ${t.slice(0, 200)}`);
      }
    }
  }

  if (m.type === 'user') {
    const um = msg as { message: { content: Array<{ type: string; tool_use_id?: string; content?: unknown; is_error?: boolean }> } };
    if (Array.isArray(um.message.content)) {
      for (const block of um.message.content) {
        if (block.type === 'tool_result') {
          toolResultSeen = true;
          toolResultIsError = Boolean(block.is_error);
          toolResultContent = typeof block.content === 'string' ? block.content : JSON.stringify(block.content);
          console.log(`[STREAM] tool_result  is_error=${block.is_error}  content=${toolResultContent.slice(0, 200)}`);
        }
      }
    }
  }

  if (m.type === 'result') break;
}

console.log('\n=== VERDICT ===');
console.log(`Tool was invoked by model:  ${toolUseSeen ? 'YES' : 'NO'}`);
console.log(`Tool result was returned:   ${toolResultSeen ? 'YES' : 'NO'}`);
if (toolResultSeen) {
  console.log(`Tool result is_error:       ${toolResultIsError}`);
  console.log(`Tool result content (first 200): ${toolResultContent.slice(0, 200)}`);
}

process.exit(0);
