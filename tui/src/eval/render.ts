// Renders the pair-model event stream as a clean text view for the user
// model. Mirrors what a human sees in the TUI but without ANSI / spinners /
// tool plumbing — just prose, tool actions and outcomes, and the A/B
// options panel when the pair calls propose_options.
//
// The renderer is *cumulative* per turn: pass it the events from one
// pair-model turn (everything between two `result` events) and it returns
// the chunk to append to the transcript.

import { type CoreAgentEvent } from '../core/types.js';
import { type OptionsEvent } from '../pair/proposeOptions.js';

export type AnyEvent = CoreAgentEvent | OptionsEvent;

type ToolRecord = { name: string; input: unknown };

const MAX_TOOL_OUTPUT_LINES = 12;

function truncateLines(text: string, max: number): string {
  const lines = text.split('\n');
  if (lines.length <= max) return text;
  return lines.slice(0, max).join('\n') + `\n… (${lines.length - max} more lines)`;
}

function summarizeInput(name: string, input: unknown): string {
  const i = (input ?? {}) as Record<string, unknown>;
  if (name === 'Bash') return String(i.command ?? '');
  if (name === 'Read' || name === 'Edit' || name === 'Write') return String(i.file_path ?? '');
  if (name === 'Glob') return String(i.pattern ?? '');
  if (name === 'Grep') return String(i.pattern ?? '');
  // Fallback: short JSON.
  try {
    const s = JSON.stringify(input);
    return s.length > 80 ? s.slice(0, 77) + '...' : s;
  } catch {
    return '';
  }
}

function renderToolBlock(rec: ToolRecord, result: { text: string; isError: boolean } | null): string {
  const arg = summarizeInput(rec.name, rec.input);
  const head = arg ? `[${rec.name}(${arg})]` : `[${rec.name}]`;

  // For Edit/Write the diff IS the user-visible content; show old→new.
  if (rec.name === 'Edit' || rec.name === 'Write') {
    const i = (rec.input ?? {}) as Record<string, unknown>;
    if (rec.name === 'Edit') {
      const oldStr = String(i.old_string ?? '');
      const newStr = String(i.new_string ?? '');
      return `${head}\n--- before\n${oldStr}\n--- after\n${newStr}`;
    } else {
      const content = String(i.content ?? '');
      return `${head}\n${truncateLines(content, MAX_TOOL_OUTPUT_LINES)}`;
    }
  }

  if (!result) return head;
  if (result.isError) return `${head}\n  error: ${result.text.split('\n')[0]}`;
  const text = result.text.trim();
  if (!text) return `${head}\n  (no output)`;
  return `${head}\n${truncateLines(text, MAX_TOOL_OUTPUT_LINES)
    .split('\n').map((l) => '  ' + l).join('\n')}`;
}

function renderOptions(ev: OptionsEvent): string {
  const [a, b] = ev.options;
  return [
    'OPTIONS:',
    `[A] ${a!.title}`,
    a!.body.trim(),
    '',
    `[B] ${b!.title}`,
    b!.body.trim(),
    '',
    '(Reply with A or B, or ask a follow-up question.)',
  ].join('\n');
}

/**
 * Render one pair-model turn's events as a text chunk. The chunk reads as
 * a transcript fragment ("Assistant: ...\n[Tool: ...]\n...").
 *
 * `events` should contain everything from `message_start` of the model's
 * reply up to and including the `result` (or end of stream). Filter
 * `text_delta`/`text_block_done` happen here; the caller doesn't have to
 * pre-aggregate.
 *
 * `forUser=true` strips content the user-model shouldn't see: the pair's
 * private thinking blocks (which would include the pair's preferred
 * answer to a propose_options decision, biasing the user's "choice").
 * Use `forUser=false` for the human-readable transcript.md.
 */
export function renderTurn(events: AnyEvent[], opts: { forUser?: boolean } = {}): string {
  const forUser = opts.forUser ?? false;
  const lines: string[] = [];
  const tools = new Map<string, ToolRecord>();
  let curText = '';

  const flushText = () => {
    if (curText.trim()) {
      lines.push('Assistant: ' + curText.trim());
      lines.push('');
    }
    curText = '';
  };

  for (const ev of events) {
    switch (ev.kind) {
      case 'text_delta':
        curText += ev.text;
        break;
      case 'text_block_done':
        flushText();
        break;
      case 'thinking_block_done':
        flushText();
        // Render thinking as a marked block so it's visually distinct from
        // assistant prose. Useful for debugging tool-use decisions; ignore
        // when reading the conversation casually. When forUser=true, skip
        // entirely — Sonnet's thinking often states its preferred option
        // and the user-model would metagame from it.
        if (!forUser && ev.text.trim()) {
          lines.push('Thinking: ' + ev.text.trim().split('\n').join('\n  '));
          lines.push('');
        }
        break;
      case 'tool_use_start':
        flushText();
        tools.set(ev.id, { name: ev.name, input: ev.input });
        break;
      case 'tool_use_done': {
        const rec = tools.get(ev.id);
        if (rec) tools.set(ev.id, { ...rec, input: ev.input });
        break;
      }
      case 'tool_result': {
        flushText();
        const rec = tools.get(ev.toolUseId) ?? { name: ev.name, input: {} };
        lines.push(renderToolBlock(rec, { text: ev.text, isError: ev.isError }));
        lines.push('');
        break;
      }
      case 'options':
        flushText();
        lines.push(renderOptions(ev));
        lines.push('');
        break;
      case 'error':
        flushText();
        lines.push(`[error: ${ev.message}]`);
        lines.push('');
        break;
      case 'result':
        flushText();
        break;
    }
  }
  flushText();

  return lines.join('\n').trim();
}
