// LLM-as-judge grader. Sends a transcript (and optionally a baseline
// transcript on the same problem) to Opus, gets back per-criterion scores
// + rationales as JSON.
//
// The rubric prompt lives here as a constant so it's easy to iterate on.
// Output schema is fixed so post-hoc aggregators have something stable.

import { query } from '@anthropic-ai/claude-agent-sdk';

export const DEFAULT_GRADER_MODEL = 'claude-opus-4-7';

export const GRADER_SYSTEM_PROMPT = `
You are an expert evaluator of pair-programming sessions. You are reviewing transcripts of conversations between an AI pair-programming assistant ("Pair") and a junior software engineer ("User"). The Pair's goal is BOTH to help solve the problem AND to teach the user something useful along the way (didactic pair-programming).

You will see one transcript from the experiment under review ("EXPERIMENT"). You may also see a transcript from a BASELINE run on the same problem where the Pair had no special instructions — this establishes a productivity reference point.

Score the EXPERIMENT on 7 criteria, each on a 1–5 integer scale. Use the anchors below; calibrate to them rather than to your priors.

== PEDAGOGICAL VALUE (judge from EXPERIMENT alone) ==

1. question_frequency - How many times does the pair engage the user with didactic questions at teachable moments (subtleties, classic gotchas, trade-offs, idioms worth knowing)?
   1: few didactic questions, mostly code-writing or clarifying questions with few teachable moments
   3: at least some effort by the pair to question the user with pedagogical intentenio
   5: high frequency of questioning, with most meaningful decision points involving the user

2. question_quality — When the Pair frames a choice (or surfaces a fork), does it hit the CRUX of the problem (boundary conditions, algorithmic trade-offs, design tensions)?
   1: choices are cosmetic, trivial, or absent.
   3: at least one substantive choice; others surface or are missed.
   5: choices consistently target the most consequential parts of the problem space.

3. scaffolding - Is the sequence of questions well scaffolded, with a logical progression, a smooth difficulty gradient, and no spoilers?
   1: too few questions, answers revealed/hinted or too obvious, or major jumps in difficulty
   3: reasonable scaffolding with no spoilers, but some abrupt skill or domain jumps
   5: pedagogically perfect scaffolding

4. flow_and_tone - Does the pair provide useful and actionable guidance, and engage in natural back and forth with the user, resulting in good conversational flow?
   1: bad conversational dynamic, excessive conflict, non sequiturs or unactionable or irrelevant responses
   3: tone is warm but conversational flow is not fluid
   5: conversational flow is natural and reflects an ideal pedagogical experience for both participants


== PRODUCTIVITY (compare EXPERIMENT to BASELINE if present) ==

5. effectiveness — Does the EXPERIMENT's final code correctly solve the original problem, in a manner equivalent to the baseline?
   1: broken, missing requirements, or never converges, or is significantly better than the baseline
   3: generally works and comparable to baseline
   5: an ideal solution, noticeably better than the baseline

6. friction — Was the conversation efficient given the problem and given the BASELINE reference?
   With BASELINE: penalize taking substantially longer (turns or prose volume) without a proportional pedagogical payoff.
   1: 2x+ longer than baseline with no proportional teaching gain.
   3: comparable to baseline OR only slighly longer with proportional payoff.
   5: tighter than baseline, or substantially better teaching for modest extra length.
   Without BASELINE: judge friction in absolute terms (3 = average for the problem class).

Be specific in rationales — name the moments you're scoring on. Each rationale should be 1–3 sentences. No flattery, no hedging language; act as a calibrated reviewer.

Output a SINGLE JSON object with this exact shape — no prose outside the JSON, no markdown fence:

{
  "pedagogical": {
    "question_frequency": { "score": 1-5, "rationale": "..." },
    "question_quality":   { "score": 1-5, "rationale": "..." },
    "scaffolding":        { "score": 1-5, "rationale": "..." },
    "flow_and_tone":      { "score": 1-5, "rationale": "..." }
  },
  "productivity": {
    "effectiveness":      { "score": 1-5, "rationale": "..." },
    "friction":           { "score": 1-5, "rationale": "..." }
  }
}
`.trim();


export type CriterionScore = { score: number; rationale: string };

export type Grade = {
  pedagogical: {
    question_frequency: CriterionScore;
    question_quality: CriterionScore;
    scaffolding: CriterionScore;
    flow_and_tone: CriterionScore;
  };
  productivity: {
    effectiveness: CriterionScore;
    friction: CriterionScore;
  };
};

/**
 * Per-criterion weights used to compute the final weighted score. Sum to 1.
 * Edit here to re-balance.
 */
export const SCORE_WEIGHTS = {
  question_frequency: 0.3,
  question_quality: 0.1,
  scaffolding: 0.1,
  flow_and_tone: 0.1,
  effectiveness: 0.2,
  friction: 0.2,
} as const;

export function weightedScore(grade: Grade): number {
  const w = SCORE_WEIGHTS;
  return (
    grade.pedagogical.question_frequency.score * w.question_frequency +
    grade.pedagogical.question_quality.score * w.question_quality +
    grade.pedagogical.scaffolding.score * w.scaffolding +
    grade.pedagogical.flow_and_tone.score * w.flow_and_tone +
    grade.productivity.effectiveness.score * w.effectiveness +
    grade.productivity.friction.score * w.friction
  );
}

/**
 * Linear normalization of a 1–5 weighted score to 0–1, where uniformly-1
 * (worst possible) maps to 0 and uniformly-5 (best possible) maps to 1.
 * Standard educational-rubric formula: (raw − min) / (max − min).
 */
export function normalizedScore(grade: Grade): number {
  return (weightedScore(grade) - 1) / 4;
}

