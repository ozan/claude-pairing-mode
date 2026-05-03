from collections import Counter

def is_anagram(a: str, b: str) -> bool:
    def norm(s: str) -> str:
        return s.replace(' ', '').lower()
    return Counter(norm(a)) == Counter(norm(b))


if __name__ == '__main__':
    assert is_anagram('listen', 'silent')
    assert is_anagram('Listen', 'Silent')
    assert is_anagram('conversation', 'voices rant on')
    assert not is_anagram('hello', 'world')
    assert not is_anagram('aabb', 'abbb')   # same letters, wrong counts
    assert not is_anagram('abc', 'abcd')    # length mismatch
    assert is_anagram('', '')               # both empty
    print('ok')
