"""10-pin bowling scorer.

Scoring rules
-------------
* A game is exactly 10 frames.
* Frame 1-9:
    - Strike  (first roll = 10): score = 10 + next two rolls; only 1 roll used
      in the frame.
    - Spare   (two rolls = 10): score = 10 + next one roll; 2 rolls used.
    - Open    (two rolls < 10): score = sum of both rolls; 2 rolls used.
* Frame 10 (bonus-roll frame):
    - Strike on first roll  → 2 extra rolls allowed.
    - Spare  on first+second → 1 extra roll  allowed.
    - Open                  → no extra rolls.
* Total pins in a non-bonus roll of a single frame cannot exceed 10.
"""


class BowlingGame:
    """Mutable game object: feed rolls one at a time, then read .score."""

    def __init__(self):
        self._rolls: list[int] = []
        self._done = False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def roll(self, pins: int) -> None:
        """Record a single roll of *pins* knocked-down pins."""
        if self._done:
            raise ValueError("Cannot roll after the game is over")
        if not isinstance(pins, int) or pins < 0:
            raise ValueError(f"Pins must be a non-negative integer, got {pins!r}")
        if pins > 10:
            raise ValueError(f"Pin count exceeds pins on the lane: {pins}")

        self._rolls.append(pins)

        # Re-validate the whole roll sequence every time so we catch illegal
        # states (e.g. two rolls in a frame summing > 10) as early as possible.
        _validate(self._rolls, partial=True)

        if _game_complete(self._rolls):
            self._done = True

    @property
    def score(self) -> int:
        """Return the final score.  Raises ValueError if the game is incomplete."""
        if not _game_complete(self._rolls):
            raise ValueError("Score cannot be taken until the end of the game")
        return _score(self._rolls)


# ---------------------------------------------------------------------------
# Functional API (score a finished list of rolls directly)
# ---------------------------------------------------------------------------

def score(rolls: list[int]) -> int:
    """Score a complete bowling game given a flat list of rolls.

    Args:
        rolls: sequence of pin counts, one entry per roll.

    Returns:
        The integer total score (0–300).

    Raises:
        ValueError: for any invalid roll sequence.
    """
    _validate(rolls, partial=False)
    if not _game_complete(rolls):
        raise ValueError("Score cannot be taken until the end of the game")
    return _score(rolls)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _score(rolls: list[int]) -> int:
    """Compute the score; assumes *rolls* has already been validated."""
    total = 0
    idx = 0  # current position in the rolls list

    for frame in range(10):
        if frame < 9:
            if rolls[idx] == 10:                          # strike
                total += 10 + rolls[idx + 1] + rolls[idx + 2]
                idx += 1
            elif rolls[idx] + rolls[idx + 1] == 10:       # spare
                total += 10 + rolls[idx + 2]
                idx += 2
            else:                                          # open frame
                total += rolls[idx] + rolls[idx + 1]
                idx += 2
        else:
            # 10th frame: just sum whatever bonus rolls were awarded.
            total += sum(rolls[idx:])

    return total


