def _validate(rolls):
    idx = 0
    for _ in range(9):
        if any(r < 0 or r > 10 for r in rolls[idx:idx + 2]):
            raise Exception("Invalid pin count")
        if rolls[idx] == 10:
            idx += 1
        elif rolls[idx] + rolls[idx + 1] > 10:
            raise Exception("Pin count exceeds pins on lane")
        else:
            idx += 2
    tenth = rolls[idx:]
    is_bonus = tenth[0] == 10 or tenth[0] + tenth[1] == 10
    expected = 3 if is_bonus else 2
    if len(tenth) != expected:
        raise Exception("Wrong number of rolls in 10th frame")


def score(rolls):
    _validate(rolls)
    total = 0
    idx = 0

    for _ in range(9):  # frames 1–9
        if rolls[idx] == 10:                          # strike
            total += 10 + rolls[idx + 1] + rolls[idx + 2]
            idx += 1
        elif rolls[idx] + rolls[idx + 1] == 10:       # spare
            total += 10 + rolls[idx + 2]
            idx += 2
        else:                                          # open frame
            total += rolls[idx] + rolls[idx + 1]
            idx += 2

    # Frame 10: no new bonus frames, just add whatever rolls remain
    total += sum(rolls[idx:])
    return total
