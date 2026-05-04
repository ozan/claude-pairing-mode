# ours-tic-tac-toe

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-05T07:26:55

## Initial prompt

Let's implement tic-tac-toe in Python. Single file, human vs computer, command line.

---

## Turn 1

### Tutor

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

Tutor: Good, let's start. First decision: how to represent the board.

OPTIONS:
[A] Flat list of 9
```diff
+++ tic_tac_toe.py
@@ -0,0 +1,4 @@
+board = [' '] * 9
+# positions:
+# 0 | 1 | 2
+# 3 | 4 | 5
+# 6 | 7 | 8
```
Win lines are index tuples; access is `board[i]`.

[B] 3×3 nested list
```diff
+++ tic_tac_toe.py
@@ -0,0 +1,3 @@
+board = [[' '] * 3 for _ in range(3)]
+# access: board[row][col]
```
Mirrors the visual grid; row/col indexing feels natural.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which do you prefer?

### Student

I'll go with **A** — the flat list of 9.

I think it'll be simpler to work with for checking win conditions. If I hardcode the winning lines as index tuples like `(0, 1, 2)`, `(3, 4, 5)`, etc., it'll be straightforward to loop through them and check if all three positions are the same. With a nested list I'd have to convert between row/col and indices anyway, so the flat structure feels more direct.

---

## Turn 2

### Tutor

Tutor: Exactly right. Let's get the file started.

[Write(tic_tac_toe.py)]
LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
    (0, 4, 8), (2, 4, 6),             # diagonals
]

def make_board():
    return [' '] * 9

def winner(board):
    for a, b, c in LINES:
        if board[a] == board[b] == board[c] != ' ':
… (3 more lines)
  File created successfully at: tic_tac_toe.py

Tutor: Now the most interesting decision — the computer's strategy:

OPTIONS:
[A] Random empty square
```diff
+++ tic_tac_toe.py
@@ -12,0 +13,4 @@
+import random
+
+def computer_move(board):
+    return random.choice([i for i, v in enumerate(board) if v == ' '])
```
Simple, beatable — the game has tension.

[B] Minimax
```diff
+++ tic_tac_toe.py
@@ -12,0 +13,14 @@
+def minimax(board, is_max):
+    w = winner(board)
+    if w == 'O': return 1
+    if w == 'X': return -1
+    moves = [i for i, v in enumerate(board) if v == ' ']
+    if not moves: return 0
+    scores = []
+    for i in moves:
+        board[i] = 'O' if is_max else 'X'
+        scores.append(minimax(board, not is_max))
+        board[i] = ' '
+    return max(scores) if is_max else min(scores)
+
+def computer_move(board):
+    moves = [i for i, v in enumerate(board) if v == ' ']
+    return max(moves, key=lambda i: (board.__setitem__(i,'O') or minimax(board,False) or 0, board.__setitem__(i,' ') or 0))
```
Unbeatable — always plays the optimal move.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which do you prefer?

### Student

I'll go with **A** — random empty square.

For a first pass at tic-tac-toe, I think random is the right call. It'll let us actually finish the game and play it, and we can still win or lose depending on luck. Minimax is cool, but it feels like scope creep right now — we don't even have the game loop or input handling yet, and I'd rather get a working, playable game first.

Plus, if we do random now and it feels too easy, we can always add minimax later. But if we start with minimax, we might get bogged down in debugging the algorithm before we even know if the rest of the game works.

---

## Turn 3

### Tutor

Tutor: Fair enough — here's my honest take though: minimax for tic-tac-toe is genuinely ~10 lines and the game tree is tiny (at most 9 levels deep, heavily pruned). It's not scope creep so much as a drop-in replacement for `random.choice`. The "finish the loop first" instinct is good in general, but here the algorithm is so self-contained it wouldn't block anything.

That said, your incremental reasoning is sound and random totally works. Want to stick with it, or swap in minimax now that you know it's that small?

### Student

You know what, that's a fair point. If it's really just a drop-in replacement and the game tree is that constrained, I don't think it'll actually slow us down. And honestly, an unbeatable opponent is way more interesting to test against — even if I can't beat it, I can at least verify the game logic works correctly.

