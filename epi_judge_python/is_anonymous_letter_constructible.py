from test_framework import generic_test


from collections import Counter, defaultdict


def is_letter_constructible_from_magazine(letter_text: str, magazine_text: str) -> bool:
    # Count the characters in the magazine. Then, count the characters in the letter,
    # checking to see that there are sufficient character counts in the magazine.
    # If the count is ever insufficient (i.e., if it falls below 0), then return return False.
    # Time: O(m + n)
    # Space: O(L)
    magazine_count = defaultdict(int)
    for char in magazine_text:
        magazine_count[char] += 1

    for char in letter_text:
        magazine_count[char] -= 1
        if magazine_count[char] < 0:
            return False

    return True


def is_letter_constructible_from_magazine_epi(
    letter_text: str, magazine_text: str
) -> bool:
    # Slight optimization over my version by counting the
    # characters in the letter text, rather than the magazine text.
    # Will be especially more efficient if len(magazine) >> len(letter).
    # Time: O(m + n)
    # Space: O(L)
    letter_counter = Counter(letter_text)

    for char in magazine_text:
        if char in letter_counter:
            letter_counter[char] -= 1
            if letter_counter[char] == 0:
                del letter_counter[char]

    return not letter_counter


def is_letter_constructible_from_magazine_pythonic(
    letter_text: str, magazine_text: str
) -> bool:
    # Build a Counter for both the letter text and the magazine text.
    # If the letter is constructible, then the magazine counter will
    # be greater than or equal to the letter counter. That is,
    # every character in the magazine has a count at least equal to the corresponding
    # count in the letter.
    # Time: O(m + n)
    # Space: O(L + K),
    # where m is the number of characters in the letter,
    # n is the number of characters in the magazine,
    # L is the number of unique characters in the magazine,
    # and K is the number of unique characters in the letter.
    return Counter(magazine_text) >= Counter(letter_text)


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "is_anonymous_letter_constructible.py",
            "is_anonymous_letter_constructible.tsv",
            is_letter_constructible_from_magazine,
        )
    )
