// Eval driver. For each problem in the seed list, run a self-driving
// "user model ↔ pair model" conversation in an isolated working directory,
// stream every event into a JSONL transcript alongside any files the pair
// model writes, and stop when either side wraps up or we hit the turn cap.

import { cpSync, existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { Session } from '../core/Session.js';
import {
  FULL_PROPOSE_TOOL_NAME,
  pairMcpServer,
  proposeOptionsHandler,
  MCP_SERVER_NAME,
  type OptionsEvent,
} from '../pair/proposeOptions.js';
import { SYSTEM_PROMPT } from '../pair/systemPrompt.js';
import { renderTurn, type AnyEvent } from './render.js';
import { Transcript, type TranscriptRecord } from './transcript.js';
import { callUserModel, isDone, stripDone, DEFAULT_USER_MODEL, USER_SYSTEM_PROMPT } from './userModel.js';

const DEFAULT_PAIR_MODEL = 'claude-opus-4-7';
const DEFAULT_MAX_TURNS = 50;
// Reject a turn if no events arrive for this long. Prevents silent hangs
// if the SDK subprocess dies or the OS suspends the process.
const TURN_IDLE_TIMEOUT_MS = 5 * 60 * 1000;

type Problem = {
  slug: string;
  prompt: string;
  source?: string;
  difficulty?: 'easy' | 'medium' | 'hard';
};

type CliArgs = {
  problemsFile: string;
  outDir: string;
  pairModel: string;
  userModel: string;
  maxTurns: number;
  numProblems: number | null;
  only: string | null;
  tag: string | null;
  baseline: boolean;
  firstPerBucket: boolean;
};

function parseArgs(argv: string[]): CliArgs {
  const args: CliArgs = {
    problemsFile: 'eval-problems.json',
    outDir: '../eval-runs',
    pairModel: DEFAULT_PAIR_MODEL,
    userModel: DEFAULT_USER_MODEL,
    maxTurns: DEFAULT_MAX_TURNS,
    numProblems: null,
    only: null,
    tag: null,
    baseline: false,
    firstPerBucket: false,
  };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i]!;
    const next = () => argv[++i]!;
    if (a === '--problems') args.problemsFile = next();
    else if (a === '--out') args.outDir = next();
    else if (a === '--pair-model') args.pairModel = next();
    else if (a === '--user-model') args.userModel = next();
    else if (a === '--max-turns') args.maxTurns = Number(next());
    else if (a === '-n' || a === '--num') args.numProblems = Number(next());
    else if (a === '--baseline') args.baseline = true;
    else if (a === '--first-per-bucket') args.firstPerBucket = true;
    else if (a === '--only') args.only = next();
    else if (a === '--tag') args.tag = next();
    else if (a === '-h' || a === '--help') { printHelp(); process.exit(0); }
    else { console.error(`unknown arg: ${a}`); process.exit(2); }
  }
  return args;
}

function printHelp(): void {
  console.log(`Usage: bun src/eval/runEval.ts [options]

One invocation produces one collection directory under --out, with one
sub-directory per problem inside it. Layout:
  <out>/<timestamp>[-<tag>]/<slug>/transcript.jsonl

Options:
  --problems FILE      JSON list of {slug, prompt}. Default: eval-problems.json
  --out DIR            Output root for collections. Default: ../eval-runs
  --tag NAME           Suffix on the collection dir (e.g. "prompt-v2")
  --pair-model MODEL   Pair (responder) model. Default: ${DEFAULT_PAIR_MODEL}
  --user-model MODEL   User (asker) model. Default: ${DEFAULT_USER_MODEL}
  --max-turns N        Per-run turn cap. Default: ${DEFAULT_MAX_TURNS}
  -n, --num N          Run only the first N problems
  --only SLUG          Run only the problem matching this slug
  --baseline           Empty system prompt, no propose_options tool
                       (reference for productivity grading)
  --first-per-bucket   Pick the first problem from each (source,difficulty)
                       combo. With the canonical 4×3 problem set, yields 12.
`);
}

function timestamp(): string {
  const d = new Date();
  const pad = (n: number) => String(n).padStart(2, '0');
  return `${d.getFullYear()}${pad(d.getMonth() + 1)}${pad(d.getDate())}-${pad(d.getHours())}${pad(d.getMinutes())}${pad(d.getSeconds())}`;
}

/**
 * Wait until the Session emits a `result` event (or `error`). Returns the
 * full event list captured during the wait, in arrival order.
 */
