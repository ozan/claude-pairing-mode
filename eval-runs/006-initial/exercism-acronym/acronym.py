import re


def abbreviate(words):
    tokens = re.split(r'[\s-]+', words)
    return ''.join(re.search(r'[A-Za-z]', t).group()
                   for t in tokens if re.search(r'[A-Za-z]', t)).upper()
