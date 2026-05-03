"""10-pin bowling scorer (Exercism)."""


def score(rolls):
    """Return the total score for a complete, valid game of bowling.

    Args:
        rolls: list of int — pin counts in delivery order.

    Returns:
        int — final score (0–300).

    Raises:
        ValueError: if the roll sequence is invalid or the game is incomplete.
    """
    total = 0
    roll = 0  # index into rolls[]

    for frame in range(10):
        if roll >= len(rolls):
            raise ValueError("Score cannot be taken until the end of the game")

        if frame < 9:
            # ── Frames 1–9 ────────────────────────────────────────────────
            if rolls[roll] > 10:
                raise ValueError("Pin count exceeds pins on the lane")
            if rolls[roll] < 0:
                raise ValueError("Negative pins not allowed")

            if rolls[roll] == 10:
                # Strike
                if roll + 2 >= len(rolls):
                    raise ValueError("Score cannot be taken until the end of the game")
                b1, b2 = rolls[roll + 1], rolls[roll + 2]
                if b1 < 0 or b2 < 0:
                    raise ValueError("Negative pins not allowed")
                if b1 > 10 or (b1 < 10 and b1 + b2 > 10):
                    raise ValueError("Pin count exceeds pins on the lane")
                total += 10 + b1 + b2
                roll += 1
            else:
                # Normal or spare
                if roll + 1 >= len(rolls):
                    raise ValueError("Score cannot be taken until the end of the game")
                r1, r2 = rolls[roll], rolls[roll + 1]
                if r2 < 0:
                    raise ValueError("Negative pins not allowed")
                if r1 + r2 > 10:
                    raise ValueError("Pin count exceeds pins on the lane")

                if r1 + r2 == 10:
                    # Spare
                    if roll + 2 >= len(rolls):
                        raise ValueError("Score cannot be taken until the end of the game")
                    total += 10 + rolls[roll + 2]
                else:
                    total += r1 + r2

                roll += 2

        else:
            # ── 10th frame ────────────────────────────────────────────────
            if rolls[roll] < 0:
                raise ValueError("Negative pins not allowed")
            if rolls[roll] > 10:
                raise ValueError("Pin count exceeds pins on the lane")

            if rolls[roll] == 10:
                # Strike in 10th — two bonus rolls
                if roll + 2 >= len(rolls):
                    raise ValueError("Score cannot be taken until the end of the game")
                b1, b2 = rolls[roll + 1], rolls[roll + 2]
                if b1 < 0 or b2 < 0:
                    raise ValueError("Negative pins not allowed")
                if b1 > 10:
                    raise ValueError("Pin count exceeds pins on the lane")
                if b1 == 10:
                    if b2 > 10:
                        raise ValueError("Pin count exceeds pins on the lane")
                else:
                    if b1 + b2 > 10:
                        raise ValueError("Pin count exceeds pins on the lane")
                total += 10 + b1 + b2
                roll += 3
            else:
                # Not a strike — need second ball
                if roll + 1 >= len(rolls):
                    raise ValueError("Score cannot be taken until the end of the game")
                r2 = rolls[roll + 1]
                if r2 < 0:
                    raise ValueError("Negative pins not allowed")
                if rolls[roll] + r2 > 10:
                    raise ValueError("Pin count exceeds pins on the lane")

                if rolls[roll] + r2 == 10:
                    # Spare in 10th — one bonus roll
                    if roll + 2 >= len(rolls):
                        raise ValueError("Score cannot be taken until the end of the game")
                    b1 = rolls[roll + 2]
                    if b1 < 0 or b1 > 10:
                        raise ValueError("Pin count exceeds pins on the lane")
                    total += 10 + b1
                    roll += 3
                else:
                    total += rolls[roll] + r2
                    roll += 2

    # Any leftover rolls mean the game is over — extra rolls are only valid
    # if they were consumed above as bonus balls.
    if roll != len(rolls):
        raise ValueError("Cannot roll after game is over")

    return total
