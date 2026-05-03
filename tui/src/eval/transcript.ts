// Transcript writer. Each run gets two files in its dir:
//   - transcript.jsonl: machine-readable record stream (one event per line)
//   - transcript.md:    human-readable rendering (alternating user/pair)
//
// JSONL records are union-typed so post-hoc scripts can filter by `kind`
// without re-parsing the rendered text. The .md is generated incrementally
// by the runner via writeHuman().

import { appendFileSync, writeFileSync } from 'node:fs';
import type { AnyEvent } from './render.js';

export type TranscriptRecord =
  | { kind: 'run_start'; ts: number; problem: { slug: string; prompt: string; source?: string; difficulty?: 'easy' | 'medium' | 'hard' }; pairModel: string; userModel: string; cwd: string; pairSystemPrompt: string; userSystemPrompt: string }
  | { kind: 'user_message'; ts: number; turn: number; text: string }
  | { kind: 'pair_event'; ts: number; turn: number; event: AnyEvent }
  | { kind: 'pair_event_with_notes'; ts: number; turn: number; event: AnyEvent; privateNotes: unknown }
  | { kind: 'turn_summary'; ts: number; turn: number; rendered: string }
  | { kind: 'run_end'; ts: number; reason: 'done' | 'max_turns' | 'error'; turns: number; durationMs: number; error?: string };

export class Transcript {
  private mdPath: string;

  constructor(private path: string) {
    this.mdPath = path.replace(/\.jsonl$/, '.md');
    writeFileSync(path, '');
    writeFileSync(this.mdPath, '');
  }

  write(rec: TranscriptRecord): void {
    appendFileSync(this.path, JSON.stringify(rec) + '\n');
  }

  /** Append a chunk of markdown to transcript.md. */
  writeHuman(s: string): void {
    appendFileSync(this.mdPath, s);
  }
}