function waitForTurn(
  session: Session<OptionsEvent>,
  onEvent: (ev: AnyEvent) => void,
): Promise<AnyEvent[]> {
  return new Promise((resolveTurn, rejectTurn) => {
    const captured: AnyEvent[] = [];
    let idleTimer: ReturnType<typeof setTimeout>;
    const armIdle = () => {
      clearTimeout(idleTimer);
      idleTimer = setTimeout(() => {
        rejectTurn(new Error(`turn idle for ${TURN_IDLE_TIMEOUT_MS / 1000}s — likely SDK hang`));
      }, TURN_IDLE_TIMEOUT_MS);
    };
    armIdle();
    session.onEvent((ev) => {
      const e = ev as AnyEvent;
      captured.push(e);
      onEvent(e);
      armIdle();
      if (e.kind === 'result') {
        clearTimeout(idleTimer);
        resolveTurn(captured);
      } else if (e.kind === 'error') {
        clearTimeout(idleTimer);
        rejectTurn(new Error(e.message));
      }
    });
  });
}

/**
 * Copy the contents of the sandbox cwd into the run dir for analysis, then
 * delete the sandbox. Skips noisy bookkeeping like __pycache__.
 */
function harvestSandbox(sandboxDir: string, runDir: string): void {
  try {
    cpSync(sandboxDir, runDir, {
      recursive: true,
      filter: (src) => !src.endsWith('__pycache__') && !src.endsWith('.pyc'),
    });
  } catch (e) {
    console.error(`  ! harvest failed: ${(e as Error).message}`);
  }
  try {
    rmSync(sandboxDir, { recursive: true, force: true });
  } catch {
    // Ignore — /tmp will get GC'd eventually.
  }
}


