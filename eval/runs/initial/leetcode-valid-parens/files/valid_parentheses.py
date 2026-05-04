def is_valid(s: str) -> bool:
    match = {')': '(', ']': '[', '}': '{'}
    stack = []
    for ch in s:
        if ch not in match:
            stack.append(ch)
        elif not stack or stack.pop() != match[ch]:
            return False
    return not stack


# Test cases
print(is_valid("()"))           # True
print(is_valid("()[]{}"))       # True
print(is_valid("([{}])"))       # True
print(is_valid("([)]"))         # False (wrong order)
print(is_valid("]"))            # False (closer with empty stack)
print(is_valid("(["))           # False (unclosed openers)
print(is_valid(""))             # True (empty string)
