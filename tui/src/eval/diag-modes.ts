// Print SDK init for each of the four configurations the eval uses, so we
// can verify before a run that:
//   - baseline: empty system prompt, no MCP, no Learning style
//   - initial: our SYSTEM_PROMPT, MCP w/ propose_options, no Learning
//   - learning: empty system prompt, no MCP, outputStyle=Learning active
//   - user-model: empty tool list, neutral system prompt
//
// Run: bun run src/eval/diag-modes.ts

import { query } from '@anthropic-ai/claude-agent-sdk';
import { mkdirSync, mkdtempSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import {
  FULL_PROPOSE_TOOL_NAME,
  pairMcpServer,
  MCP_SERVER_NAME,
} from '../pair/proposeOptions.js';
import { SYSTEM_PROMPT } from '../pair/systemPrompt.js';
import { USER_SYSTEM_PROMPT } from './userModel.js';

const PAIR_MODEL = 'claude-sonnet-4-6';
const USER_MODEL = 'claude-haiku-4-5-20251001';

type InitInfo = {
  output_style?: string;
  available_output_styles?: string[];
  tools: string[];
  mcp_servers: Array<{ name: string; status: string }>;
};

async function probe(
  label: string,
  prompt: string,
  options: Record<string, unknown>,
): Promise<InitInfo | null> {
  const q = query({
    prompt,
    options: {
      permissionMode: 'bypassPermissions',
      includePartialMessages: false,
      ...options,
    },
  });
  let init: InitInfo | null = null;
  for await (const msg of q) {
    const m = msg as { type?: string; subtype?: string };
    if (m.type === 'system' && m.subtype === 'init') {
      init = msg as unknown as InitInfo;
    }
    if (m.type === 'result') break;
  }
  console.log(`\n=== ${label} ===`);
  if (!init) {
    console.log('  (no init message captured)');
    return null;
  }
  console.log(`  output_style: ${init.output_style ?? '(unset)'}`);
  const customMcp = init.mcp_servers.filter((s) => s.name === MCP_SERVER_NAME);
  console.log(`  pairing MCP: ${customMcp.length === 0 ? 'NOT REGISTERED' : customMcp[0]!.status}`);
  const proposeOptionsAvailable = init.tools.includes(FULL_PROPOSE_TOOL_NAME);
  console.log(`  ${FULL_PROPOSE_TOOL_NAME}: ${proposeOptionsAvailable ? 'in tool list' : 'NOT in tool list'}`);
  console.log(`  total tools available: ${init.tools.length}`);
  if (label.startsWith('USER MODEL')) {
    console.log(`  tool list: ${init.tools.join(', ')}`);
  }
  return init;
}

function makeSettingsCwd(outputStyle?: string): string {
  const dir = mkdtempSync(join(tmpdir(), 'diag-modes-'));
  if (outputStyle) {
    mkdirSync(join(dir, '.claude'));
    writeFileSync(join(dir, '.claude', 'settings.json'), JSON.stringify({ outputStyle }));
  }
  return dir;
}

await probe('PAIR — baseline mode', 'reply "ok"', {
  model: PAIR_MODEL,
  systemPrompt: '',
  mcpServers: {},
  allowedTools: ['Read', 'Glob', 'Grep', 'Edit', 'Write', 'Bash'],
  disallowedTools: ['AskUserQuestion'],
  cwd: makeSettingsCwd(),
});

await probe('PAIR — initial mode (didactic + propose_options)', 'reply "ok"', {
  model: PAIR_MODEL,
  systemPrompt: SYSTEM_PROMPT,
  mcpServers: { [MCP_SERVER_NAME]: pairMcpServer },
  allowedTools: ['Read', 'Glob', 'Grep', 'Edit', 'Write', 'Bash', FULL_PROPOSE_TOOL_NAME],
  disallowedTools: ['AskUserQuestion'],
  cwd: makeSettingsCwd(),
});

await probe('PAIR — learning mode (outputStyle via settings.json)', 'reply "ok"', {
  model: PAIR_MODEL,
  systemPrompt: '',
  mcpServers: {},
  allowedTools: ['Read', 'Glob', 'Grep', 'Edit', 'Write', 'Bash'],
  disallowedTools: ['AskUserQuestion'],
  cwd: makeSettingsCwd('Learning'),
  settingSources: ['project'],
});

await probe('USER MODEL — neutral, no tools', 'reply "ok"', {
  model: USER_MODEL,
  systemPrompt: USER_SYSTEM_PROMPT,
  allowedTools: [],
  // allowedTools: [] is silently ignored — disallowedTools is required.
  disallowedTools: [
    'Task', 'AskUserQuestion', 'Bash', 'CronCreate', 'CronDelete', 'CronList',
    'Edit', 'EnterPlanMode', 'EnterWorktree', 'ExitPlanMode', 'ExitWorktree',
    'Glob', 'Grep', 'Monitor', 'NotebookEdit', 'PushNotification', 'Read',
    'RemoteTrigger', 'ScheduleWakeup', 'Skill', 'TaskOutput', 'TaskStop',
    'TodoWrite', 'ToolSearch', 'WebFetch', 'WebSearch', 'Write',
    'mcp__claude_ai_Gmail__authenticate', 'mcp__claude_ai_Gmail__complete_authentication',
    'mcp__claude_ai_Google_Calendar__authenticate', 'mcp__claude_ai_Google_Calendar__complete_authentication',
    'mcp__claude_ai_Google_Drive__authenticate', 'mcp__claude_ai_Google_Drive__complete_authentication',
  ],
});

process.exit(0);
