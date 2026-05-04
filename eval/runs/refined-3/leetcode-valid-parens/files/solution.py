def is_valid(s: str) -> bool:
    pairs = {'(': ')', '[': ']', '{': '}'}
    stack = []
    for ch in s:
        if ch in pairs:            # it's an opener
            stack.append(pairs[ch])
        elif not stack or stack.pop() != ch:
            return False
    return len(stack) == 0
