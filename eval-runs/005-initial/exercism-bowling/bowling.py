def _validate(rolls: list[int]) -> None:
    if any(r < 0 or r > 10 for r in rolls):
        raise ValueError("invalid pin count")
    try:
        i = 0
        for _ in range(9):
            if rolls[i] != 10 and rolls[i] + rolls[i+1] > 10:
                raise ValueError("frame exceeds 10 pins")
            i += 1 if rolls[i] == 10 else 2
        if rolls[i] == 10:                              # 10th: strike
            if rolls[i+1] != 10 and rolls[i+1] + rolls[i+2] > 10:
                raise ValueError("bonus rolls exceed 10")
            if i + 3 != len(rolls):
                raise ValueError("wrong number of rolls")
        elif rolls[i] + rolls[i+1] == 10:              # 10th: spare
            if i + 3 != len(rolls):
                raise ValueError("wrong number of rolls")
        else:                                           # 10th: open
            if i + 2 != len(rolls):
                raise ValueError("wrong number of rolls")
    except IndexError:
        raise ValueError("incomplete game")


def score(rolls: list[int]) -> int:
    _validate(rolls)
    total = 0
    i = 0
    for _ in range(10):
        if rolls[i] == 10:          # strike
            total += rolls[i] + rolls[i+1] + rolls[i+2]
            i += 1
        elif rolls[i] + rolls[i+1] == 10:  # spare
            total += rolls[i] + rolls[i+1] + rolls[i+2]
            i += 2
        else:
            total += rolls[i] + rolls[i+1]
            i += 2
    return total
