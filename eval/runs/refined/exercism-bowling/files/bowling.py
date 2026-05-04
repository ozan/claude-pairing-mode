def _walk_frames(rolls):
    """Yields (frame_score, next_roll_index) for each of 10 frames."""
    i = 0
    for frame in range(10):
        if frame < 9:
            if rolls[i] == 10:                        # strike
                score = 10 + rolls[i + 1] + rolls[i + 2]
                i += 1
            elif rolls[i] + rolls[i + 1] == 10:       # spare
                score = 10 + rolls[i + 2]
                i += 2
            else:                                      # open
                score = rolls[i] + rolls[i + 1]
                i += 2
        else:                                          # 10th frame
            score = sum(rolls[i:])
            i = len(rolls)
        yield (score, i)


def _validate(rolls):
    i = 0
    for frame in range(10):
        if frame < 9:
            if rolls[i] < 0 or rolls[i] > 10:
                raise ValueError(f"invalid roll: {rolls[i]}")
            if rolls[i] == 10:                        # strike
                i += 1
            else:
                if rolls[i + 1] < 0 or rolls[i + 1] > 10:
                    raise ValueError(f"invalid roll: {rolls[i + 1]}")
                if rolls[i] + rolls[i + 1] > 10:
                    raise ValueError("pin count exceeds pins on the lane")
                i += 2
        else:                                          # 10th frame
            r = rolls[i:]
            if len(r) < 2:
                raise ValueError("too few rolls in 10th frame")
            if r[0] < 0 or r[0] > 10:
                raise ValueError(f"invalid roll: {r[0]}")
            if r[1] < 0 or r[1] > 10:
                raise ValueError(f"invalid roll: {r[1]}")
            if r[0] == 10:                             # strike: 2 bonus rolls
                if len(r) != 3:
                    raise ValueError("wrong number of bonus rolls")
                if r[2] < 0 or r[2] > 10:
                    raise ValueError(f"invalid roll: {r[2]}")
                if r[1] != 10 and r[1] + r[2] > 10:
                    raise ValueError("pin count exceeds pins on the lane")
            elif r[0] + r[1] == 10:                   # spare: 1 bonus roll
                if len(r) != 3:
                    raise ValueError("wrong number of bonus rolls")
                if r[2] < 0 or r[2] > 10:
                    raise ValueError(f"invalid roll: {r[2]}")
            else:                                      # open: no bonus
                if r[0] + r[1] > 10:
                    raise ValueError("pin count exceeds pins on the lane")
                if len(r) != 2:
                    raise ValueError("too many rolls in 10th frame")


def score(rolls):
    _validate(rolls)
    return sum(s for s, _ in _walk_frames(rolls))
