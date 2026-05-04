class BowlingGame:
    def __init__(self):
        self._rolls = []
        self._current_frame = 0   # 0-indexed (0–9)
        self._roll_in_frame = 0   # which roll within the current frame
        self._game_done = False

    def roll(self, pins):
        if self._game_done:
            raise Exception("Cannot roll after game is over")
        if pins < 0:
            raise Exception("Negative pins not allowed")
        if pins > 10:
            raise Exception("Pin count exceeds pins on the lane")

        if self._current_frame < 9:
            self._roll_normal_frame(pins)
        else:
            self._roll_tenth_frame(pins)

    def _roll_normal_frame(self, pins):
        if self._roll_in_frame == 1:
            if self._rolls[-1] + pins > 10:
                raise Exception("Pin count exceeds pins on the lane")
            self._rolls.append(pins)
            self._current_frame += 1
            self._roll_in_frame = 0
        else:
            self._rolls.append(pins)
            if pins == 10:          # strike — frame done in one roll
                self._current_frame += 1
            else:
                self._roll_in_frame = 1

    def _roll_tenth_frame(self, pins):
        r = self._roll_in_frame
        if r == 1:
            first = self._rolls[-1]
            if first != 10 and first + pins > 10:
                raise Exception("Pin count exceeds pins on the lane")
        elif r == 2:
            first, second = self._rolls[-2], self._rolls[-1]
            if first != 10 and first + second != 10:
                raise Exception("Cannot roll after game is over")
            # strike then non-strike: second set of pins must be ≤ 10 - second
            if first == 10 and second != 10 and second + pins > 10:
                raise Exception("Pin count exceeds pins on the lane")

        self._rolls.append(pins)
        self._roll_in_frame += 1

        if self._roll_in_frame == 2:
            first, second = self._rolls[-2], self._rolls[-1]
            if first != 10 and first + second != 10:
                self._game_done = True   # no bonus roll earned
        elif self._roll_in_frame == 3:
            self._game_done = True

    def score(self):
        if not self._game_done:
            raise Exception("Score cannot be taken until the end of the game")

        total = 0
        roll = 0
        for _ in range(10):
            if self._rolls[roll] == 10:                          # strike
                total += 10 + self._rolls[roll + 1] + self._rolls[roll + 2]
                roll += 1
            elif self._rolls[roll] + self._rolls[roll + 1] == 10:  # spare
                total += 10 + self._rolls[roll + 2]
                roll += 2
            else:
                total += self._rolls[roll] + self._rolls[roll + 1]
                roll += 2
        return total
