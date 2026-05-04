import type { Solver } from "./solvers/types";
import { solver as p001 } from "./solvers/problem_001";

// ── Registry: add new solvers here as you go ─────────────────────────────────
const solvers: Solver[] = [p001];

// ── Run one problem (bun run runner.ts 1) or all (bun run runner.ts) ─────────
const arg = process.argv[2];
const target = arg ? parseInt(arg, 10) : null;

for (const s of solvers) {
  if (target !== null && s.problem !== target) continue;
  console.log(`\nProblem ${String(s.problem).padStart(3, "0")}: ${s.title}`);
  const answer = s.solve();
  console.log(`  answer       → ${answer}`);
}
