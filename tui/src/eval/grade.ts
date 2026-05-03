// Grade an experiment collection. For each <slug>/transcript.md in the
// experiment dir, optionally pair with the matching baseline by slug, send
// both to Opus, write grade.json next to the transcript.
//
// Usage:
//   bun run src/eval/grade.ts <experiment-collection> [--baseline <baseline-collection>]
//                            [--grader-model claude-opus-4-7] [--only <slug>]

import { existsSync, readFileSync, readdirSync, statSync, writeFileSync } from 'node:fs';
import { join, resolve, basename } from 'node:path';
import { gradeTranscript, DEFAULT_GRADER_MODEL, weightedScore, normalizedScore, type Grade } from './grader.js';

type CliArgs = {
  experimentDir: string;
  baselineDir: string | null;
  graderModel: string;
  only: string | null;
  force: boolean;
};

function parseArgs(argv: string[]): CliArgs {
  const args: CliArgs = {
    experimentDir: '',
    baselineDir: null,
    graderModel: DEFAULT_GRADER_MODEL,
    only: null,
    force: false,
  };
  const positional: string[] = [];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i]!;
    const next = () => argv[++i]!;
    if (a === '--baseline') args.baselineDir = next();
    else if (a === '--grader-model') args.graderModel = next();
    else if (a === '--only') args.only = next();
    else if (a === '--force' || a === '-f') args.force = true;
    else if (a === '-h' || a === '--help') { printHelp(); process.exit(0); }
    else if (a.startsWith('-')) { console.error(`unknown arg: ${a}`); process.exit(2); }
    else positional.push(a);
  }
  if (positional.length !== 1) {
    printHelp();
    process.exit(2);
  }
  args.experimentDir = positional[0]!;
  return args;
}

function printHelp(): void {
  console.log(`Usage: bun src/eval/grade.ts <experiment-collection> [options]

Walks each <slug>/transcript.md in the experiment collection, sends it to
Opus with the rubric, writes grade.json next to it.

Options:
  --baseline DIR        Baseline collection (matched by slug). Without it,
                        productivity criteria are scored in absolute terms.
  --grader-model MODEL  Default: ${DEFAULT_GRADER_MODEL}
  --only SLUG           Grade only the run matching this slug.
  -f, --force           Re-grade runs that already have grade.json.
`);
}

type RunDir = { slug: string; dir: string; transcript: string; isBaseline: boolean };

/**
 * Inspect a run's transcript.jsonl run_start record to determine whether
 * the pair model was running in baseline mode (empty system prompt). Used
 * by the grader to mechanically pin productivity scores to 3 for baselines
 * — they're the reference, so judging them comparatively makes no sense.
 */
function isBaselineRun(runDir: string): boolean {
  const jsonl = join(runDir, 'transcript.jsonl');
  if (!existsSync(jsonl)) return false;
  try {
    const firstLine = readFileSync(jsonl, 'utf8').split('\n', 1)[0] ?? '';
    const rec = JSON.parse(firstLine) as { kind?: string; pairSystemPrompt?: string };
    return rec.kind === 'run_start' && (rec.pairSystemPrompt ?? '') === '';
  } catch {
    return false;
  }
}

function findRuns(collectionDir: string): RunDir[] {
  if (!existsSync(collectionDir) || !statSync(collectionDir).isDirectory()) {
    console.error(`not a directory: ${collectionDir}`);
    process.exit(1);
  }
  const out: RunDir[] = [];
  for (const name of readdirSync(collectionDir)) {
    const dir = join(collectionDir, name);
    const md = join(dir, 'transcript.md');
    if (statSync(dir).isDirectory() && existsSync(md)) {
      out.push({ slug: name, dir, transcript: md, isBaseline: isBaselineRun(dir) });
    }
  }
  out.sort((a, b) => a.slug.localeCompare(b.slug));
  return out;
}

