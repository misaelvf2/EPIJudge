from test_framework import generic_test
from test_framework.test_failure import TestFailure


def int_to_string(x: int) -> str:
    # There are a couple of tricks to keep in mind on this one.
    # It's very easy to make the mistake of reaching for str()
    # to try to convert a single digit integer to a string,
    # but that is explicitly disallowed in the instructions.
    # Instead, we have to rely on the ASCII representation of digits.
    # The other trick is the use of mod 10 to get the lowest digit
    # from an integer, and div 10 to "shift" the integer to the left.
    # Time: O(n), where n is the number of digits in x. Alternatively, O(log x).
    # Space: O(n)
    if x == 0:
        return "0"

    result = []
    parity = "-" if x < 0 else ""

    # We do this because the mod 10 trick doesn't work for negative ints.
    x = abs(x)

    while x > 0:
        # x % 10 gets the smallest digit from the number
        # chr converts a Unicode codepoint to its string representation
        # ord is the inverse operation: it converts a single-character
        # string to its Unicode codepoint
        # Digits 0-9 start at 48 in ASCII, so we have to add ord("0") as an offset.
        # Remember that ASCII is a subset of Unicode.
        digit = chr(ord("0") + x % 10)
        result.append(digit)
        # This shifts the integer to the right by one.
        x //= 10

    return parity + "".join(reversed(result))


def string_to_int(s: str) -> int:
    # Same idea as int_to_string, but in reverse, of course.
    # The most common pitfall (at least in my experience) is to
    # try to use something like Math.pow(b, x) to multiply by powers of 10,
    # which quickly becomes inaccurate.
    # The key insight is to realize that multiplying by 10 every iteration
    # achieves the same effect, only more efficiently and accurately!
    # This is analogous with dividing by 10 in the int_to_string function.
    result = 0

    if s[0] == "-":
        parity = -1
        s = s[1:]
    elif s[0] == "+":
        parity = 1
        s = s[1:]
    else:
        parity = 1

    i = 0
    while i < len(s):
        # Digits 0-9 start at 48 in ASCII, so we have to subtract ord("0") = 48
        # from the ASCII codepoint to get the actual digit.
        digit = ord(s[i]) - ord("0")
        result *= 10
        result += digit
        i += 1

    return parity * result


def wrapper(x, s):
    if int(int_to_string(x)) != x:
        raise TestFailure("Int to string conversion failed")
    if string_to_int(s) != x:
        raise TestFailure("String to int conversion failed")


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "string_integer_interconversion.py",
            "string_integer_interconversion.tsv",
            wrapper,
        )
    )
