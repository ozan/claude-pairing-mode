class BowlingGame:
    def __init__(self):
        self.rolls = []
        self._game_over = False
        self._current_frame = 1
        self._rolls_in_frame = 0
        self._frame_first_roll = 0  # pins on first roll of current frame
        self._tenth_first_was_strike = False

    def roll(self, pins):
        if self._game_over:
            raise Exception("Game is already over, cannot add more rolls")
        if pins < 0 or pins > 10:
            raise Exception(f"Invalid number of pins: {pins}")

        self.rolls.append(pins)
        self._advance_state(pins)

    def _advance_state(self, pins):
        """Track frame position to detect when the game ends."""
        frame = self._current_frame
        roll_in = self._rolls_in_frame  # 0-indexed position within the frame

        if frame < 10:
            if roll_in == 0:
                if pins == 10:  # strike
                    self._current_frame += 1
                    # _rolls_in_frame stays 0
                else:
                    self._frame_first_roll = pins
                    self._rolls_in_frame = 1
            else:  # roll_in == 1
                if self._frame_first_roll + pins > 10:
                    raise Exception("Pin count exceeds pins on the lane")
                self._rolls_in_frame = 0
                self._frame_first_roll = 0
                self._current_frame += 1

        else:  # 10th frame — up to 3 rolls
            if roll_in == 0:
                self._frame_first_roll = pins
                self._rolls_in_frame = 1
            elif roll_in == 1:
                if self._frame_first_roll == 10:
                    # First was a strike; second can be 0-10
                    self._tenth_first_was_strike = True
                    self._rolls_in_frame = 2
                    self._frame_first_roll = pins  # track second roll for validation
                elif self._frame_first_roll + pins == 10:
                    # Spare — gets a bonus roll
                    self._rolls_in_frame = 2
                else:
                    # Open frame — game over after this roll
                    if self._frame_first_roll + pins > 10:
                        raise Exception("Pin count exceeds pins on the lane")
                    self._game_over = True
            else:  # roll_in == 2 (bonus roll)
                if self._tenth_first_was_strike and self._frame_first_roll != 10:
                    # Strike then non-strike: pins reset but were partially knocked down.
                    # second + third must not exceed 10.
                    if self._frame_first_roll + pins > 10:
                        raise Exception("Pin count exceeds pins on the lane")
                self._game_over = True

    def score(self):
        if not self._game_over:
            raise Exception("Score cannot be taken until the end of the game")

        total = 0
        i = 0

        for _frame in range(10):
            if self.rolls[i] == 10:  # strike
                total += 10 + self.rolls[i + 1] + self.rolls[i + 2]
                i += 1
            elif self.rolls[i] + self.rolls[i + 1] == 10:  # spare
                total += 10 + self.rolls[i + 2]
                i += 2
            else:
                total += self.rolls[i] + self.rolls[i + 1]
                i += 2

        return total
