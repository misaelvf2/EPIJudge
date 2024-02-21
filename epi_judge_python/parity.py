from test_framework import generic_test


def parity(x: int) -> int:
    i = 0
    answer = 0
    while i < 64:
        answer ^= PARITY_TABLE[(x >> i) & 0xFFFF]
        i += 16
    return answer


def build_parity_table(size: int) -> dict[int, int]:
    table = {}
    for i in range(2**size):
        table[i] = count_set_bits(i) % 2
    return table


def count_set_bits(x: int) -> int:
    count = 0
    while x:
        count += x & 1
        x >>= 1
    return count


PARITY_TABLE = build_parity_table(16)


if __name__ == "__main__":
    exit(generic_test.generic_test_main("parity.py", "parity.tsv", parity))
