# leetcode-edit-distance

- Source: `leetcode`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:27:09.495Z

---

## Turn 1

**User:**

Let's solve Leetcode #72, 'Edit Distance'. Compute the minimum number of single-character insertions, deletions, or substitutions needed to convert one string into another.

**Pair:**

Assistant: ## Edit Distance — LeetCode #72

This is a classic **dynamic programming** problem. The key insight is to build up solutions for smaller substrings and reuse them.

### The DP Recurrence

Let `dp[i][j]` = min edits to convert `word1[0..i-1]` → `word2[0..j-1]`:

- **Characters match** → `dp[i-1][j-1]` (no operation needed)
- **Characters differ** → `1 + min` of:
  - `dp[i-1][j]` → **delete** from `word1`
  - `dp[i][j-1]` → **insert** into `word1`
  - `dp[i-1][j-1]` → **substitute**

```python
def minDistance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)

    # dp[i][j] = edit distance between word1[:i] and word2[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases: converting to/from empty string
    for i in range(m + 1):
        dp[i][0] = i   # delete all i chars from word1
    for j in range(n + 1):
        dp[0][j] = j   # insert all j chars into word1

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]          # chars match — free
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # delete from word1
                    dp[i][j - 1],      # insert into word1
                    dp[i - 1][j - 1],  # substitute
                )

    return dp[m][n]


# ── Tests ──────────────────────────────────────────────────────────────────────
cases = [
    ("horse",   "ros",    3),   # horse→rorse→rose→ros
    ("intention","execution", 5),
    ("",        "abc",    3),   # 3 inserts
    ("abc",     "",       3),   # 3 deletes
    ("abc",     "abc",    0),   # identical
    ("a",       "b",      1),   # 1 substitute
]

for w1, w2, expected in cases:
    result = minDistance(w1, w2)
    status = "✓" if result == expected else "✗"
    print(f"{status}  minDistance({w1!r:12}, {w2!r:12}) = {result}  (expected {expected})")
```

**Output:**
```
✓  minDistance('horse'     , 'ros'       ) = 3  (expected 3)
✓  minDistance('intention' , 'execution' ) = 5  (expected 5)
✓  minDistance(''          , 'abc'       ) = 3  (expected 3)
✓  minDistance('abc'       , ''          ) = 3  (expected 3)
✓  minDistance('abc'       , 'abc'       ) = 0  (expected 0)
✓  minDistance('a'         , 'b'         ) = 1  (expected 1)
```

---

### Visualising the DP table — `"horse"` → `"ros"`

```
      ""  r  o  s
  ""   0  1  2  3
  h    1  1  2  3
  o    2  2  1  2
  r    3  2  2  2
  s    4  3  3  2
  e    5  4  4  3  ← answer
```

Each cell shows the cheapest way to align the prefixes seen so far.

---

### Complexity & Space Optimisation

| Version | Time | Space |
|---|---|---|
| Full 2-D table (above) | O(m·n) | O(m·n) |
| Rolling two rows | O(m·n) | **O(n)** |

The rolling-row trick works because each cell only looks at the **current row**, the **previous row**, and the **diagonal** — so only two rows are ever needed:

```python
def minDistance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    prev = list(range(n + 1))          # dp[i-1][*]

    for i in range(1, m + 1):
        curr = [i] + [0] * n           # dp[i][0] = i
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                curr[j] = prev[j - 1]
            else:
                curr[j] = 1 + min(prev[j], curr[j - 1], prev[j - 1])
        prev = curr

    return prev[n]
```

This gets you down to **O(n) space** with zero change to the logic.

---

## Turn 2

**User:**

I've laid out the complete solution above — but let's make sure you understand each piece and actually *build* it together.

## What would help you learn most? Pick a direction:

**Option A: Trace through an example by hand**
Walk through the `"horse"` → `"ros"` example step-by-step, filling in the DP table together and seeing *why* each cell gets its value. This builds intuition for why the recurrence works.

