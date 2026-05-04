def is_pangram(text):
    return set(text.lower()) >= set('abcdefghijklmnopqrstuvwxyz')