def _validate(rolls: list[int], *, partial: bool = False) -> None:
    """Walk through the roll list frame-by-frame and raise ValueError on any
    rule violation.

    When *partial* is True the sequence may be incomplete (mid-game), so we
    only check frames for which we have enough data.
    """
    # Check every individual roll value first.
    for pin in rolls:
        if pin < 0:
            raise ValueError(f"Negative pin count is not allowed: {pin}")
        if pin > 10:
            raise ValueError(f"Pin count exceeds pins on the lane: {pin}")

    idx = 0

    for frame in range(10):
        # Not enough rolls yet — only OK in partial mode.
        if idx >= len(rolls):
            if partial:
                return
            raise ValueError("Score cannot be taken until the end of the game")

        if frame < 9:
            # ---- Frames 1-9 ------------------------------------------------
            first = rolls[idx]

            if first == 10:                               # strike
                idx += 1
                # We need two more rolls for the bonus but only validate
                # them when they exist (partial mode) or must exist (full).
                if idx + 1 < len(rolls):
                    b1, b2 = rolls[idx], rolls[idx + 1]
                    if b1 > 10:
                        raise ValueError(
                            f"Pin count exceeds pins on the lane: {b1}"
                        )
                    if b1 < 10 and b1 + b2 > 10:
                        raise ValueError(
                            f"Pin count exceeds pins on the lane: {b1 + b2}"
                        )
            else:
                # Need the second roll of this frame.
                if idx + 1 >= len(rolls):
                    if partial:
                        return
                    raise ValueError(
                        "Score cannot be taken until the end of the game"
                    )
                second = rolls[idx + 1]
                if first + second > 10:
                    raise ValueError(
                        f"Pin count exceeds pins on the lane: {first + second}"
                    )
                idx += 2

        else:
            # ---- Frame 10 --------------------------------------------------
            # Determine how many rolls the 10th frame is entitled to.
            if idx >= len(rolls):
                if partial:
                    return
                raise ValueError(
                    "Score cannot be taken until the end of the game"
                )

            r1 = rolls[idx]

            if r1 == 10:                                  # strike on roll 1
                # Need rolls idx+1 and idx+2
                if idx + 2 >= len(rolls):
                    if partial:
                        return
                    raise ValueError(
                        "Score cannot be taken until the end of the game"
                    )
                r2 = rolls[idx + 1]
                r3 = rolls[idx + 2]
                if r2 > 10:
                    raise ValueError(
                        f"Pin count exceeds pins on the lane: {r2}"
                    )
                if r2 == 10:                              # second roll also strike
                    if r3 > 10:
                        raise ValueError(
                            f"Pin count exceeds pins on the lane: {r3}"
                        )
                else:
                    if r2 + r3 > 10:
                        raise ValueError(
                            f"Pin count exceeds pins on the lane: {r2 + r3}"
                        )
                # No rolls should follow.
                if idx + 3 < len(rolls):
                    raise ValueError("Cannot roll after the game is over")
            else:
                # Non-strike first roll in 10th.
                if idx + 1 >= len(rolls):
                    if partial:
                        return
                    raise ValueError(
                        "Score cannot be taken until the end of the game"
                    )
                r2 = rolls[idx + 1]
                if r1 + r2 > 10:
                    raise ValueError(
                        f"Pin count exceeds pins on the lane: {r1 + r2}"
                    )
                if r1 + r2 == 10:                         # spare → one bonus roll
                    if idx + 2 >= len(rolls):
                        if partial:
                            return
                        raise ValueError(
                            "Score cannot be taken until the end of the game"
                        )
                    r3 = rolls[idx + 2]
                    if r3 > 10:
                        raise ValueError(
                            f"Pin count exceeds pins on the lane: {r3}"
                        )
                    if idx + 3 < len(rolls):
                        raise ValueError("Cannot roll after the game is over")
                else:                                      # open → no bonus rolls
                    if idx + 2 < len(rolls):
                        raise ValueError("Cannot roll after the game is over")


def _game_complete(rolls: list[int]) -> bool:
    """Return True only when the roll list represents a finished game."""
    idx = 0
    for frame in range(10):
        if idx >= len(rolls):
            return False

        if frame < 9:
            if rolls[idx] == 10:
                idx += 1
            else:
                if idx + 1 >= len(rolls):
                    return False
                idx += 2
        else:
            # 10th frame
            if idx >= len(rolls):
                return False
            r1 = rolls[idx]
            if r1 == 10:
                return idx + 2 < len(rolls)
            if idx + 1 >= len(rolls):
                return False
            r2 = rolls[idx + 1]
            if r1 + r2 == 10:
                return idx + 2 < len(rolls)
            return True   # open 10th frame — 2 rolls suffice

    return False