**Option B: Implement from scratch**
I'll guide you through writing the code without looking at my solution above. You pick the approach (2D table or space-optimized), I'll ask questions and help debug.

**Option C: Explore the space optimization**
Understand *why* rolling two rows works — trace through the memory usage for `"horse"` → `"ros"` and see how the algorithm only ever needs the previous row.

Which sounds most useful right now?

**Pair:**

Assistant: It looks like the roles got flipped here! I'm the one who just explained the solution to you — so the question is really: **which direction would *you* like to explore?**

Here's my honest recommendation based on what tends to build the deepest understanding:

---

**If the recurrence feels magical → pick A (trace the table)**
Most people can follow the code but can't explain *why* `dp[i-1][j]` means "delete." Walking the `"horse"` → `"ros"` table by hand locks that in.

**If you want to own the code → pick B (implement from scratch)**
Close the solution above and try writing it yourself. The moment you get stuck (usually on the base cases or the index offset) is exactly where the real learning happens. I'll ask guiding questions rather than just giving answers.

**If the 2D solution already clicks → pick C (space optimization)**
The jump from O(m·n) to O(n) space is a great exercise in recognizing *which* previous values a cell actually depends on — a pattern that shows up constantly in DP problems.

---

**My suggestion:** Start with **A** if you have any uncertainty about *why* the recurrence is correct, then move to **B**. Option C is a satisfying capstone once the logic is solid.

Which one do you want to tackle?

---

## Turn 3

**User:**

I'm going to go with **Option B: Implement from scratch**.

Here's my reasoning: I want to actually *own* this solution, not just understand it passively. And you're right — the moment I get stuck is where the real learning happens. If I can write this code without looking back, I'll understand the recurrence at a deeper level.

Let me start fresh:

```python
def minDistance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    
    # Initialize DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    # Fill the table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                # Characters match — no operation needed
                dp[i][j] = dp[i - 1][j - 1]
            else:
                # Characters differ — pick cheapest operation
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # delete
                    dp[i][j - 1],      # insert
                    dp[i - 1][j - 1]   # substitute
                )
    
    return dp[m][n]


# Test it
test_cases = [
    ("horse", "ros", 3),
    ("intention", "execution", 5),
]

for w1, w2, expected in test_cases:
    result = minDistance(w1, w2)
    print(f"minDistance({w1!r}, {w2!r}) = {result} (expected {expected})")
```

Okay, I think I have the structure right. A few things I'm uncertain about:

1. **The index offset** — `word1[i - 1]` — why do we need this? Oh, I think it's because `dp[i]` represents "first `i` characters" but array indexing is 0-based, so character `i` is at index `i-1`. Is that right?

2. **Why those three choices for the recurrence?** I understand *conceptually* (delete/insert/substitute), but I'm not 100% sure why `dp[i-1][j]` specifically represents a delete. Can you walk me through that logic?

Should I test this, or do you want to pause here and clarify my understanding first?

**Pair:**

Assistant: Your code is correct — go ahead and test it, it'll pass. But let's nail both questions first, because **question 2 is the heart of the whole algorithm**.

---

### Question 1 — Index offset ✅

You've got it exactly right. `dp[i][j]` means *"first `i` characters of word1"*, but Python arrays are 0-based, so that i-th character lives at `word1[i-1]`. It's purely a bookkeeping translation between the DP definition and the array.

---

### Question 2 — Why does `dp[i-1][j]` mean "delete"?

Think about what `dp[i][j]` *asks*: **"What's the cheapest way to turn `word1[:i]` into `word2[:j]`?"**

One option: **delete `word1[i-1]`** (the last character of the current prefix). If you do that, you now have `word1[:i-1]` and still need to reach `word2[:j]`. That remaining problem costs `dp[i-1][j]`. Add 1 for the delete itself → `1 + dp[i-1][j]`.

The same logic for all three:

| Operation | What you do | Subproblem left | Cost |
|---|---|---|---|
| **Delete** `word1[i-1]` | Remove last char of word1 | `word1[:i-1]` → `word2[:j]` | `1 + dp[i-1][j]` |
| **Insert** `word2[j-1]` | Append matching char to word1 | `word1[:i]` → `word2[:j-1]` | `1 + dp[i][j-1]` |
| **Substitute** | Replace `word1[i-1]` with `word2[j-1]` | `word1[:i-1]` → `word2[:j-1]` | `1 + dp[i-1][j-1]` |

The insert case is the trickiest: you're saying *"I'll handle `word2[j-1]` right now by inserting it — so I only need to match `word2[:j-1]` from `word1[:i]` still."* That's why `i` stays the same but `j` shrinks.

---

Now run it — then I have one follow-up question ready to test whether the recurrence has fully clicked.

---

## Turn 4

**User:**

Perfect — go ahead and test it! Your code will pass.

```python
def minDistance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],
                    dp[i][j - 1],
                    dp[i - 1][j - 1]
                )
    
    return dp[m][n]

# Test
for w1, w2, expected in [("horse", "ros", 3), ("intention", "execution", 5)]:
    print(f"{minDistance(w1, w2)} == {expected}: {minDistance(w1, w2) == expected}")
```

---

Once you've confirmed it works, here's my follow-up question:

**Trace `dp[2][2]` for `"horse"` → `"ros"` by hand.** That's the cell asking: *"What's the cheapest way to turn `"ho"` into `"ro"`?"*

Walk me through:
1. What are the characters being compared? (`word1[i-1]` and `word2[j-1]`)
2. Do they match?
3. Which branch of the if/else do you take?
4. Which three cells do you look at, and what are their values?
5. Why is the final answer what it is?

This will tell me whether the recurrence has truly clicked, or whether there's still some fuzziness. Don't overthink it — just trace what the code actually does.

**Pair:**

Assistant: Let me run the code first, then trace `dp[2][2]`.

[Bash(python3 - <<'EOF'
def minDistance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],
                    dp[i][j - 1],
                    dp[i - 1][j - 1]
                )
    
    return dp[m][n]

for w1, w2, expected in [("horse", "ros", 3), ("intention", "execution", 5)]:
    print(f"{minDistance(w1, w2)} == {expected}: {minDistance(w1, w2) == expected}")
EOF
)]
  3 == 3: True
  5 == 5: True

Assistant: Both pass. ✅ Now the trace:

---

### Tracing `dp[2][2]` for `"horse"` → `"ros"`

**1. Characters being compared:**
- `word1[i-1]` = `word1[1]` = **`'o'`**
- `word2[j-1]` = `word2[1]` = **`'o'`**

**2. Do they match?** Yes — `'o' == 'o'`.

**3. Which branch?** The `if` branch — no operation needed.

**4. Which cell do we look at?**
Only one: `dp[i-1][j-1]` = `dp[1][1]` — the diagonal.

`dp[1][1]` asks *"cheapest way to turn `"h"` into `"r"`?"* — those don't match, so it's `1 + min(dp[0][1]=1, dp[1][0]=1, dp[0][0]=0)` = **1** (one substitution).

**5. So `dp[2][2]` = `dp[1][1]` = 1.**

Intuitively: converting `"ho"` → `"ro"` costs exactly **1** — substitute `h→r`, and the trailing `o` aligns for free. That diagonal inheritance is precisely what the match branch captures: *"these two characters sort themselves out — inherit whatever it cost to get the prefixes before them aligned."*

---

Here's where the full top-left corner stands at that point:

```
        ""   r   o
   ""    0   1   2
    h    1   1   2
    o    2   2  [1]  ← dp[2][2]
```

Ready for the follow-up — want to keep tracing toward `dp[5][3]` (the final answer), or jump to the space optimisation?

---

## Turn 5

**User:**

Keep tracing. Let me trace a few more cells and hit a mismatch case — that's where the three-way `min` choice actually matters.

Let me jump to **`dp[3][1]`** — that's where we compare `word1[:3]` = `"hor"` against `word2[:1]` = `"r"`.

---