Let me swap to **B** — minimax. I'd rather have the cleaner final version and understand how it works while we're building this, than add it as an afterthought later.

---

## Turn 4

### Tutor

Tutor: Good call. Let me read the current file and apply a clean version:

[Read(tic_tac_toe.py)]
  1	LINES = [
  2	    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
  3	    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
  4	    (0, 4, 8), (2, 4, 6),             # diagonals
  5	]
  6	
  7	def make_board():
  8	    return [' '] * 9
  9	
  10	def winner(board):
  11	    for a, b, c in LINES:
  12	        if board[a] == board[b] == board[c] != ' ':
  … (3 more lines)

[Edit(tic_tac_toe.py)]
--- before
def winner(board):
    for a, b, c in LINES:
        if board[a] == board[b] == board[c] != ' ':
            return board[a]
    return None
--- after
def winner(board):
    for a, b, c in LINES:
        if board[a] == board[b] == board[c] != ' ':
            return board[a]
    return None

def minimax(board, is_max):
    w = winner(board)
    if w == 'O': return 1
    if w == 'X': return -1
    moves = [i for i, v in enumerate(board) if v == ' ']
    if not moves: return 0
    results = []
    for i in moves:
        board[i] = 'O' if is_max else 'X'
        results.append(minimax(board, not is_max))
        board[i] = ' '
    return max(results) if is_max else min(results)

def computer_move(board):
    moves = [i for i, v in enumerate(board) if v == ' ']
    best = max(moves, key=lambda i: _score_move(board, i))
    return best

def _score_move(board, i):
    board[i] = 'O'
    s = minimax(board, False)
    board[i] = ' '
    return s
  The file tic_tac_toe.py has been updated successfully.

Tutor: The core logic is done. Now let's wire up display and input. One decision worth pausing on — input validation:

OPTIONS:
[A] isdigit then range-check
```diff
+++ tic_tac_toe.py
@@ -35,0 +36,6 @@
+def get_human_move(board):
+    while True:
+        s = input("Your move (1-9): ").strip()
+        if s.isdigit() and 1 <= int(s) <= 9 and board[int(s)-1] == ' ':
+            return int(s) - 1
+        print("Invalid move, try again.")
```

[B] try/except int()
```diff
+++ tic_tac_toe.py
@@ -35,0 +36,8 @@
+def get_human_move(board):
+    while True:
+        try:
+            i = int(input("Your move (1-9): ")) - 1
+            if 0 <= i <= 8 and board[i] == ' ':
+                return i
+        except ValueError:
+            pass
+        print("Invalid move, try again.")
```

(Reply with A or B, or ask a follow-up question.)

### Student

I'll go with **A** — isdigit then range-check.

It's more explicit about what we're validating, and I find it easier to read. With `isdigit()` I can see right away that we're checking "is this a digit string", then the range, then the board state. The try/except approach works fine, but it feels like we're using exception handling for control flow, which I've heard is not ideal in Python.

Plus, `isdigit()` is clearer intent — we know upfront whether the user gave us digits or garbage, before we even try to convert.

---

## Turn 5

### Tutor

Tutor: Worth pushing back on the "exceptions for control flow" concern — that's actually the *opposite* of the Python idiom. Python explicitly encourages **EAFP** (Easier to Ask Forgiveness than Permission) over **LBYL** (Look Before You Leap). `try/except ValueError` around `int()` is considered more Pythonic, not less.

The concrete issue with `isdigit()`: it returns `False` for `"-1"` or `" 3"` (with a space), even after `.strip()` on the outer string. Worse, it calls `int()` twice — once hidden inside the condition, once to get the value. It's not wrong here, just subtly fragile at the edges.

That said, for a short script like this the difference is minor. Want to stick with `isdigit` or swap to `try/except`?

### Student

Okay, that's a good teaching moment — I didn't realize EAFP was the Python norm. And you're right, I was calling `int()` twice, which is wasteful.

Let me swap to **B** — try/except int().

