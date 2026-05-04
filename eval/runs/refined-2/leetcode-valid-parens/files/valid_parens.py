def is_valid(s: str) -> bool:
    match = {'(': ')', '[': ']', '{': '}'}
    stack = []

    for char in s:
        if char in match:
            stack.append(match[char])
        elif not stack or stack.pop() != char:
            return False

    return not stack


# --- tests ---
assert is_valid("()")
assert is_valid("()[]{}")
assert is_valid("{[]}")
assert not is_valid("(]")
assert not is_valid("([)]")
assert not is_valid("(")
assert not is_valid(")")
print("all tests passed")
