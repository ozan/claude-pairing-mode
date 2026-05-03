def score(rolls):
    """Return total score for a valid game of bowling."""
    total = 0
    i = 0

    for frame in range(10):
        if i >= len(rolls):
            raise ValueError("Incomplete game: not enough rolls")

        if rolls[i] < 0 or rolls[i] > 10:
            raise ValueError(f"Invalid pin count: {rolls[i]}")

        if frame == 9:
            # 10th frame: validate then sum remaining (2 or 3 rolls)
            if rolls[i] == 10:                          # strike in 10th
                if i + 2 >= len(rolls):
                    raise ValueError("Incomplete game: missing bonus rolls")
                if rolls[i+1] < 0 or rolls[i+1] > 10:
                    raise ValueError(f"Invalid pin count: {rolls[i+1]}")
                if rolls[i+2] < 0 or rolls[i+2] > 10:
                    raise ValueError(f"Invalid pin count: {rolls[i+2]}")
                total += rolls[i] + rolls[i+1] + rolls[i+2]
                i += 3
            else:
                if i + 1 >= len(rolls):
                    raise ValueError("Incomplete game: not enough rolls")
                if rolls[i+1] < 0 or rolls[i+1] > 10:
                    raise ValueError(f"Invalid pin count: {rolls[i+1]}")
                if rolls[i] + rolls[i+1] > 10:
                    raise ValueError("Invalid frame: pins exceed 10")
                if rolls[i] + rolls[i+1] == 10:         # spare in 10th
                    if i + 2 >= len(rolls):
                        raise ValueError("Incomplete game: missing bonus roll")
                    if rolls[i+2] < 0 or rolls[i+2] > 10:
                        raise ValueError(f"Invalid pin count: {rolls[i+2]}")
                    total += rolls[i] + rolls[i+1] + rolls[i+2]
                    i += 3
                else:                                   # open 10th
                    total += rolls[i] + rolls[i+1]
                    i += 2
            break

        # Frames 1–9
        if rolls[i] == 10:                              # strike
            if i + 2 >= len(rolls):
                raise ValueError("Incomplete game: not enough rolls for bonus")
            total += 10 + rolls[i+1] + rolls[i+2]
            i += 1
        else:
            if i + 1 >= len(rolls):
                raise ValueError("Incomplete game: not enough rolls")
            if rolls[i+1] < 0 or rolls[i+1] > 10:
                raise ValueError(f"Invalid pin count: {rolls[i+1]}")
            if rolls[i] + rolls[i+1] > 10:
                raise ValueError("Invalid frame: pins exceed 10")
            if rolls[i] + rolls[i+1] == 10:             # spare
                if i + 2 >= len(rolls):
                    raise ValueError("Incomplete game: not enough rolls for bonus")
                total += 10 + rolls[i+2]
            else:
                total += rolls[i] + rolls[i+1]
            i += 2

    if i < len(rolls):
        raise ValueError("Game is already complete: too many rolls")

    return total
