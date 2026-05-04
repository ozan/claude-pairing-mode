def _check_pin(n):
    if not 0 <= n <= 10:
        raise ValueError("Invalid pin count")


def validate(rolls):
    i = 0

    # Frames 0–8
    for frame in range(9):
        try:
            first = rolls[i]
        except IndexError:
            raise ValueError("Not enough rolls")

        _check_pin(first)

        if first == 10:  # strike
            i += 1
        else:
            try:
                second = rolls[i + 1]
            except IndexError:
                raise ValueError("Not enough rolls")

            _check_pin(second)
            if first + second > 10:
                raise ValueError("Frame total exceeds 10")

            i += 2

    # 10th frame
    try:
        first_10 = rolls[i]
    except IndexError:
        raise ValueError("Not enough rolls")

    _check_pin(first_10)

    if first_10 == 10:  # strike in 10th
        try:
            second_10 = rolls[i + 1]
            third_10 = rolls[i + 2]
        except IndexError:
            raise ValueError("Not enough rolls")

        _check_pin(second_10)
        _check_pin(third_10)
        if second_10 != 10 and second_10 + third_10 > 10:
            raise ValueError("Pin count exceeds pins on the lane")

        i += 3
    else:
        try:
            second_10 = rolls[i + 1]
        except IndexError:
            raise ValueError("Not enough rolls")

        _check_pin(second_10)

        if first_10 + second_10 == 10:  # spare in 10th
            try:
                third_10 = rolls[i + 2]
            except IndexError:
                raise ValueError("Not enough rolls")

            _check_pin(third_10)
            i += 3
        else:  # open in 10th
            if first_10 + second_10 > 10:
                raise ValueError("Frame total exceeds 10")
            i += 2

    if i != len(rolls):
        raise ValueError("Too many rolls")


def score(rolls):
    validate(rolls)
    i = 0
    total = 0
    for frame in range(9):
        if rolls[i] == 10:                          # strike
            total += rolls[i] + rolls[i+1] + rolls[i+2]
            i += 1
        elif rolls[i] + rolls[i+1] == 10:           # spare
            total += rolls[i] + rolls[i+1] + rolls[i+2]
            i += 2
        else:                                        # open
            total += rolls[i] + rolls[i+1]
            i += 2
    total += sum(rolls[i:])                          # 10th frame: sum remaining
    return total
