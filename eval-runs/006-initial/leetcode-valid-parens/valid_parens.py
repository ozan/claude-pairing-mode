def is_valid(s: str) -> bool:
    MATCHING = {'(': ')', '[': ']', '{': '}'}
    stack = []
    for char in s:
        if char in MATCHING:
            stack.append(MATCHING[char])
        elif not stack or char != stack.pop():
            return False
    return not stack


# Tests
assert is_valid("()")
assert is_valid("()[]{}")
assert is_valid("{[]}")
assert not is_valid("(]")
assert not is_valid("([)]")
assert not is_valid("{")       # unmatched opener
assert not is_valid(")")       # closer on empty stack
assert is_valid("")            # empty string is valid
print("All tests passed.")
