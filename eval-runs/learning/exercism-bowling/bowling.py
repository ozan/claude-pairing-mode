def score(rolls):
    """Return the total score for a 10-pin bowling game.

    Args:
        rolls: list of pin counts, one integer per roll.

    Returns:
        Total score as an integer.

    Raises:
        ValueError: if the rolls list is invalid (wrong length,
                    negative counts, pin counts exceeding what
                    is physically possible, etc.).
    """
    _validate(rolls)

    cursor = 0  # index of the current roll being processed
    total = 0

    for frame in range(10):
        if frame < 9:
            # ── Frames 1–9 ──────────────────────────────────────────
            if rolls[cursor] == 10:          # strike
                total += 10 + rolls[cursor + 1] + rolls[cursor + 2]
                cursor += 1                  # one roll consumed this frame
            elif rolls[cursor] + rolls[cursor + 1] == 10:  # spare
                total += 10 + rolls[cursor + 2]
                cursor += 2
            else:                            # open frame
                total += rolls[cursor] + rolls[cursor + 1]
                cursor += 2
        else:
            # ── Frame 10 ────────────────────────────────────────────
            # Score is simply the sum of all rolls in this frame
            # (bonus rolls are already appended; no extra bonus applies).
            total += sum(rolls[cursor:])

    return total


# ── Validation helpers ───────────────────────────────────────────────────────

def _validate(rolls):
    """Raise ValueError for any impossible bowling sequence."""
    if not isinstance(rolls, list):
        raise ValueError("rolls must be a list")

    cursor = 0

    for frame in range(10):
        _check_cursor(cursor, rolls, frame)

        first = rolls[cursor]
        _check_pin(first, "first roll of frame")

        if frame < 9:
            if first == 10:                  # strike – one roll this frame
                cursor += 1
            else:
                _check_cursor(cursor + 1, rolls, frame)
                second = rolls[cursor + 1]
                _check_pin(second, "second roll of frame")
                if first + second > 10:
                    raise ValueError(
                        "Pin count exceeds pins on the lane"
                    )
                cursor += 2
        else:
            # 10th frame: validate all remaining rolls
            _validate_tenth_frame(rolls, cursor)
            cursor = len(rolls)   # consume everything

    if cursor != len(rolls):
        raise ValueError("Cannot roll after game is over")


def _validate_tenth_frame(rolls, start):
    """Validate rolls from `start` through end-of-list as the 10th frame."""
    remaining = rolls[start:]

    if not remaining:
        raise ValueError("Score cannot be taken until the end of the game")

    first = remaining[0]
    _check_pin(first, "10th-frame first roll")

    if first == 10:                          # strike → need 2 more rolls
        if len(remaining) < 3:
            raise ValueError("Score cannot be taken until the end of the game")
        if len(remaining) > 3:
            raise ValueError("Cannot roll after game is over")

        second = remaining[1]
        third  = remaining[2]
        _check_pin(second, "10th-frame second roll")
        _check_pin(third,  "10th-frame third roll")

        if second == 10:                     # second is also a strike → third 0-10
            pass                             # already validated by _check_pin
        elif second + third > 10:
            raise ValueError("Pin count exceeds pins on the lane")

    else:                                    # no strike on first ball
        if len(remaining) < 2:
            raise ValueError("Score cannot be taken until the end of the game")

        second = remaining[1]
        _check_pin(second, "10th-frame second roll")

        if first + second > 10:
            raise ValueError("Pin count exceeds pins on the lane")

        if first + second == 10:             # spare → one bonus roll
            if len(remaining) < 3:
                raise ValueError(
                    "Score cannot be taken until the end of the game"
                )
            if len(remaining) > 3:
                raise ValueError("Cannot roll after game is over")
            third = remaining[2]
            _check_pin(third, "10th-frame bonus roll")
        else:                                # open frame → no bonus roll
            if len(remaining) > 2:
                raise ValueError("Cannot roll after game is over")


def _check_pin(value, label="roll"):
    if value < 0:
        raise ValueError(f"Negative pins not allowed ({label})")
    if value > 10:
        raise ValueError(f"Pin count exceeds pins on the lane ({label})")


def _check_cursor(cursor, rolls, frame):
    if cursor >= len(rolls):
        raise ValueError(
            f"Score cannot be taken until the end of the game "
            f"(missing rolls for frame {frame + 1})"
        )