I want to get the idioms right while I'm learning, and if that's how Python is meant to be written, better to practice it now than build bad habits. Plus it handles the edge cases more cleanly.

---

## Turn 6

### Tutor

Tutor: Good instinct. Applying it:

[Edit(tic_tac_toe.py)]
--- before
def _score_move(board, i):
    board[i] = 'O'
    s = minimax(board, False)
    board[i] = ' '
    return s
--- after
def _score_move(board, i):
    board[i] = 'O'
    s = minimax(board, False)
    board[i] = ' '
    return s

def get_human_move(board):
    while True:
        try:
            i = int(input("Your move (1-9): ")) - 1
            if 0 <= i <= 8 and board[i] == ' ':
                return i
        except ValueError:
            pass
        print("Invalid move, try again.")
  The file tic_tac_toe.py has been updated successfully.

Tutor: Now let's add display and the game loop. Quick decision on the board display — do we show position hints?

OPTIONS:
[A] Show position guide
```diff
+++ tic_tac_toe.py
@@ -48,0 +49,8 @@
+def print_board(board):
+    def cell(i):
+        return board[i] if board[i] != ' ' else str(i + 1)
+    for row in range(3):
+        r = row * 3
+        print(f" {cell(r)} | {cell(r+1)} | {cell(r+2)} ")
+        if row < 2:
+            print("---+---+---")
```
Empty squares show their number (1–9), so the player always has a reference.

[B] Board only, no hints
```diff
+++ tic_tac_toe.py
@@ -48,0 +49,6 @@
+def print_board(board):
+    for row in range(3):
+        r = row * 3
+        print(f" {board[r]} | {board[r+1]} | {board[r+2]} ")
+        if row < 2:
+            print("---+---+---")
```
Clean output; player memorizes or refers to the prompt.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which do you prefer?

### Student

I'll go with **A** — show position guide.

It's much more user-friendly. The player doesn't have to memorize or mentally map the 1–9 grid every turn. Since we're asking for input as 1–9, showing those numbers in the empty squares makes it immediately obvious which position corresponds to which number. It's a small quality-of-life thing, but it makes the game actually playable without frustration.

---

## Turn 7

### Tutor

Tutor: Exactly — good UX is invisible. Let's apply it and finish with the game loop:

[Edit(tic_tac_toe.py)]
--- before
def get_human_move(board):
--- after
def print_board(board):
    def cell(i):
        return board[i] if board[i] != ' ' else str(i + 1)
    for row in range(3):
        r = row * 3
        print(f" {cell(r)} | {cell(r+1)} | {cell(r+2)} ")
        if row < 2:
            print("---+---+---")

def get_human_move(board):
  The file tic_tac_toe.py has been updated successfully.

Tutor: Now the game loop — let me add it and the entry point:

[Read(tic_tac_toe.py)]
  1	LINES = [
  2	    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
  3	    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
  4	    (0, 4, 8), (2, 4, 6),             # diagonals
  5	]
  6	
  7	def make_board():
  8	    return [' '] * 9
  9	
  10	def winner(board):
  11	    for a, b, c in LINES:
  12	        if board[a] == board[b] == board[c] != ' ':
  … (46 more lines)

[Edit(tic_tac_toe.py)]
--- before
        print("Invalid move, try again.")
--- after
        print("Invalid move, try again.")

def play():
    board = make_board()
    print("You are X, computer is O. X goes first.")
    print_board(board)

    for turn in range(9):
        if turn % 2 == 0:
            board[get_human_move(board)] = 'X'
        else:
            move = computer_move(board)
            print(f"Computer plays {move + 1}.")
            board[move] = 'O'

        print_board(board)
        w = winner(board)
        if w:
            print(f"{'You win!' if w == 'X' else 'Computer wins!'}")
            return

    print("It's a draw.")

if __name__ == '__main__':
    play()
  The file tic_tac_toe.py has been updated successfully.

Tutor: It's playable. Let's do a quick sanity check:

