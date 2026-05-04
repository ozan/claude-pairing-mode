# ours-tic-tac-toe

- Source: `ours`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:42:47.114Z

---

## Turn 1

**User:**

Let's implement tic-tac-toe in Python. Single file, human vs computer, command line.

**Pair:**

[Glob(tic_tac_toe.py)]
  No files found

Assistant: Let's start with the most fundamental design decision — how to represent the board. Which of these would you go with?

**Option A — Flat list**
```diff
+++ tic_tac_toe.py
@@ -0,0 +1,4 @@
+WINS = [(0,1,2),(3,4,5),(6,7,8),
+        (0,3,6),(1,4,7),(2,5,8),
+        (0,4,8),(2,4,6)]
+board = [' '] * 9
```

**Option B — 3×3 nested list**
```diff
+++ tic_tac_toe.py
@@ -0,0 +1,4 @@
+WINS = [[(0,0),(0,1),(0,2)],[(1,0),(1,1),(1,2)],[(2,0),(2,1),(2,2)],
+        [(0,0),(1,0),(2,0)],[(0,1),(1,1),(2,1)],[(0,2),(1,2),(2,2)],
+        [(0,0),(1,1),(2,2)],[(0,2),(1,1),(2,0)]]
+board = [[' ']*3 for _ in range(3)]
```

Which do you prefer?

---

## Turn 2

**User:**

I'd go with **Option A — the flat list**.

Here's my thinking: The flat representation keeps the win-checking logic clean and simple (just tuple-matching), and it's easier to feed positions to the computer AI without juggling coordinate conversions. Option B's nested structure is more "visually intuitive" but adds friction when you're actually checking wins or scanning the whole board in a loop.

For a command-line game, we can still display the board nicely with a little formatting — the flat index doesn't have to leak into the UI.

Let's go with Option A.

**Pair:**

Assistant: Exactly right. Let me lay down the foundation.

[Write(tic_tac_toe.py)]
WINS = [(0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)]
board = [' '] * 9


Assistant: Good. Next up: the computer's move logic. This is where the game gets interesting — which approach?

Assistant: **Option A — Minimax**
```diff
+++ tic_tac_toe.py
@@ -4,0 +5,13 @@
+def minimax(board, is_max):
+    winner = get_winner(board)
+    if winner == 'X': return -1
+    if winner == 'O': return  1
+    if ' ' not in board: return  0
+    scores = []
+    for i in range(9):
+        if board[i] == ' ':
+            board[i] = 'O' if is_max else 'X'
+            scores.append(minimax(board, not is_max))
+            board[i] = ' '
+    return max(scores) if is_max else min(scores)
```

**Option B — Heuristic (win/block/random)**
```diff
+++ tic_tac_toe.py
@@ -4,0 +5,11 @@
+def computer_move(board):
+    for mark in ('O', 'X'):          # win, then block
+        for line in WINS:
+            vals = [board[i] for i in line]
+            if vals.count(mark) == 2 and ' ' in vals:
+                return line[vals.index(' ')]
+    if board[4] == ' ': return 4     # centre
+    corners = [i for i in (0,2,6,8) if board[i]==' ']
+    if corners: return random.choice(corners)
+    return random.choice([i for i,v in enumerate(board) if v==' '])
```

Which do you want for the computer player?

---

## Turn 3

**User:**

I'd go with **Option B — Heuristic**.

Here's my thinking: For a command-line game, minimax feels like overkill. It would play perfectly (always tie or win), which makes the game deterministic and less fun to actually *play*. The human would lose every time.

The heuristic approach is way cleaner — it's simple enough to understand at a glance, it's fast, and it actually gives the human a fighting chance. The logic is readable: "win if you can, block the opponent, then take the center, corners, or whatever's left." That's a solid B-level opponent without being unbeatable.

Plus, if we later want to tweak difficulty (like "sometimes pick suboptimal moves"), the heuristic is trivial to modify. Minimax less so.

Let's go with the heuristic. We'll need to import `random` for it, so let's add that at the top.

**Pair:**

Assistant: Great call — and your point about modifiable difficulty is spot on. Let me apply it.

[Read(tic_tac_toe.py)]
  1	WINS = [(0,1,2),(3,4,5),(6,7,8),
  2	        (0,3,6),(1,4,7),(2,5,8),
  3	        (0,4,8),(2,4,6)]
  4	board = [' '] * 9
  5

