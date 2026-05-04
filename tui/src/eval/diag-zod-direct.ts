// Deterministic Zod-validation probe.
//
// We've been speculating about whether the SDK's "No such tool available"
// rejection is caused by our Zod schema vs something else. This script
// removes the SDK from the loop entirely:
//
// 1. Take the EXACT malformed input captured from a failing eval run.
// 2. Run it through the Zod schema we currently have on the MCP tool.
// 3. Report pass/fail.
//
// If Zod rejects → schema IS the problem; tighten/loosen accordingly.
// If Zod accepts → the rejection is happening somewhere else (CLI subprocess,
//   API-level validation, etc.) and schema changes won't help.
//
// Run: bun run src/eval/diag-zod-direct.ts

import { readFileSync } from 'node:fs';
import { z } from 'zod';

// Load one captured malformed input from the failing eval.
function loadCapturedInput(transcriptPath: string): unknown {
  const lines = readFileSync(transcriptPath, 'utf-8').split('\n').filter(Boolean);
  for (const line of lines) {
    let rec;
    try { rec = JSON.parse(line); } catch { continue; }
    if (rec.kind !== 'pair_raw') continue;
    const msg = rec.msg;
    if (msg?.type !== 'assistant') continue;
    for (const block of msg.message?.content ?? []) {
      if (block.type === 'tool_use' && block.name === 'mcp__pairing__propose_options') {
        return block.input;
      }
    }
  }
  throw new Error(`No propose_options call found in ${transcriptPath}`);
}

const inputs = {
  'leetcode (failed at SDK)': loadCapturedInput('/Users/oz/dev/ai-pair-proto/eval-runs/_smoke-relaxed/leetcode-trap-rain-water/transcript.jsonl'),
  'euler-6 (failed at SDK)': loadCapturedInput('/Users/oz/dev/ai-pair-proto/eval-runs/_smoke-relaxed/euler-6-sum-square-diff/transcript.jsonl'),
  'mini-calc (succeeded)': loadCapturedInput('/Users/oz/dev/ai-pair-proto/eval-runs/_smoke-A-sonnet/ours-mini-calculator/transcript.jsonl'),
};

// Three candidate schemas to test.
const schemas: Record<string, z.ZodTypeAny> = {
  'STRICT (original)': z.object({
    options: z.array(
      z.object({ title: z.string(), body: z.string() }),
    ).min(2).max(2),
    private_notes: z.object({
      best_index: z.number().int(),
      rationale: z.string(),
    }),
  }),
  'UNION (array | string)': z.object({
    options: z.union([
      z.array(z.object({ title: z.string(), body: z.string() })).min(2).max(2),
      z.string(),
    ]),
    private_notes: z.union([
      z.object({
        best_index: z.number().int(),
        rationale: z.string(),
      }),
      z.string(),
      z.null(),
    ]).optional(),
  }),
  'UNKNOWN (current)': z.object({
    options: z.unknown(),
    private_notes: z.unknown().optional(),
  }),
};

console.log('Schema validation test\n=====================\n');

for (const [inputLabel, input] of Object.entries(inputs)) {
  console.log(`INPUT: ${inputLabel}`);
  console.log(`  options type: ${Array.isArray((input as Record<string, unknown>).options) ? 'array' : typeof (input as Record<string, unknown>).options}`);
  console.log(`  private_notes type: ${(input as Record<string, unknown>).private_notes === null ? 'null' : typeof (input as Record<string, unknown>).private_notes}`);
  for (const [schemaLabel, schema] of Object.entries(schemas)) {
    const result = schema.safeParse(input);
    console.log(`    [${schemaLabel}] → ${result.success ? 'PASS' : 'FAIL: ' + result.error.issues.map((i) => i.message).slice(0, 2).join('; ')}`);
  }
  console.log();
}
