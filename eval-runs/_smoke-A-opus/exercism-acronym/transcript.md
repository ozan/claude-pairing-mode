# exercism-acronym

- Source: `exercism`
- Difficulty: `medium`
- Pair model: `claude-opus-4-7`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T02:34:31.663Z

---

## Turn 1

**User:**

Exercism 'Acronym': given a phrase, return its acronym in uppercase. Treat hyphens as word separators; ignore other punctuation. e.g. 'Portable Network Graphics' → 'PNG'.

**Pair:**

Assistant: The pairing tool isn't available in this session — I'll just proceed directly. Here's the natural one-liner:

[Write(acronym.py)]
def abbreviate(words: str) -> str:
    return ''.join(w[0].upper() for w in words.replace('-', ' ').split())


Assistant: Quick test against the tricky cases:

[Bash(python3 -c "
from acronym import abbreviate
cases = [
    ('Portable Network Graphics', 'PNG'),
    ('Ruby on Rails', 'ROR'),
    ('First In, First Out', 'FIFO'),
    ('Complementary metal-oxide semiconductor', 'CMOS'),
    (\"Halley's Comet\", 'HC'),
    ('the quick brown fox', 'TQBF'),
]
for phrase, expected in cases:
    got = abbreviate(phrase)
    print(f'{got==expected}  {phrase!r:55} -> {got} (expected {expected})')
"
)]
  True  'Portable Network Graphics'                             -> PNG (expected PNG)
  True  'Ruby on Rails'                                         -> ROR (expected ROR)
  True  'First In, First Out'                                   -> FIFO (expected FIFO)
  True  'Complementary metal-oxide semiconductor'               -> CMOS (expected CMOS)
  True  "Halley's Comet"                                        -> HC (expected HC)
  True  'the quick brown fox'                                   -> TQBF (expected TQBF)

Assistant: All green. Worth noting why this works on the sneaky one — **"Halley's Comet" → "HC"**:

`split()` keeps `Halley's` as one token (apostrophe is just an interior character), so we grab `H`. A common wrong turn here is `re.findall(r'\w+', words)` — `\w` doesn't include `'`, so it splits `Halley's` into `['Halley', 's']` and you get `HCS`. The `replace('-', ' ').split()` approach sidesteps the whole question of "which punctuation counts" by only deciding what's a *separator* (whitespace + hyphen) and letting everything else ride along inside the word. The first letter is alphabetic regardless.

---

## Turn 2 (final)

**User:**

Oh nice, I see it now. The key insight is that we're only saying "hyphens are separators" — everything else (including apostrophes) just stays inside its word. When we take the first character of each word after splitting on whitespace + hyphens, we naturally get the right letter whether it's `H` from `Halley's` or just the plain letter if punctuation had split it. That's much cleaner than trying to enumerate all the punctuation to ignore.

And the tests confirm it handles the edge cases properly. The solution is solid.

<done/>

---

**Run end**: done after 1 turn (39s)