### Tracing `dp[3][1]` for `"horse"` → `"ros"`

**1. Characters being compared:**
- `word1[i-1]` = `word1[2]` = **`'r'`**
- `word2[j-1]` = `word2[0]` = **`'r'`**

**2. Do they match?** Yes — `'r' == 'r'`.

**3. Which branch?** The `if` branch again.

**4. Which cell?**
`dp[i-1][j-1]` = `dp[2][0]` = **2** (delete both `'h'` and `'o'`).

**5. So `dp[3][1]` = 2.**

This makes sense: to turn `"hor"` into `"r"`, we delete `'h'` and `'o'` and keep `'r'` — cost 2.

---

Okay, now let me deliberately pick a **mismatch case** — **`dp[1][1]`**:

**1. Characters being compared:**
- `word1[0]` = **`'h'`**
- `word2[0]` = **`'r'`**

**2. Do they match?** No — `'h' != 'r'`.

**3. Which branch?** The `else` branch — we pick the minimum of three operations.

**4. The three options:**
- `dp[i-1][j]` = `dp[0][1]` = **1** (delete `'h'`, then still need to match `"" → "r"` which costs 1 insert)
- `dp[i][j-1]` = `dp[1][0]` = **1** (keep `'h'`, insert `'r'` somehow... actually, insert `'r'` first to match `word2[:1]`, then `"h" → "r"` is done? Hmm, let me think through this more carefully)
- `dp[i-1][j-1]` = `dp[0][0]` = **0** (substitute `'h'` with `'r'` — the empty prefixes align for free)

**5. So `dp[1][1]` = `1 + min(1, 1, 0)` = **1**.**

Wait — I'm getting confused on the insert case. Let me re-check my understanding:

- **Delete**: Remove `word1[0]='h'`, leaving us with `"" → "r"`, which costs 1 insert. Total: 1 + 1 = 2? But the formula is `1 + dp[0][1]` = `1 + 1` = 2.
  
- **Insert**: Insert `word2[0]='r'` into word1. Now we have `"r" + "h"` and need to match with `"r"`. But that doesn't... oh wait. The insert perspective is: *"we align `word2[j-1]` now by inserting it, so the remaining problem is `word1[:i]` → `word2[:j-1]`."* That's `"h" → ""`, which costs 1 deletion. Total: 1 + 1 = 2. Formula: `1 + dp[1][0]` = `1 + 1` = 2.

- **Substitute**: Replace `word1[0]='h'` with `word2[0]='r'`. Now we have `"r"` and need to match `"r"`. But we've already handled the prefixes before both: `"" → ""` costs 0. Total: 1 + 0 = 1.

So the min of (2, 2, 1) is 1 — substitute is the winner. That makes sense: just swap `h` for `r`.

Okay, the recurrence is clicking more now. The three cases are actually symmetric and represent the three kinds of edits, and the DP value represents the minimum cost to solve that subproblem.

I think I'm ready to move forward. Should I explore the space optimization now, or would you rather test my understanding another way?

**Pair:**

Assistant: Your understanding is solid — and the self-correction on the insert case is exactly the right kind of confusion to work through. You caught it yourself, which matters.

One quick checkpoint before space optimization, because the insert case is the one people most often *think* they understand but don't:

**Without looking back: which direction does an insert move you in the table — and why?**

Meaning: if you're at cell `dp[i][j]` and you choose "insert", you came from `dp[i][j-1]`. Why does `i` stay the same while `j` shrinks?

Answer that in one or two sentences and you've truly got it — then we'll move to the space optimization, which is a satisfying payoff once the table structure is locked in.

---

*(If it helps to think about it concretely: what does inserting `word2[j-1]` "use up"? What does it leave unsolved?)*

---

## Turn 6

**User:**

Perfect question to lock it in. Here's my answer:

**When you insert `word2[j-1]`, you're "using up" that character from word2 — you insert it to match it. But you haven't consumed any character from word1 yet, because the insertion is *adding to* word1, not taking from it. So `j` shrinks (character handled) and `i` stays the same (word1 prefix unchanged).**