export type GraderOptions = {
  model?: string;
  systemPrompt?: string;
};

/**
 * Best-effort JSON extraction. Strip a ```json fence if present, otherwise
 * grab the substring from the first `{` to the matching last `}`.
 * Models sometimes emit a leading "Here is my evaluation:" preamble or
 * trailing prose; this is more forgiving than strict JSON.parse on raw.
 */
function extractJson(s: string): string {
  const trimmed = s.trim();
  const fence = trimmed.match(/```(?:json)?\s*([\s\S]*?)\s*```/);
  if (fence) return fence[1]!.trim();
  const first = trimmed.indexOf('{');
  const last = trimmed.lastIndexOf('}');
  if (first !== -1 && last > first) return trimmed.slice(first, last + 1);
  return trimmed;
}

const PEDAGOGICAL_KEYS = ['question_frequency', 'question_quality', 'scaffolding', 'flow_and_tone'] as const;
const PRODUCTIVITY_KEYS = ['effectiveness', 'friction'] as const;

/**
 * Strictly validate AND normalize a parsed grade. Drops any extra fields
 * Opus invented (e.g. `scaffolding_note`) and verifies all required ones
 * are present with numeric scores. Returns null if invalid.
 */
function validateAndNormalize(parsed: unknown): Grade | null {
  if (!parsed || typeof parsed !== 'object') return null;
  const p = parsed as Record<string, unknown>;
  const peds = p.pedagogical as Record<string, unknown> | undefined;
  const prods = p.productivity as Record<string, unknown> | undefined;
  if (!peds || !prods) return null;

  const pedOut: Record<string, CriterionScore> = {};
  for (const k of PEDAGOGICAL_KEYS) {
    const c = peds[k] as { score?: unknown; rationale?: unknown } | undefined;
    if (!c || typeof c.score !== 'number' || !Number.isFinite(c.score)) return null;
    pedOut[k] = { score: c.score, rationale: typeof c.rationale === 'string' ? c.rationale : '' };
  }
  const prodOut: Record<string, CriterionScore> = {};
  for (const k of PRODUCTIVITY_KEYS) {
    const c = prods[k] as { score?: unknown; rationale?: unknown } | undefined;
    if (!c || typeof c.score !== 'number' || !Number.isFinite(c.score)) return null;
    prodOut[k] = { score: c.score, rationale: typeof c.rationale === 'string' ? c.rationale : '' };
  }
  return {
    pedagogical: pedOut as Grade['pedagogical'],
    productivity: prodOut as Grade['productivity'],
  };
}

async function callGrader(prompt: string, opts: GraderOptions): Promise<string> {
  const q = query({
    prompt,
    options: {
      model: opts.model ?? DEFAULT_GRADER_MODEL,
      systemPrompt: opts.systemPrompt ?? GRADER_SYSTEM_PROMPT,
      permissionMode: 'bypassPermissions',
      allowedTools: [],
      includePartialMessages: false,
    },
  });
  let text = '';
  for await (const msg of q) {
    const m = msg as { type?: string; message?: { content?: Array<{ type: string; text?: string }> } };
    if (m.type === 'assistant' && m.message?.content) {
      for (const block of m.message.content) {
        if (block.type === 'text' && block.text) text += block.text;
      }
    }
    if (m.type === 'result') break;
  }
  return text;
}

/**
 * Grade one transcript. If `baseline` is provided, the grader sees both
 * and uses the baseline as the productivity reference.
 *
 * Retries once with stricter wording if the model omits a required field
 * or invents extras — both modes were observed in the wild.
 */
export async function gradeTranscript(args: {
  experiment: { slug: string; markdown: string };
  baseline?: { slug: string; markdown: string };
  opts?: GraderOptions;
}): Promise<{ grade: Grade; raw: string }> {
  const opts = args.opts ?? {};

  const sections: string[] = [];
  if (args.baseline) {
    sections.push(`# BASELINE TRANSCRIPT (no system prompt, no didactic tools)\n\n${args.baseline.markdown}`);
  }
  sections.push(`# EXPERIMENT TRANSCRIPT (under review)\n\n${args.experiment.markdown}`);
  sections.push(`# YOUR TASK\n\nGrade the EXPERIMENT against the rubric. Return JSON only.`);
  const basePrompt = sections.join('\n\n---\n\n');

  const tryOnce = async (prompt: string): Promise<{ grade: Grade | null; raw: string; parseError?: string }> => {
    const raw = await callGrader(prompt, opts);
    const cleaned = extractJson(raw);
    let parsed: unknown;
    try {
      parsed = JSON.parse(cleaned);
    } catch (e) {
      return { grade: null, raw, parseError: (e as Error).message };
    }
    return { grade: validateAndNormalize(parsed), raw };
  };

  const first = await tryOnce(basePrompt);
  if (first.grade) return { grade: first.grade, raw: first.raw };

  // Retry with stricter wording. The most common failures: omitting one
  // criterion, or inventing fields like `scaffolding_note`.
  const strictReminder = `\n\n# REMINDER (strict)\n\nReturn EXACTLY the schema shown — no extra keys (e.g. no \`scaffolding_note\`), no missing keys, all 4 pedagogical + 2 productivity criteria with numeric scores. JSON object only.`;
  const second = await tryOnce(basePrompt + strictReminder);
  if (second.grade) return { grade: second.grade, raw: second.raw };

  const why = first.parseError
    ? `JSON parse failed: ${first.parseError}`
    : `JSON parsed but missing/extra fields`;
  const preview = (second.raw || first.raw).slice(0, 400).replace(/\n/g, '\\n');
  throw new Error(`grader output unusable after 2 attempts (${why})\nRaw (first 400 chars): ${preview}`);
}
