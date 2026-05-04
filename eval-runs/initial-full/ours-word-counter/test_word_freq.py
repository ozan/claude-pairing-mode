from word_freq import word_frequency


def test_basic():
    assert word_frequency("hello world") == {'hello': 1, 'world': 1}


def test_repeated_words():
    assert word_frequency("the the the") == {'the': 3}


def test_punctuation_and_case():
    assert word_frequency("Hello, world!") == {'hello': 1, 'world': 1}


def test_mid_word_punctuation():
    assert word_frequency("It's-a me!") == {'it': 1, 's': 1, 'a': 1, 'me': 1}
