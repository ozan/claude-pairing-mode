import re

def abbreviate(words):
    return ''.join(m.upper()
                   for m in re.findall(r'\b[a-zA-Z]|(?<=[a-z])[A-Z]', words))
