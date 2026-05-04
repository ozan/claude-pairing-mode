"""10-pin bowling scorer (Exercism exercise)."""


class BowlingGame:
    """Track rolls and compute the final score of a 10-pin bowling game.

    Rules summary
    -------------
    * A game has 10 frames; each frame normally has up to 2 rolls.
    * **Strike** (10 pins on the first roll of a frame): frame score is
      10 + the next *two* rolls as a bonus.  Only one roll is consumed for
      the frame itself, so the index advances by 1.
    * **Spare** (10 pins across the two rolls of a frame): frame score is
      10 + the next *one* roll as a bonus.  Index advances by 2.
    * **Open frame**: frame score is simply the sum of both rolls.
    * **10th-frame bonus rolls**: if the 10th frame is a strike or spare the
      bowler gets 1 or 2 extra rolls *only* to fulfil the bonus — they do not
      start a new frame.  The bonus rolls are already included naturally by the
      look-ahead logic used for frames 1-10.
    """

    def __init__(self) -> None:
        self._rolls: list[int] = []
        self._done: bool = False

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def roll(self, pins: int) -> None:
        """Record a single roll.

        Raises
        ------
        ValueError
            If the roll is invalid (negative pins, more pins than remain on
            the lane, or rolling after the game is already complete).
        """
        if self._done:
            raise ValueError("Cannot roll after the game is over.")
        if pins < 0:
            raise ValueError(f"Negative pin count is invalid: {pins}.")
        if pins > 10:
            raise ValueError(f"Pin count exceeds 10: {pins}.")

        # Validate within the current frame context before appending.
        self._validate_mid_frame(pins)

        self._rolls.append(pins)

        # Check whether the game has reached its natural end.
        if self._game_over():
            self._done = True

    def score(self) -> int:
        """Return the final score.

        Raises
        ------
        ValueError
            If the game is incomplete (not enough rolls recorded yet).
        """
        if not self._done:
            raise ValueError("Score cannot be taken until the end of the game.")

        total = 0
        idx = 0  # current position in the rolls list

        for frame in range(10):
            if idx >= len(self._rolls):
                # Should never happen for a valid completed game, but guard anyway.
                raise ValueError("Score cannot be taken until the end of the game.")

            if self._rolls[idx] == 10:                           # ── strike ──
                total += 10 + self._rolls[idx + 1] + self._rolls[idx + 2]
                idx += 1
            elif self._rolls[idx] + self._rolls[idx + 1] == 10:  # ── spare ──
                total += 10 + self._rolls[idx + 2]
                idx += 2
            else:                                                 # ── open ──
                total += self._rolls[idx] + self._rolls[idx + 1]
                idx += 2

        return total

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _validate_mid_frame(self, pins: int) -> None:
        """Raise ValueError if *pins* would make the current in-progress
        frame invalid (e.g. two rolls that exceed 10 outside the 10th frame).
        """
        frame, pos_in_frame, _ = self._current_frame_info()

        if frame < 9:
            # Frames 1-9: two rolls may not exceed 10 (strikes use only 1 roll).
            if pos_in_frame == 1:
                first = self._rolls[-1]  # the roll already recorded this frame
                if first + pins > 10:
                    raise ValueError(
                        f"Pin count exceeds pins on the lane: {first} + {pins} > 10."
                    )
        else:
            # 10th frame has more complex rules.
            self._validate_tenth_frame(pins)

    def _validate_tenth_frame(self, pins: int) -> None:
        """Validate a roll that falls inside the 10th frame."""
        tenth_rolls = self._tenth_frame_rolls()
        n = len(tenth_rolls)

        if n == 0:
            return  # first roll of the 10th — only the >10 check already applies

        if n == 1:
            first = tenth_rolls[0]
            if first == 10:
                return  # after a strike the lane is reset: 0-10 all valid
            if first + pins > 10:
                raise ValueError(
                    f"Pin count exceeds pins on the lane in 10th frame: "
                    f"{first} + {pins} > 10."
                )

        elif n == 2:
            first, second = tenth_rolls[0], tenth_rolls[1]
            # Third roll only allowed after a strike or spare.
            if first == 10:
                # Strike: second roll might itself be a strike (lane reset) or not.
                if second == 10:
                    return  # double strike — fill ball can be 0-10
                # Non-strike second ball: fill ball must not exceed 10 - second.
                if second + pins > 10:
                    raise ValueError(
                        f"Pin count exceeds pins on the lane in 10th frame fill: "
                        f"{second} + {pins} > 10."
                    )
            elif first + second == 10:
                return  # spare — fill ball resets the lane, 0-10 valid

    def _current_frame_info(self) -> tuple[int, int, int]:
        """Return ``(frame_index, roll_index_within_frame, roll_list_offset)``.

        *frame_index* is 0-based (0-8 for frames 1-9, 9 for the 10th).
        *roll_index_within_frame* is how many rolls have been consumed in the
        current (incomplete) frame.
        *roll_list_offset* is the index into ``self._rolls`` where the current
        frame starts.
        """
        idx = 0
        for frame in range(9):  # frames 0-8
            if idx >= len(self._rolls):
                return frame, 0, idx
            if self._rolls[idx] == 10:  # strike — frame done in one roll
                idx += 1
            else:
                if idx + 1 >= len(self._rolls):
                    return frame, 1, idx  # mid-frame: one roll recorded
                idx += 2  # both rolls recorded, frame complete

        # We are in the 10th frame (index 9).
        tenth_rolls = len(self._rolls) - idx
        return 9, tenth_rolls, idx

    def _tenth_frame_rolls(self) -> list[int]:
        """Return the rolls recorded so far in the 10th frame."""
        _, _, offset = self._current_frame_info()
        return self._rolls[offset:]

    def _game_over(self) -> bool:
        """Return True when a complete, valid game has been recorded."""
        frame, _, offset = self._current_frame_info()
        if frame < 9:
            return False

        tenth = self._rolls[offset:]
        n = len(tenth)
        if n < 2:
            return False

        first, second = tenth[0], tenth[1]
        strike = first == 10
        spare = (not strike) and (first + second == 10)

        if strike or spare:
            return n == 3  # bonus roll required
        return n == 2      # open 10th frame — done


# ---------------------------------------------------------------------------
# Functional convenience wrapper
# ---------------------------------------------------------------------------

def score(rolls: list[int]) -> int:
    """Compute the bowling score from a complete list of rolls.

    Parameters
    ----------
    rolls:
        Ordered list of pin counts for an entire game.

    Returns
    -------
    int
        The final score (0-300).

    Raises
    ------
    ValueError
        If the roll sequence is invalid or incomplete.
    """
    game = BowlingGame()
    for pins in rolls:
        game.roll(pins)
    return game.score()