const BASELINE_NEUTRAL_SCORE = 3;
const BASELINE_NEUTRAL_RATIONALE =
  'Baseline run — productivity criteria pinned to 3 by convention (the baseline IS the reference; judging it comparatively is meaningless).';

/**
 * For baseline runs, replace effectiveness/friction with neutral 3 — the
 * LLM may have generated noise here that we want to ignore. Pedagogical
 * scores are kept; the rubric is meaningful for baselines too.
 */
function applyBaselineOverride(grade: Grade): Grade {
  return {
    pedagogical: grade.pedagogical,
    productivity: {
      effectiveness: { score: BASELINE_NEUTRAL_SCORE, rationale: BASELINE_NEUTRAL_RATIONALE },
      friction: { score: BASELINE_NEUTRAL_SCORE, rationale: BASELINE_NEUTRAL_RATIONALE },
    },
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const expDir = resolve(args.experimentDir);
  const baseDir = args.baselineDir ? resolve(args.baselineDir) : null;

  let experiments = findRuns(expDir);
  if (args.only) experiments = experiments.filter((r) => r.slug === args.only);
  if (experiments.length === 0) {
    console.error(`no transcripts to grade in ${expDir}${args.only ? ` matching slug "${args.only}"` : ''}`);
    process.exit(1);
  }

  // Build slug → transcript path lookup for the baseline collection.
  const baselineBySlug = new Map<string, string>();
  if (baseDir) {
    for (const r of findRuns(baseDir)) baselineBySlug.set(r.slug, r.transcript);
  }

  console.log(`Grading ${experiments.length} run(s) in ${basename(expDir)} via ${args.graderModel}${baseDir ? `, baseline=${basename(baseDir)}` : ' (no baseline)'}\n`);

  let graded = 0;
  let skipped = 0;
  for (const r of experiments) {
    const gradePath = join(r.dir, 'grade.json');
    if (existsSync(gradePath) && !args.force) {
      console.log(`  ⊘ ${r.slug} (already graded; pass -f to re-grade)`);
      skipped++;
      continue;
    }
    const expMd = readFileSync(r.transcript, 'utf8');
    const baseMdPath = baselineBySlug.get(r.slug);
    const baseMd = baseMdPath ? readFileSync(baseMdPath, 'utf8') : null;

    const start = Date.now();
    try {
      const { grade: rawGrade } = await gradeTranscript({
        experiment: { slug: r.slug, markdown: expMd },
        baseline: baseMd ? { slug: r.slug, markdown: baseMd } : undefined,
        opts: { model: args.graderModel },
      });
      const grade = r.isBaseline ? applyBaselineOverride(rawGrade) : rawGrade;
      const weighted = weightedScore(grade);
      const final = normalizedScore(grade);
      const out = {
        ts: Date.now(),
        graderModel: args.graderModel,
        experimentSlug: r.slug,
        isBaseline: r.isBaseline,
        baselineCollection: baseDir ? basename(baseDir) : null,
        weightedScore: Number(weighted.toFixed(3)),
        finalScore: Number(final.toFixed(3)),
        ...grade,
      };
      writeFileSync(gradePath, JSON.stringify(out, null, 2) + '\n');
      const elapsed = Math.round((Date.now() - start) / 1000);
      const peds = Object.values(grade.pedagogical).map((c) => c.score);
      const prods = Object.values(grade.productivity).map((c) => c.score);
      const avg = (xs: number[]) => xs.reduce((a, b) => a + b, 0) / xs.length;
      const tag = r.isBaseline ? '[base]' : '      ';
      console.log(`  ✓ ${tag} ${r.slug} (${elapsed}s)  ped=${avg(peds).toFixed(1)} prod=${avg(prods).toFixed(1)} weighted=${weighted.toFixed(2)} final=${final.toFixed(2)}`);
      graded++;
    } catch (e) {
      const err = e as Error;
      console.log(`  ✗ ${r.slug}: ${err.message}`);
    }
  }

  console.log(`\nDone: ${graded} graded, ${skipped} skipped.`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