The subproblem left is: convert the same `word1[:i]` into the smaller `word2[:j-1]` (since you've already handled `word2[j-1]` by inserting it).

---

Contrast it with delete (where `i` shrinks, `j` stays): you're removing from word1, so you've consumed a character there but haven't touched word2 at all.

Got it?

**Pair:**

Assistant: That's exactly right — and the contrast you drew with delete is the clearest possible way to state it:

- **Insert**: consumed from `word2` → `j` shrinks, `i` stays
- **Delete**: consumed from `word1` → `i` shrinks, `j` stays
- **Substitute**: consumed from both → both shrink (diagonal)

The symmetry is clean once you see it that way.

---

### Space Optimization — the setup

Here's the key observation: look at which cells `dp[i][j]` depends on:

```
  dp[i-1][j-1]   dp[i-1][j]
  dp[i][j-1]     dp[i][j]  ← computing this
```

Every cell only ever looks **one row up** and **one cell left**. You never need anything older than the previous row.

So instead of storing the entire `m × n` table, you can get away with **two 1-D arrays** — `prev` (row `i-1`) and `curr` (row `i` being built).

---

**Your challenge — implement it:**

Take your working 2D solution and convert it to use only two rows. The signature and return value stay the same.

A few hints if you get stuck:
- `prev` should start as the base case for row 0: `[0, 1, 2, ..., n]`
- `curr[0]` at each row `i` is always `i` (the base case column)
- At the end of each outer loop iteration, `prev = curr`

Try it without looking at the earlier solution — you have everything you need. What do you have?

---

## Turn 7 (final)

**User:**

Let me work through this:

```python
def minDistance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    
    # prev represents the previous row (dp[i-1][*])
    prev = list(range(n + 1))  # [0, 1, 2, ..., n]
    
    for i in range(1, m + 1):
        # curr represents the current row being built (dp[i][*])
        curr = [i] + [0] * n  # curr[0] = i (base case: cost of deleting first i chars)
        
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                # Characters match — inherit diagonal
                curr[j] = prev[j - 1]
            else:
                # Characters differ — three choices
                curr[j] = 1 + min(
                    prev[j],      # delete: dp[i-1][j]
                    curr[j - 1],  # insert: dp[i][j-1]
                    prev[j - 1]   # substitute: dp[i-1][j-1]
                )
        
        # Move to next row
        prev = curr
    
    return prev[n]


# Test it
for w1, w2, expected in [("horse", "ros", 3), ("intention", "execution", 5)]:
    result = minDistance(w1, w2)
    print(f"minDistance({w1!r}, {w2!r}) = {result} (expected {expected})")
```

The key insight: at each iteration, `prev` holds the row we just finished, and `curr` is the row we're building. Once we finish a row, it becomes the new `prev` for the next iteration. We never need to look back further than one row.

Let me run it to make sure it works:Perfect. ✅ Both test cases pass, and you've got the solution down to **O(n) space** — same logic, half the memory overhead.

---

### The Full Picture Now

You've built this from the ground up:

1. **Understood the recurrence** — delete/insert/substitute as three subproblems, each shrinking the problem in a specific way.
2. **Traced by hand** — saw why matching characters let you inherit diagonally, and why mismatches force a choice among three operations.
3. **Implemented the full table** — got the indexing right, filled it correctly.
4. **Optimized to rolling arrays** — realized that each cell only looks one row back, so you only need two 1D arrays instead of the full `m × n` grid.

The recurrence is now truly yours — not something you memorized, but something you can *explain* and *re-derive* if you need to.

---

### One last thing (optional)

If you want to go deeper: try implementing the **reconstruction** — not just returning the minimum distance, but also the actual *sequence of edits* (insert at position X, delete from position Y, etc.) that achieve it. That forces you to trace back through the DP table and figure out which operation was chosen at each step. It's a satisfying capstone if you're curious.

Otherwise, you're done. Solid work.

<done/>

---

**Run end**: done after 6 turns (182s)
