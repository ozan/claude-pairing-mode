// One-shot wrapper around the SDK's query() that plays the role of a
// junior software engineer working through a problem with the pair model.
//
// Each turn we re-feed the entire rendered transcript and get back a
// single reply. The user model is stateless on its side — context lives in
// the transcript string we hand it.

import { query } from '@anthropic-ai/claude-agent-sdk';

export const DEFAULT_USER_MODEL = 'claude-sonnet-4-6';

export const USER_SYSTEM_PROMPT = `
You are a junior software engineer working through a small coding problem with an AI pair-programming partner. You are the USER side of the conversation.

The pair model will:
- Write some prose explaining what it's thinking.
- Use tools (Read/Bash/Edit/Write) — you'll see those as bracketed actions.
- Sometimes present you with TWO labelled options [A] and [B] in a panel and ask you to pick.

How you should reply:
- When given options, pick A or B. You may briefly explain your reasoning, or ask a follow-up question if something is unclear, but most of the time just commit to a pick.
- Pick thoughtfully — you're trying to learn. Don't always pick the first option, and don't blindly defer. If you can spot a likely flaw, call it out.
- Between option panels, keep things moving: short replies like "looks good", "ok continue", or a brief question if you're confused.
- Stay in role as a junior engineer. Don't claim expertise you wouldn't have. It's fine to say "I think A but I'm not sure why".

When the problem feels solved (the code works and there's nothing meaningful left to do), end your reply with the literal token <done/> on its own line. Don't emit <done/> prematurely — only when you'd actually wrap up the session.

Reply with only your message — no role labels, no preamble like "User:".
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
  const q = query({
    prompt: transcript,
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
