import re


def abbreviate(phrase):
    return ''.join(
        m.group() for part in re.split(r'[\s-]+', phrase)
        if (m := re.search(r'[a-zA-Z]', part))
    ).upper()
