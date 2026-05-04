def encode(text, shift):
    result = []
    for ch in text:
        if ch.isupper():
            result.append(chr((ord(ch) - ord('A') + shift) % 26 + ord('A')))
        elif ch.islower():
            result.append(chr((ord(ch) - ord('a') + shift) % 26 + ord('a')))
        else:
            result.append(ch)
    return ''.join(result)


def decode(text, shift):
    return encode(text, -shift)


if __name__ == "__main__":
    import string
    for shift in range(27):
        for text in ["Hello, World!", string.printable]:
            assert decode(encode(text, shift), shift) == text
    print("All tests passed.")
