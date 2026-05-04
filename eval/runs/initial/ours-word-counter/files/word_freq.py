import re


def word_frequency(text):
    words = re.findall(r'[a-z]+', text.lower())
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq


if __name__ == "__main__":
    text = "Hello, world! Hello everyone."
    result = word_frequency(text)
    print(result)