[Edit(tic_tac_toe.py)]
--- before
WINS = [(0,1,2),(3,4,5),(6,7,8),
--- after
import random

WINS = [(0,1,2),(3,4,5),(6,7,8),

[Edit(tic_tac_toe.py)]
--- before
board = [' '] * 9
--- after
board = [' '] * 9

def get_winner(board):
    for a, b, c in WINS:
        if board[a] == board[b] == board[c] != ' ':
            return board[a]
    return None

def computer_move(board):
    for mark in ('O', 'X'):          # win, then block
        for line in WINS:
            vals = [board[i] for i in line]
            if vals.count(mark) == 2 and ' ' in vals:
                return line[vals.index(' ')]
    if board[4] == ' ': return 4     # centre
    corners = [i for i in (0,2,6,8) if board[i]==' ']
    if corners: return random.choice(corners)
    return random.choice([i for i,v in enumerate(board) if v==' '])

Assistant: I snuck in `get_winner` too — it'll be needed by the game loop. Now let's think about the display. Two options:

**Option A — Labels from position**
```diff
+++ tic_tac_toe.py
@@ -18,0 +19,6 @@
+def display(board):
+    def cell(i):
+        return board[i] if board[i] != ' ' else str(i+1)
+    for r in range(3):
+        print(' | '.join(cell(r*3+c) for c in range(3)))
+        if r < 2: print('--+---+--')
```

**Option B — Blank for empty**
```diff
+++ tic_tac_toe.py
@@ -18,0 +19,5 @@
+def display(board):
+    for r in range(3):
+        print(' | '.join(board[r*3+c] for c in range(3)))
+        if r < 2: print('--+---+--')
```

Option A shows position numbers in empty cells (so the player always knows what to type). Option B shows blanks. Which do you prefer?

---

## Turn 4

**User:**

I'd go with **Option A — Labels from position**.

Here's why: For a command-line game, the player needs to know *which position to type* when they want to move. If the board just shows blanks (Option B), they'd have to mentally map the grid positions themselves—"is that top-left position 1 or 0?"—and reference some external guide. That's friction.

Option A puts the position labels *right there* in the empty cells, so the move prompt becomes obvious: "Type any number from the board." The player can see their options at a glance. Much better UX for a CLI game.

Let's go with Option A.

**Pair:**

Assistant: Agreed, it's a small touch that makes the game self-documenting. Applying it:

[Read(tic_tac_toe.py)]
  1	import random
  2	
  3	WINS = [(0,1,2),(3,4,5),(6,7,8),
  4	        (0,3,6),(1,4,7),(2,5,8),
  5	        (0,4,8),(2,4,6)]
  6	board = [' '] * 9
  7	
  8	def get_winner(board):
  9	    for a, b, c in WINS:
  10	        if board[a] == board[b] == board[c] != ' ':
  11	            return board[a]
  12	    return None
  … (12 more lines)

[Edit(tic_tac_toe.py)]
--- before
    return random.choice([i for i,v in enumerate(board) if v==' '])
--- after
    return random.choice([i for i,v in enumerate(board) if v==' '])

def display(board):
    def cell(i):
        return board[i] if board[i] != ' ' else str(i+1)
    for r in range(3):
        print(' | '.join(cell(r*3+c) for c in range(3)))
        if r < 2: print('--+---+--')

Assistant: Now for the game loop — the last piece. One question here about turn order:

**Option A — Computer goes second always**
```diff
+++ tic_tac_toe.py
@@ -31,0 +32,16 @@
+def play():
+    board = [' '] * 9
+    display(board)
+    for turn in range(9):
+        if turn % 2 == 0:
+            move = int(input("Your move (1-9): ")) - 1
+            board[move] = 'X'
+        else:
+            move = computer_move(board)
+            print(f"Computer plays {move+1}")
+            board[move] = 'O'
+        display(board)
+        winner = get_winner(board)
+        if winner:
+            print("You win!" if winner=='X' else "Computer wins!")
+            return
+    print("Draw!")
```

**Option B — Randomly decide who goes first**
```diff
+++ tic_tac_toe.py
@@ -31,0 +32,18 @@
+def play():
+    board = [' '] * 9
+    human = random.choice(['X', 'O'])
+    cpu = 'O' if human == 'X' else 'X'
+    print(f"You are {human}. ", end='')
+    print("You go first!" if human=='X' else "Computer goes first!")
+    display(board)
+    for turn in range(9):
+        current = 'X' if turn % 2 == 0 else 'O'
+        if current == human:
+            move = int(input("Your move (1-9): ")) - 1
+            board[move] = current
+        else:
+            move = computer_move(board)
+            print(f"Computer plays {move+1}")
+            board[move] = current
+        display(board)
+        winner = get_winner(board)
+        if winner:
+            print("You win!" if winner==human else "Computer wins!")
+            return
+    print("Draw!")
```

Which do you prefer?

---

## Turn 5

**User:**

I'd go with **Option A — Computer goes second always**.

Here's my thinking: Given the choices we've made so far—flat list for simplicity, heuristic for readable logic, position labels for self-documenting UX—I think consistency and predictability fit the pattern. 

With Option A, the game has a fixed identity: *you are X, you always move first, the computer is O.* There's no cognitive overhead about "who am I today?" The player can focus entirely on strategy. It's simpler to code, easier to test, and for a single-file CLI game, that directness is a win.

Option B is appealing—variety *is* fun across multiple plays. But it adds branching logic (`human` vs `cpu` variables, alternate parity checks). For our scope, Option A feels like the right tradeoff: straightforward, teachable, and still totally playable.

Plus, we can always add a "difficulty toggle" later if we want to shake things up. But let's start with the simple, predictable version.

Let's go with Option A.

**Pair:**

Assistant: Good — simple, predictable, and consistent with the decisions so far. Applying:

[Read(tic_tac_toe.py)]
  1	import random
  2	
  3	WINS = [(0,1,2),(3,4,5),(6,7,8),
  4	        (0,3,6),(1,4,7),(2,5,8),
  5	        (0,4,8),(2,4,6)]
  6	board = [' '] * 9
  7	
  8	def get_winner(board):
  9	    for a, b, c in WINS:
  10	        if board[a] == board[b] == board[c] != ' ':
  11	            return board[a]
  12	    return None
  … (19 more lines)

[Edit(tic_tac_toe.py)]
--- before
board = [' '] * 9

def get_winner(board):
--- after
def get_winner(board):

[Edit(tic_tac_toe.py)]
--- before
        if r < 2: print('--+---+--')
--- after
        if r < 2: print('--+---+--')

def play():
    board = [' '] * 9
    display(board)
    for turn in range(9):
        if turn % 2 == 0:
            while True:
                try:
                    move = int(input("Your move (1-9): ")) - 1
                    if 0 <= move <= 8 and board[move] == ' ':
                        break
                except ValueError:
                    pass
                print("Invalid move, try again.")
            board[move] = 'X'
        else:
            move = computer_move(board)
            print(f"Computer plays {move+1}")
            board[move] = 'O'
        display(board)
        winner = get_winner(board)
        if winner:
            print("You win!" if winner == 'X' else "Computer wins!")
            return
    print("Draw!")

if __name__ == '__main__':
    play()

Assistant: I added input validation in the human turn — it rejects out-of-range entries, non-integers, and already-taken cells. Let's verify the full file looks right:

[Read(tic_tac_toe.py)]
  1	import random
  2	
  3	WINS = [(0,1,2),(3,4,5),(6,7,8),
  4	        (0,3,6),(1,4,7),(2,5,8),
  5	        (0,4,8),(2,4,6)]
  6	def get_winner(board):
  7	    for a, b, c in WINS:
  8	        if board[a] == board[b] == board[c] != ' ':
  9	            return board[a]
  10	    return None
  11	
  12	def computer_move(board):
  … (45 more lines)

Assistant: Clean. Let's give it a quick smoke test:

[Bash(echo "5
1
9
3
7" | python tic_tac_toe.py)]
  error: Exit code 127

[Bash(echo "5
1
9
3
7" | python3 tic_tac_toe.py)]
  1 | 2 | 3
  --+---+--
  4 | 5 | 6
  --+---+--
  7 | 8 | 9
  Your move (1-9): 1 | 2 | 3
  --+---+--
  4 | X | 6
  --+---+--
  7 | 8 | 9
  Computer plays 9
  1 | 2 | 3
  … (28 more lines)

Assistant: Works perfectly. A few things worth noting in that output:

- The board renders cleanly with position labels in empty cells
- The computer correctly blocked (played 7 to get two O's on the bottom row, then 8 to complete it)
- The invalid move (`9` was already taken) was caught and re-prompted without crashing

`python3 tic_tac_toe.py` to play. The heuristic is solid — it'll beat you if you're not paying attention, but it's not unbeatable.

---

## Turn 6 (final)

**User:**

Perfect! We've got a complete, playable tic-tac-toe game. Let me summarize what we built:

## What we chose (and why)

1. **Flat list board** — clean win-checking, easy to iterate
2. **Heuristic AI** — reads like plain English (win, block, center, corners), beatable but smart
3. **Position labels in empty cells** — self-documenting UI, player always knows what to type
4. **Human always X, goes first** — consistent, predictable, zero cognitive overhead
5. **Input validation** — rejects invalid moves, non-integers, out-of-range, already-taken cells

## How to play

```bash
python3 tic_tac_toe.py
```

Type 1–9 for your move. The board shows available positions. Computer plays O and announces its moves.

## The code lives in one file

All 50-some lines in `tic_tac_toe.py` — no external dependencies beyond Python's standard `random` module. Each function is focused: `get_winner()` checks for a match, `computer_move()` decides the next O, `display()` renders the board, `play()` orchestrates the game loop.

The heuristic is tuned so the computer is competent (it won't throw away winning positions, it'll block your threats) but not perfect. You can actually win against it with decent play.

<done/>

---

**Run end**: done after 5 turns (251s)
