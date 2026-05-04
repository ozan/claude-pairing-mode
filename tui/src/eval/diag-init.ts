// Tiny probe: print SDK init for several configurations side by side.
// Confirms whether outputStyle is being honored end-to-end.

import { query } from '@anthropic-ai/claude-agent-sdk';
import { mkdirSync, mkdtempSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

async function probe(label: string, opts: Record<string, unknown>): Promise<void> {
  const q = query({
    prompt: 'reply with the single word: ok',
    options: {
      model: 'claude-sonnet-4-6',
      systemPrompt: '',
      permissionMode: 'bypassPermissions',
      allowedTools: [],
      includePartialMessages: false,
      ...opts,
    },
  });
  for await (const msg of q) {
    const m = msg as {
      type?: string;
      subtype?: string;
      output_style?: string;
      available_output_styles?: string[];
    };
    if (m.type === 'system' && m.subtype === 'init') {
      console.log(`\n=== ${label} ===`);
      console.log(`  output_style: ${m.output_style ?? '(unset)'}`);
      console.log(`  available_output_styles: ${(m.available_output_styles ?? []).join(', ') || '(none)'}`);
    }
    if (m.type === 'result') break;
  }
}

// Build a tmp project dir with .claude/settings.json that sets outputStyle.
function mkSettingsDir(outputStyle: string): string {
  const dir = mkdtempSync(join(tmpdir(), 'diag-init-'));
  mkdirSync(join(dir, '.claude'));
  writeFileSync(join(dir, '.claude', 'settings.json'), JSON.stringify({ outputStyle }, null, 2));
  return dir;
}

await probe('A: no opts', {});
await probe('B: per-query outputStyle=Learning (we already know this is ignored)', { outputStyle: 'Learning' } as Record<string, unknown>);
await probe(
  'C: settings.json outputStyle=Learning + settingSources=project',
  { cwd: mkSettingsDir('Learning'), settingSources: ['project'] } as Record<string, unknown>,
);
await probe(
  'D: settings.json outputStyle=Learning + settingSources=local',
  { cwd: mkSettingsDir('Learning'), settingSources: ['local'] } as Record<string, unknown>,
);
process.exit(0);
