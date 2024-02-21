from test_framework import generic_test


CHUNK_SIZE = 16


def parity(x: int) -> int:
    result = 0
    # This neat trick gives me a bit mask consisting of CHUNK_SIZE 1 bits
    bit_mask = (1 << CHUNK_SIZE) - 1
    while x:
        # This uses masking to isolate the last CHUNK_SIZE bits
        result ^= PARITY_TABLE[x & bit_mask]
        # This shifts the next CHUNK_SIZE bits to the end of the word
        x >>= CHUNK_SIZE
    return result


def build_parity_table(size: int) -> dict[int, int]:
    table = {}
    for i in range(1 << size + 1):
        table[i] = count_set_bits(i) % 2
    return table


def count_set_bits(x: int) -> int:
    count = 0
    while x:
        count += 1
        # This bit manipulation trick clears the lowest set bit,
        # so this loop runs in O(k), where k is the number of set bits
        x &= x - 1
    return count


PARITY_TABLE = build_parity_table(CHUNK_SIZE)


if __name__ == "__main__":
    exit(generic_test.generic_test_main("parity.py", "parity.tsv", parity))
