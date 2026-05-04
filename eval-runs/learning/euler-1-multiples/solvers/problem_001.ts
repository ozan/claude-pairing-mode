import type { Solver } from "./types";

// ── Approach 1: brute-force loop ─────────────────────────────────────────────
// Check every integer below the limit. Simple, obvious, O(n).
function bruteForce(limit: number): number {
  let sum = 0;
  for (let i = 1; i < limit; i++) {
    if (i % 3 === 0 || i % 5 === 0) sum += i;
  }
  return sum;
}

// ── Approach 2: closed-form via inclusion-exclusion ──────────────────────────
// Multiples of k below `limit` form an arithmetic series: k, 2k, …, p·k
// where p = ⌊(limit-1)/k⌋.  Their sum = k · p(p+1)/2  (triangular number).
// By inclusion-exclusion: |mult3 ∪ mult5| = |mult3| + |mult5| − |mult15|
function sumOfMultiples(k: number, limit: number): number {
  const p = Math.floor((limit - 1) / k);
  return k * (p * (p + 1)) / 2;
}

function closedForm(limit: number): number {
  return (
    sumOfMultiples(3, limit) +
    sumOfMultiples(5, limit) -
    sumOfMultiples(15, limit) // LCM(3,5) — subtract the double-counted overlap
  );
}

// ── Solver entry point ───────────────────────────────────────────────────────
export const solver: Solver = {
  problem: 1,
  title: "Multiples of 3 or 5",
  solve() {
    const limit = 1000;
    const a = bruteForce(limit);
    const b = closedForm(limit);
    console.log(`  brute-force  → ${a}`);
    console.log(`  closed-form  → ${b}`);
    return b;
  },
};
