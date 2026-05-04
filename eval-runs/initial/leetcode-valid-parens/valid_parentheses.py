def is_valid(s: str) -> bool:
    stack = []
    matching = {'(': ')', '[': ']', '{': '}'}
    for char in s:
        if char in matching:
            stack.append(matching[char])
        elif not stack or stack.pop() != char:
            return False
    return not stack


if __name__ == "__main__":
    cases = [
        ("()",        True),
        ("()[]{}" ,   True),
        ("(]",        False),
        ("([)]",      False),
        ("{[]}",      True),
        (")",         False),   # closer on empty stack
        ("(((",        False),   # unclosed openers
        ("",          True),    # empty string — trivially valid
    ]
    for s, expected in cases:
        result = is_valid(s)
        status = "✓" if result == expected else "✗"
        print(f"{status}  is_valid({s!r:10}) = {result}  (expected {expected})")
