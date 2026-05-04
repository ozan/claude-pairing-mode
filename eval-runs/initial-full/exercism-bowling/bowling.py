class BowlingGame:
    def __init__(self):
        self._rolls = []
        self._frame = 0
        self._roll_in_frame = 0
        self._first_pins = 0
        self._second_pins = 0
        self._game_over = False

    def roll(self, pins):
        if self._game_over:
            raise Exception("Cannot roll after game is over")
        if pins < 0 or pins > 10:
            raise Exception("Invalid pin count")
        self._rolls.append(pins)

        if self._frame < 9:                          # frames 1–9
            if self._roll_in_frame == 0:
                if pins == 10:                       # strike
                    self._frame += 1
                else:
                    self._first_pins = pins
                    self._roll_in_frame = 1
            else:
                if self._first_pins + pins > 10:
                    raise Exception("Pin count exceeds pins on lane")
                self._frame += 1
                self._roll_in_frame = 0
        else:                                        # 10th frame
            if self._roll_in_frame == 0:
                self._first_pins = pins
                self._roll_in_frame = 1
            elif self._roll_in_frame == 1:
                if self._first_pins != 10 and self._first_pins + pins > 10:
                    raise Exception("Pin count exceeds pins on lane")
                self._second_pins = pins
                self._roll_in_frame = 2
                if self._first_pins < 10 and self._first_pins + pins < 10:
                    self._game_over = True           # open frame, done
            else:                                    # bonus roll
                if self._first_pins == 10 and self._second_pins < 10:
                    if self._second_pins + pins > 10:
                        raise Exception("Pin count exceeds pins on lane")
                self._game_over = True

    def score(self):
        if not self._game_over:
            raise Exception("Score cannot be taken until the end of the game")
        total = 0
        i = 0
        for frame in range(10):
            if frame == 9:
                total += sum(self._rolls[i:])
            elif self._rolls[i] == 10:              # strike
                total += 10 + self._rolls[i+1] + self._rolls[i+2]
                i += 1
            elif self._rolls[i] + self._rolls[i+1] == 10:  # spare
                total += 10 + self._rolls[i+2]
                i += 2
            else:
                total += self._rolls[i] + self._rolls[i+1]
                i += 2
        return total
