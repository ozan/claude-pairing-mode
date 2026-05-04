// A/B test: does outputStyle='Learning' actually change Sonnet's behavior,
// or is the apparent activation just an artifact of prompt content?
//
// Two probes per prompt: one with outputStyle='Learning', one without.
// Same prompt, same model, same cwd shape, same temperature defaults.
// If outputs are functionally identical, the style is a no-op.
//
// Run: bun run src/eval/diag-learning-ab.ts

import { query } from '@anthropic-ai/claude-agent-sdk';
import { mkdirSync, mkdtempSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const MODEL = 'claude-sonnet-4-6';

// Two prompts. Prompt 1 has NO TODO(human) hint. Prompt 2 explicitly
// asks for it. Together they tell us: (a) does the style add the protocol
// when not asked, and (b) does the style add anything BEYOND what an
// explicit ask would produce.
const PROMPTS: Array<{ name: string; text: string }> = [
  {
    name: 'P1_neutral',
    text: "Exercism 'Pangram': write `is_pangram(text)` that returns True iff the input contains every letter of the alphabet at least once (case-insensitive).",
  },
  {
    name: 'P2_explicit_todo',
    text: "I want to learn by doing — please scaffold the code with a single `TODO(human)` gap for me to fill in the core logic, plus tests if helpful, and then wait for me to attempt the implementation.\n\nExercism 'Pangram': write `is_pangram(text)` that returns True iff the input contains every letter of the alphabet at least once (case-insensitive).",
  },
];

type Result = {
  promptName: string;
  styleOn: boolean;
  text: string;
  writes: Array<{ path: string; content: string }>;
};

async function probe(prompt: string, withStyle: boolean): Promise<Result['text'] extends string ? Result : never> {
  // Activate Learning via settings.json in the cwd + settingSources=project.
  // The per-query outputStyle option is silently ignored — see diag-init.ts.
  const cwd = mkdtempSync(join(tmpdir(), `diag-ab-`));
  if (withStyle) {
    mkdirSync(join(cwd, '.claude'));
    writeFileSync(join(cwd, '.claude', 'settings.json'), JSON.stringify({ outputStyle: 'Learning' }));
  }
  const q = query({
    prompt,
    options: {
      model: MODEL,
      systemPrompt: '',
      permissionMode: 'bypassPermissions',
      allowedTools: ['Read', 'Glob', 'Grep', 'Edit', 'Write', 'Bash'],
      includePartialMessages: false,
      cwd,
      ...(withStyle ? ({ settingSources: ['project'] } as Record<string, unknown>) : {}),
    },
  });

  let text = '';
  const writes: Result['writes'] = [];
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
  return { promptName: '', styleOn: withStyle, text, writes } as Result;
}

function summarize(r: Result): void {
  const tag = r.styleOn ? 'STYLE=Learning' : 'STYLE=off       ';
  const writeCount = r.writes.length;
  const todoInWrites = r.writes.some((w) => /TODO\(human\)/.test(w.content));
  const todoInText = /TODO\(human\)/.test(r.text);
  const learnByDoing = /Learn by Doing/i.test(r.text);
  const waitForHuman = /wait.*(?:for you|for the human|until you|to implement)/i.test(r.text);
  const passPlaceholder = r.writes.some((w) => /\bpass\b/.test(w.content));
  console.log(`  ${tag}  writes=${writeCount}  TODO=${todoInWrites || todoInText}  LbD=${learnByDoing}  wait=${waitForHuman}  text-len=${r.text.length}`);
  if (r.writes.length > 0) {
    for (const w of r.writes) {
      console.log(`    write ${w.path.split('/').pop()} (${w.content.length} bytes)${/TODO\(human\)/.test(w.content) ? ' [TODO]' : ''}${/\bpass\b/.test(w.content) ? ' [pass]' : ''}`);
    }
  }
}

for (const p of PROMPTS) {
  console.log(`\n=== ${p.name} ===`);
  console.log(`prompt: ${p.text.replace(/\n/g, ' / ').slice(0, 100)}...`);
  const off = await probe(p.text, false);
  const on = await probe(p.text, true);
  summarize(off);
  summarize(on);

  // Print a short delta of the assistant text length and some opening lines.
  console.log(`  --- STYLE off opening (200 chars):`);
  console.log(`    ${off.text.slice(0, 200).replace(/\n/g, ' ⏎ ')}`);
  console.log(`  --- STYLE on  opening (200 chars):`);
  console.log(`    ${on.text.slice(0, 200).replace(/\n/g, ' ⏎ ')}`);
}

process.exit(0);
