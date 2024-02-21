from test_framework import generic_test


CHUNK_SIZE = 16


def parity(x: int) -> int:
    # This approach combines the word-level XOR instructions and caching
    x ^= x >> 32
    return PARITY_TABLE[(x >> 16) & 0xFFFF] ^ PARITY_TABLE[x & 0xFFFF]


def parity_word_level(x: int) -> int:
    # Time: O(log n)
    # Space: O(1)
    # This exploits the fact that XOR is associative and commutative
    # to use CPU word-level XOR instructions
    # The running XOR is stored in the latter half of the word,
    # and we continue until it reaches a single bit,
    # at which point, we extract it from the word
    x ^= x >> 32
    x ^= x >> 16
    x ^= x >> 8
    x ^= x >> 4
    x ^= x >> 2
    x ^= x >> 1
    return x & 1


def parity_cache(x: int) -> int:
    # Time: O(n/L), where L is the CHUNK_SIZE
    # Space: O(1), ignoring space used for table
    # This approach is based on the observation that XOR is associative,
    # so we can split the input into n/L CHUNK_SIZE sub-words
    # If we pre-compute a table for every CHUNK_SIZE sub-word,
    # then this algorithm reduces to keying into the table
    # and combining the sub-results
    # This is workable for 16-bit subwords, since the table
    # only takes up 64KiB
    result = 0
    bit_mask = (1 << CHUNK_SIZE) - 1
    while x:
        result ^= PARITY_TABLE[x & bit_mask]
        x >>= CHUNK_SIZE
    return result


def parity_unoptimized(x: int) -> int:
    # Time: O(n)
    # Space: O(1)
    # Unoptimized algorithm. Look at each bit, counting the 1s as you go
    result = 0
    while x:
        result ^= x & 1
        x >>= 1
    return result


def parity_clear_lowest(x: int) -> int:
    # Time: O(k)
    # Space: O(1)
    # Use bit-flidding trick to only look at the set bits
    result = 0
    while x:
        result ^= 1
        x &= x - 1
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
        # This bit-fiddling trick clears the lowest set bit,
        # so this loop runs in O(k), where k is the number of set bits
        x &= x - 1
    return count


PARITY_TABLE = build_parity_table(CHUNK_SIZE)


if __name__ == "__main__":
    exit(generic_test.generic_test_main("parity.py", "parity.tsv", parity))
