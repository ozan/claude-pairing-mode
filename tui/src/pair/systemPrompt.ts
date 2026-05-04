// The pair-programming system prompt is shared with the Python eval at
// ../../../pairing_prompt.md so both surfaces register the exact same
// behavior with the model. Bun's `with { type: 'text' }` import attribute
// loads the markdown file as a string at compile time.

import promptText from '../../../pairing_prompt.md' with { type: 'text' };

export const SYSTEM_PROMPT = promptText.trim();
