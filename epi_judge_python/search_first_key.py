from typing import List

from test_framework import generic_test


import bisect


def search_first_of_k(A: List[int], k: int) -> int:
    # Iterative version of the same binary search algorithm
    # from below. Same considerations apply.
    # Some implementation hints: binary search is *really*
    # easy to get subtly wrong. I've found that using inclusive
    # start and end pointers leads to an easier to understand implementation,
    # at the cost of inconsistency with Python's slice indexing conventions.
    # Also, using the average of start and end is better than halving the difference,
    # because it's easy to forget to add it to the start index later on.
    # Time: O(log n)
    # Space: O(1)
    start, end = 0, len(A) - 1
    while start < end:
        mid = start + (end - start) // 2
        if A[mid] >= k:
            end = mid
        else:
            start = mid + 1
    if start < len(A) and A[start] == k:
        return start
    return -1


def search_first_of_k_epi(A: List[int], k: int) -> int:
    # Very similar to my solution, with the some slight differences.
    # This version tests for one of three conditions:
    # greater than key, equal to key, and less than key.
    # The binary search also terminates when the candidate space is empty,
    # in contrast to my solution which terminates when the candidate space
    # is a single element.
    # To accomodate for this, this initializes a result variable to -1,
    # and updates it whenever the key is found in the list.
    # The candidate space is updated carefully such that earlier occurrences
    # of the key are not excluded, similarly to my solution.
    # Time: O(log n)
    # Space: O(1)
    start, end = 0, len(A) - 1
    result = -1

    # Perform binary search until candidate set is empty.
    while start <= end:
        mid = start + (end - start) // 2
        if A[mid] < k:
            start = mid + 1
        elif A[mid] == k:
            result = mid
            end = mid - 1
        else:
            end = mid - 1

    return result


def search_first_of_k_pythonic(A: List[int], k: int) -> int:
    # Perform binary search using Python's built-in bisect module.
    # Note that we use bisect_left, which effectively returns
    # the index of the leftmost occurrence of the key,
    # if it is already present in the list.
    # Equivalently, it returns the index where the key
    # should be inserted such that it will be to the
    # left of any existing instances of the key.
    index = bisect.bisect_left(A, k)

    if index < len(A) and A[index] == k:
        return index
    return -1


def search_first_of_k_rec(A: List[int], k: int) -> int:
    # Perform usual binary search, but don't terminate
    # on finding the key. Instead, continue binary search
    # until list is down to a single element.
    # Recursive implementation.
    # Time: O(log n)
    # Space: O(log n)
    def bin_search(start, end):
        if start < end:
            mid = (start + end) // 2
            if A[mid] >= k:
                return bin_search(start, mid)
            else:
                return bin_search(mid + 1, end)
        # The empty input edge case is very easy to miss.
        if start < len(A) and A[start] == k:
            return start
        return -1

    return bin_search(0, len(A) - 1)


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "search_first_key.py", "search_first_key.tsv", search_first_of_k
        )
    )
