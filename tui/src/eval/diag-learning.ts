// Diagnostic for the Learning output style. Tries several user-message
// framings to find one that actually activates the "Learn by Doing /
// TODO(human)" protocol on Sonnet.
//
// We bypass Session and call SDK query() directly so this is a clean
// single-prompt probe.
//
// Run: bun run src/eval/diag-learning.ts

import { query } from '@anthropic-ai/claude-agent-sdk';
import { mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const MODEL = 'claude-sonnet-4-6';

const FRAMINGS: Array<{ name: string; prompt: string }> = [
  {
    name: 'A_solve_directly',
    prompt: "Exercism 'Pangram': write `is_pangram(text)` that returns True iff the input contains every letter of the alphabet at least once (case-insensitive).",
  },
  {
    name: 'B_explicit_learn',
    prompt: "I want to learn by doing. Help me implement Exercism's `is_pangram(text)` function (returns True iff input contains every letter of the alphabet, case-insensitive). Set up the file with a TODO(human) gap for me to fill in the core logic.",
  },
  {
    name: 'C_junior_asks',
    prompt: "I'm a junior engineer working through Exercism. Today's problem: `is_pangram(text)` — returns True iff the input contains every letter of the alphabet (case-insensitive). I want to write the implementation myself but I'd like you to scaffold the file and tests, then point me at where to write code.",
  },
];


async function runOne(framing: { name: string; prompt: string }): Promise<void> {
  const cwd = mkdtempSync(join(tmpdir(), `diag-learning-${framing.name}-`));
  console.log(`\n=== ${framing.name} ===`);
  console.log(`prompt: ${framing.prompt.slice(0, 80)}...`);

  const q = query({
    prompt: framing.prompt,
    options: {
      model: MODEL,
      systemPrompt: '',
      permissionMode: 'bypassPermissions',
      allowedTools: ['Read', 'Glob', 'Grep', 'Edit', 'Write', 'Bash'],
      includePartialMessages: false,
      cwd,
      // outputStyle isn't on the SDK Options type but is accepted at runtime;
      // spread to dodge the strict typecheck.
      ...({ outputStyle: 'Learning' } as Record<string, unknown>),
    },
  });

  let text = '';
  const writes: Array<{ path: string; content: string }> = [];
  for await (const msg of q) {
    const m = msg as { type?: string; message?: { content?: Array<{ type: string; text?: string; name?: string; input?: unknown }> } };
    if (m.type === 'assistant' && m.message?.content) {
      for (const block of m.message.content) {
        if (block.type === 'text' && block.text) text += block.text;
        if (block.type === 'tool_use' && block.name === 'Write') {
          const inp = block.input as { file_path?: string; content?: string };
          writes.push({ path: inp.file_path ?? '?', content: inp.content ?? '' });
        }
      }
    }
    if (m.type === 'result') break;
  }

  const hasLearnByDoing = /Learn by Doing/i.test(text);
  const hasTodoHuman = /TODO\(human\)/.test(text) || writes.some((w) => /TODO\(human\)/.test(w.content));
  console.log(`assistant text length: ${text.length}`);
  console.log(`Writes: ${writes.length}`);
  for (const w of writes) {
    const todo = /TODO\(human\)/.test(w.content) ? '  [HAS TODO(human)!]' : '';
    console.log(`  Write ${w.path} (${w.content.length} bytes)${todo}`);
  }
  console.log(`Mentions "Learn by Doing": ${hasLearnByDoing}`);
  console.log(`Has TODO(human) anywhere: ${hasTodoHuman}`);
  if (hasLearnByDoing || hasTodoHuman) {
    const idx = Math.max(text.search(/Learn by Doing/i), text.search(/TODO\(human\)/));
    console.log(`---excerpt:---\n${text.slice(Math.max(0, idx - 100), idx + 400)}`);
  } else {
    console.log(`---first 300 chars of text:---\n${text.slice(0, 300)}`);
  }
}

for (const framing of FRAMINGS) {
  await runOne(framing);
}

process.exit(0);
