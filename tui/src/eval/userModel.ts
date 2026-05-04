// One-shot wrapper around the SDK's query() that plays the role of a
// junior software engineer working through a problem with the pair model.
//
// Each turn we re-feed the entire rendered transcript and get back a
// single reply. The user model is stateless on its side — context lives in
// the transcript string we hand it.

import { query } from '@anthropic-ai/claude-agent-sdk';

export const DEFAULT_USER_MODEL = 'claude-sonnet-4-6';

export const USER_SYSTEM_PROMPT = `
You are a junior software engineer working through a small coding problem with an AI pair-programming partner. You would like to solve the problem but also learn along the way.

You are the USER role in this conversation; the pair is the assistant. Write only your own next reply — never write the pair's response, never narrate in the second person ("you should…"), never use the pair's voice ("I'll walk you through it…"). Stay in your own voice as the junior engineer asking and learning.

Stay focused on the original problem stated at the start of the session. If the pair offers to extend, generalize, or move on to a different problem, politely decline and wrap up — your goal is to solve the one problem you were given, not to start new work.

When the problem feels solved (the code works and there's nothing meaningful left to do), end your reply with the literal token <done/> on its own line. Don't emit <done/> prematurely — only when you'd actually wrap up the session.
`.trim();


export type UserModelOptions = {
  /** SDK model id, e.g. "claude-sonnet-4-5" or "claude-opus-4-7". */
  model?: string;
  /** Override the default system prompt (e.g. for persona experiments). */
  systemPrompt?: string;
};

/**
 * Run a single user-model turn. `transcript` is the full conversation as
 * rendered by render.ts plus any prior user replies, terminated by the
 * latest pair-model output. Returns the user's reply text.
 */
export async function callUserModel(
  transcript: string,
  opts: UserModelOptions = {},
): Promise<string> {
  // Append a terminal "User:" cue to disambiguate which role is next.
  // Without this the model can pattern-match the pair's voice when the
  // pair's last message ends with assistant-shaped phrasing like "Pick A
  // or B and I'll walk you through it." We saw this happen in real runs.
  const cued = transcript.replace(/\s+$/, '') + '\n\nUser: ';

  const q = query({
    prompt: cued,
    options: {
      model: opts.model ?? DEFAULT_USER_MODEL,
      systemPrompt: opts.systemPrompt ?? USER_SYSTEM_PROMPT,
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
  return text.trim();
}

/** True if reply contains the <done/> sentinel on its own. */
export function isDone(reply: string): boolean {
  return /(^|\n)\s*<done\s*\/?>\s*(\n|$)/.test(reply);
}

/** Strip the <done/> sentinel for the version we send back to the pair. */
export function stripDone(reply: string): string {
  return reply.replace(/(^|\n)\s*<done\s*\/?>\s*(\n|$)/g, '$1').trim();
}
