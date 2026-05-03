def is_balanced(s: str) -> bool:
    """Return True if brackets in s are balanced and properly nested."""
    EXPECTED = {'(': ')', '[': ']', '{': '}'}
    stack: list[str] = []
    for c in s:
        if c in EXPECTED:
            stack.append(EXPECTED[c])
        else:
            if not stack or stack.pop() != c:
                return False
    return not stack


if __name__ == "__main__":
    cases = [
        ("", True),
        ("()", True),
        ("([])", True),
        ("([)]", False),
        ("(", False),
        (")", False),
        ("{[()]}", True),
        ("{[(])}", False),
    ]
    for s, want in cases:
        got = is_balanced(s)
        assert got == want, f"{s!r}: want {want}, got {got}"
    print(f"ok ({len(cases)} cases)")
