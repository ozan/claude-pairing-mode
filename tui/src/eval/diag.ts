// Diagnostic: start a Session with the same config the eval uses and dump
// the SDK's `init` message so we can see exactly which tools the model has
// in its tool list. Then send one prompt and watch what tool_use blocks
// the model emits.
//
// Run: bun run src/eval/diag.ts [--model claude-sonnet-4-6]

import { query } from '@anthropic-ai/claude-agent-sdk';
import {
  FULL_PROPOSE_TOOL_NAME,
  pairMcpServer,
  MCP_SERVER_NAME,
} from '../pair/proposeOptions.js';
import { SYSTEM_PROMPT } from '../pair/systemPrompt.js';

const model = process.argv.includes('--model')
  ? process.argv[process.argv.indexOf('--model') + 1]!
  : 'claude-sonnet-4-6';

console.log(`Model: ${model}`);
console.log(`Expected MCP tool name: ${FULL_PROPOSE_TOOL_NAME}\n`);

async function* singlePrompt() {
  yield {
    type: 'user' as const,
    message: { role: 'user' as const, content: 'List the tools you have access to. Then call the propose_options tool with two trivial options about whether to print "hi" or "hello". Use whatever name appears in your tool list.' },
    parent_tool_use_id: null,
  };
}

const q = query({
  prompt: singlePrompt(),
  options: {
    model,
    systemPrompt: SYSTEM_PROMPT,
    mcpServers: { [MCP_SERVER_NAME]: pairMcpServer },
    allowedTools: ['Read', 'Glob', 'Grep', 'Edit', 'Write', 'Bash', FULL_PROPOSE_TOOL_NAME],
    permissionMode: 'bypassPermissions',
    includePartialMessages: false,
  },
});

let assistantText = '';
for await (const msg of q) {
  const m = msg as { type?: string; subtype?: string };

  if (m.type === 'system' && m.subtype === 'init') {
    const init = msg as {
      tools: string[];
      mcp_servers: Array<{ name: string; status: string }>;
    };
    console.log('=== SDK INIT MESSAGE ===');
    console.log('mcp_servers:', JSON.stringify(init.mcp_servers, null, 2));
    console.log('\ntools available to model (' + init.tools.length + '):');
    for (const t of init.tools) {
      const tag = t.startsWith('mcp__') ? ' [MCP]' : '';
      const ours = t === FULL_PROPOSE_TOOL_NAME ? '  ← ours!' : '';
      console.log('  ' + t + tag + ours);
    }
    const ourToolPresent = init.tools.includes(FULL_PROPOSE_TOOL_NAME);
    console.log(`\npropose_options in tool list: ${ourToolPresent ? 'YES' : 'NO'}`);
    console.log('========================\n');
    continue;
  }

  if (m.type === 'assistant') {
    const am = msg as { message: { content: Array<{ type: string; text?: string; name?: string; input?: unknown }> } };
    for (const block of am.message.content) {
      if (block.type === 'text' && block.text) {
        assistantText += block.text;
      }
      if (block.type === 'tool_use') {
        console.log(`>>> assistant called tool: ${block.name}`);
        console.log(`    input: ${JSON.stringify(block.input).slice(0, 200)}`);
      }
    }
  }

  if (m.type === 'user') {
    const um = msg as { message: { content: Array<{ type: string; tool_use_id?: string; content?: unknown; is_error?: boolean }> } };
    for (const block of um.message.content) {
      if (block.type === 'tool_result') {
        const text = typeof block.content === 'string' ? block.content : JSON.stringify(block.content);
        console.log(`<<< tool_result for ${block.tool_use_id}: ${text.slice(0, 200)} (error=${!!block.is_error})`);
      }
    }
  }

  if (m.type === 'result') break;
}

console.log('\n=== ASSISTANT FINAL TEXT ===');
console.log(assistantText.trim());

process.exit(0);
