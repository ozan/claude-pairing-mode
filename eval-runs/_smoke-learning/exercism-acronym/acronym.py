import re

def abbreviate(words):
    result = []
    for token in re.split(r'[\s\-]+', words):           # spaces & hyphens are separators
        token = re.sub(r'^[^a-zA-Z]+|[^a-zA-Z]+$', '', token)  # strip leading/trailing punctuation
        if not token:
            continue
        result.append(token[0])                          # first letter of token
        for i in range(1, len(token)):                   # camelCase: uppercase after lowercase
            if token[i].isupper() and token[i - 1].islower():
                result.append(token[i])
    return ''.join(result).upper()