async function runOne(problem: Problem, collectionDir: string, args: CliArgs): Promise<void> {
  // Final destination for transcripts + copied artifacts.
  const runDir = resolve(join(collectionDir, problem.slug));
  mkdirSync(runDir, { recursive: true });
  const transcriptPath = join(runDir, 'transcript.jsonl');
  const transcript = new Transcript(transcriptPath);

  // Sandbox cwd in /tmp so the model can't pattern-match the project root and
  // start writing absolute paths into our repo. We saw Sonnet do this on
  // baseline runs (no system prompt → no "use relative paths" instruction):
  // it inferred /Users/oz/dev/ai-pair-proto/ as the project root from the cwd
  // and wrote files there, even editing tui/src/. /tmp has no such cues.
  const sandboxDir = mkdtempSync(join(tmpdir(), `ai-pair-eval-${problem.slug}-`));

  console.log(`\n▶ ${problem.slug} → ${runDir}  (sandbox: ${sandboxDir})`);

  const pairSystemPrompt = args.baseline ? '' : SYSTEM_PROMPT;
  transcript.write({
    kind: 'run_start',
    ts: Date.now(),
    problem,
    pairModel: args.pairModel,
    userModel: args.userModel,
    cwd: sandboxDir,
    pairSystemPrompt,
    userSystemPrompt: USER_SYSTEM_PROMPT,
  });
  const meta: string[] = [];
  if (problem.source) meta.push(`- Source: \`${problem.source}\``);
  if (problem.difficulty) meta.push(`- Difficulty: \`${problem.difficulty}\``);
  meta.push(`- Pair model: \`${args.pairModel}\``);
  meta.push(`- User model: \`${args.userModel}\``);
  meta.push(`- Started: ${new Date().toISOString()}`);
  transcript.writeHuman(
    `# ${problem.slug}\n\n` +
    meta.join('\n') + '\n\n' +
    `---\n\n`,
  );

  const session = new Session<OptionsEvent>({
    systemPrompt: pairSystemPrompt,
    mcpServers: args.baseline ? {} : { [MCP_SERVER_NAME]: pairMcpServer },
    // Include the MCP tool name in allowedTools when running the experiment;
    // without it the SDK whitelist hides the tool and Sonnet falls back to
    // inline markdown options, defeating the experiment.
    allowedTools: args.baseline
      ? ['Read', 'Glob', 'Grep', 'Edit', 'Write', 'Bash']
      : ['Read', 'Glob', 'Grep', 'Edit', 'Write', 'Bash', FULL_PROPOSE_TOOL_NAME],
    // Keep PairApp and the eval in lockstep — see PairApp.tsx for why.
    disallowedTools: ['AskUserQuestion'],
    customToolHandlers: args.baseline ? {} : { [FULL_PROPOSE_TOOL_NAME]: proposeOptionsHandler },
    cwd: sandboxDir,
    model: args.pairModel,
  });
  session.start();

  // Cumulative transcript text the user model sees.
  let conversation = `Problem: ${problem.prompt}\n`;

  // First user message — the problem prompt itself.
  let nextUserMsg: string = problem.prompt;
  let turn = 0;
  let endReason: 'done' | 'max_turns' | 'error' = 'max_turns';
  const startedAt = Date.now();

  try {
    while (turn < args.maxTurns) {
      turn++;
      transcript.write({ kind: 'user_message', ts: Date.now(), turn, text: nextUserMsg });
      conversation += `\nUser: ${nextUserMsg}\n`;
      transcript.writeHuman(
        `## Turn ${turn}\n\n` +
        `**User:**\n\n${nextUserMsg.trim()}\n\n` +
        `**Pair:**\n\n`,
      );

      const turnEventsPromise = waitForTurn(session, (ev) => {
        const rec: TranscriptRecord = ev.kind === 'options' && ev.privateNotes
          ? { kind: 'pair_event_with_notes', ts: Date.now(), turn, event: ev, privateNotes: ev.privateNotes }
          : { kind: 'pair_event', ts: Date.now(), turn, event: ev };
        transcript.write(rec);
      });

      session.send(nextUserMsg);
      const events = await turnEventsPromise;

      const rendered = renderTurn(events);
      transcript.write({ kind: 'turn_summary', ts: Date.now(), turn, rendered });
      conversation += '\n' + rendered + '\n';
      transcript.writeHuman(`${rendered}\n\n---\n\n`);

      // User model's turn.
      const userReply = await callUserModel(conversation, { model: args.userModel });
      const done = isDone(userReply);
      const cleanReply = stripDone(userReply);

      if (done) {
        // Record the final reply but don't send it back to the pair.
        transcript.write({ kind: 'user_message', ts: Date.now(), turn: turn + 1, text: userReply });
        transcript.writeHuman(
          `## Turn ${turn + 1} (final)\n\n` +
          `**User:**\n\n${userReply.trim()}\n\n` +
          `---\n\n`,
        );
        endReason = 'done';
        break;
      }
      if (!cleanReply) {
        // Empty reply — treat as done to avoid spinning.
        endReason = 'done';
        break;
      }
      nextUserMsg = cleanReply;
    }
  } catch (e) {
    const err = e as Error;
    endReason = 'error';
    transcript.write({
      kind: 'run_end',
      ts: Date.now(),
      reason: 'error',
      turns: turn,
      durationMs: Date.now() - startedAt,
      error: err.message,
    });
    transcript.writeHuman(`**Run end**: error after ${turn} turns — ${err.message}\n`);
    session.close();
    harvestSandbox(sandboxDir, runDir);
    console.log(`  ✗ error after ${turn} turns: ${err.message}`);
    return;
  }

  const elapsedSec = Math.round((Date.now() - startedAt) / 1000);
  transcript.write({
    kind: 'run_end',
    ts: Date.now(),
    reason: endReason,
    turns: turn,
    durationMs: Date.now() - startedAt,
  });
  transcript.writeHuman(`**Run end**: ${endReason} after ${turn} turn${turn === 1 ? '' : 's'} (${elapsedSec}s)\n`);
  session.close();
  harvestSandbox(sandboxDir, runDir);
  console.log(`  ✓ ${endReason} after ${turn} turns (${elapsedSec}s)`);
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (!existsSync(args.problemsFile)) {
    console.error(`problems file not found: ${args.problemsFile}`);
    process.exit(1);
  }
  let problems: Problem[] = JSON.parse(readFileSync(args.problemsFile, 'utf8'));
  if (args.only) {
    problems = problems.filter((p) => p.slug === args.only);
    if (problems.length === 0) {
      console.error(`no problem with slug "${args.only}"`);
      process.exit(1);
    }
  }
  if (args.firstPerBucket) {
    // Group by (source, difficulty) preserving file order, then pick the
    // first member of each bucket. Problems missing source/difficulty get
    // their own buckets keyed by `?`.
    const seen = new Set<string>();
    const picked: Problem[] = [];
    for (const p of problems) {
      const key = `${p.source ?? '?'}/${p.difficulty ?? '?'}`;
      if (seen.has(key)) continue;
      seen.add(key);
      picked.push(p);
    }
    problems = picked;
  }
  if (args.numProblems !== null) problems = problems.slice(0, args.numProblems);

  const collectionName = args.tag ?? timestamp();
  const collectionDir = resolve(join(args.outDir, collectionName));
  mkdirSync(collectionDir, { recursive: true });

  console.log(`Eval: ${problems.length} problem(s), pair=${args.pairModel}, user=${args.userModel}, max-turns=${args.maxTurns}`);
  console.log(`Collection: ${collectionDir}`);

  for (const p of problems) {
    await runOne(p, collectionDir, args);
  }
  console.log('\nDone.');
}

main()
  .then(() => {
    // SDK subprocesses can keep the event loop alive past main()'s return,
    // which prevents shell `&&` chains from advancing. Force exit.
    process.exit(0);
  })
  .catch((e) => {
    console.error(e);
    process.exit(1);
  });
