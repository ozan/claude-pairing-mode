# =============================================================================
# Sliding Window Practice
# =============================================================================
# Fill in the two functions below, then run:
#   python sliding_window.py
#
# You'll see PASS / FAIL for each test case.
# Don't peek at the other function while solving the first!
# =============================================================================


# -----------------------------------------------------------------------------
# Problem 1: Longest Substring Without Repeating Characters (LeetCode #3)
#
# Given a string s, return the length of the longest substring where
# every character is unique.
#
# Examples:
#   "abcabcbb" → 3   ("abc")
#   "bbbbb"    → 1   ("b")
#   "pwwkew"   → 3   ("wke")
# -----------------------------------------------------------------------------

def length_of_longest_substring(s: str) -> int:
    pass  # your code here


# -----------------------------------------------------------------------------
# Problem 2: Longest Substring With At Most K Distinct Characters
#
# Given a string s and integer k, return the length of the longest substring
# that contains at most k *distinct* characters.
#
# Examples:
#   "eceba",  k=2 → 3   ("ece")
#   "aabbcc", k=2 → 4   ("aabb" or "bbcc")
#   "abc",    k=1 → 1   ("a" or "b" or "c")
#
# Hint: how does your window shrink condition change compared to Problem 1?
# -----------------------------------------------------------------------------

def longest_k_distinct(s: str, k: int) -> int:
    pass  # your code here


# =============================================================================
# Test harness — don't modify below this line
# =============================================================================

def run_tests():
    results = []

    def check(label, got, expected):
        status = "PASS" if got == expected else "FAIL"
        results.append((status, label, got, expected))

    # --- Problem 1 tests ---
    check("p1: standard",        length_of_longest_substring("abcabcbb"), 3)
    check("p1: all same",        length_of_longest_substring("bbbbb"),    1)
    check("p1: end window",      length_of_longest_substring("pwwkew"),   3)
    check("p1: all unique",      length_of_longest_substring("abcdef"),   6)
    check("p1: empty string",    length_of_longest_substring(""),         0)
    check("p1: single char",     length_of_longest_substring("z"),        1)
    check("p1: dvdf",            length_of_longest_substring("dvdf"),     3)

    # --- Problem 2 tests ---
    check("p2: eceba k=2",       longest_k_distinct("eceba",  k=2),  3)
    check("p2: aabbcc k=2",      longest_k_distinct("aabbcc", k=2),  4)
    check("p2: all same k=1",    longest_k_distinct("aaaa",   k=1),  4)
    check("p2: abc k=1",         longest_k_distinct("abc",    k=1),  1)
    check("p2: k=0",             longest_k_distinct("abc",    k=0),  0)
    check("p2: empty string",    longest_k_distinct("",       k=2),  0)
    check("p2: k >= all unique", longest_k_distinct("abcde",  k=10), 5)

    # --- Report ---
    print()
    passed = sum(1 for r in results if r[0] == "PASS")
    total  = len(results)

    for status, label, got, expected in results:
        if status == "PASS":
            print(f"  ✓  {label}")
        else:
            print(f"  ✗  {label}")
            print(f"       expected {expected}, got {got}")

    print()
    print(f"  {passed}/{total} tests passed")
    print()


if __name__ == "__main__":
    run_tests()