[Bash(cd /tmp && echo "1
3
7" | python /Users/will/code/scratch/tic_tac_toe.py 2>&1 || true)]
  python: can't open file '/Users/will/code/scratch/tic_tac_toe.py': [Errno 2] No such file or directory
  Shell cwd was reset to /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-7qa_j56p

[Bash(echo "1
3
7" | python tic_tac_toe.py 2>&1 || true)]
  You are X, computer is O. X goes first.
   1 | 2 | 3 
  ---+---+---
   4 | 5 | 6 
  ---+---+---
   7 | 8 | 9 
  Your move (1-9):  X | 2 | 3 
  ---+---+---
   4 | 5 | 6 
  ---+---+---
   7 | 8 | 9 
  Computer plays 5.
  … (38 more lines)

Tutor: The EOF at the end is just the pipe running dry — the game logic is working correctly. Computer blocked the top row (position 2) then blocked the left column (position 4). Minimax is doing its job.

One last thing worth thinking about before calling it done:

OPTIONS:
[A] Keep deterministic computer
Leave `computer_move` as-is. `max()` always returns the first move with the highest score, so the computer plays the same game every time given the same inputs. Predictable, but unbeatable.

[B] Randomize among tied moves
```diff
+++ tic_tac_toe.py
@@ -29,3 +29,4 @@
 def computer_move(board):
     moves = [i for i, v in enumerate(board) if v == ' ']
-    best = max(moves, key=lambda i: _score_move(board, i))
-    return best
+    best_score = max(_score_move(board, i) for i in moves)
+    best_moves = [i for i in moves if _score_move(board, i) == best_score]
+    return random.choice(best_moves)
```
Among equally-scored moves, pick randomly — the computer still never loses, but varies its play.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which do you prefer?

### Student

I'll go with **B** — randomize among tied moves.

The computer is still unbeatable, so the game logic stays solid, but it adds variety. Playing the exact same game every time gets boring fast, and since multiple moves can have the same minimax score (especially early on), randomizing among those keeps things fresh. It's the best of both worlds — we keep the guarantee that the computer plays optimally, but the experience isn't deterministic and rote.

---

## Turn 8

### Tutor

Tutor: Agreed. Need to add `import random` too — let me apply both:

[Edit(tic_tac_toe.py)]
--- before
LINES = [
--- after
import random

LINES = [
  The file tic_tac_toe.py has been updated successfully.

[Edit(tic_tac_toe.py)]
--- before
def computer_move(board):
    moves = [i for i, v in enumerate(board) if v == ' ']
    best = max(moves, key=lambda i: _score_move(board, i))
    return best
--- after
def computer_move(board):
    moves = [i for i, v in enumerate(board) if v == ' ']
    best_score = max(_score_move(board, i) for i in moves)
    best_moves = [i for i in moves if _score_move(board, i) == best_score]
    return random.choice(best_moves)
  The file tic_tac_toe.py has been updated successfully.

Tutor: Let's do a final read to make sure everything looks clean:

[Read(tic_tac_toe.py)]
  1	import random
  2	
  3	LINES = [
  4	    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
  5	    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
  6	    (0, 4, 8), (2, 4, 6),             # diagonals
  7	]
  8	
  9	def make_board():
  10	    return [' '] * 9
  11	
  12	def winner(board):
  … (73 more lines)

Tutor: Clean. Here's a summary of what we built and the decisions we made:

- **Flat list** for the board — win lines as index tuples, no row/col translation needed
- **Minimax** for the AI — ~10 lines, fully optimal, exploits the tiny game tree
- **EAFP `try/except`** for input — idiomatic Python over `isdigit()` LBYL
- **Position hints** in the display — empty squares show their number so you never have to guess
- **Randomized tie-breaking** — unbeatable but not predictable

Run it with `python tic_tac_toe.py`. Fair warning: the best you can do is draw. 🙂

### Student

That's a solid summary. I feel like I learned a lot here — especially the EAFP thing, which I'll definitely remember. The minimax decision was good too; I was wrong about it being scope creep, and it turned out to be elegant and contained.

The game works, it's unbeatable but still fun to play (even if I can only tie), and the code is clean. I think we're done.

<done/>

---

**Run end:** done after 8 turn(s) in 172.7s
