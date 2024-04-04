from typing import List

from test_framework import generic_test


import bisect


def has_three_sum(A: List[int], t: int) -> bool:
    # Approach based on invariants.
    # Sort the array so we can use the invariants
    # implementation of 2Sum.
    # Time: O(n^2), we look at every element, and for every element, we spend O(n) work.
    # Space: O(1)
    A.sort()
    for i, num in enumerate(A):
        complement = t - num
        if has_two_sum(A[i:], complement):
            return True
    return False


def has_two_sum(A: list[int], t: int) -> bool:
    A.sort()
    start, end = 0, len(A) - 1
    while start <= end:
        if A[start] + A[end] == t:
            return True
        elif A[start] + A[end] < t:
            start += 1
        else:
            end -= 1
    return False


def has_three_sum_extra_space(A: List[int], t: int) -> bool:
    # Approach based on extra space utilization.
    # First, store each element in a hashset.
    # Then, iterate over the list, subtracting each element
    # from the target.
    # The problem now reduces to finding a pair of numbers that
    # add up to the difference between the target and the number
    # we chose in the outer loop.
    # In other words, 3Sum now reduces to 2Sum.
    # This is the extra space implementation of 2Sum.
    # Time: O(n^2), both the outer and inner loops look at each element once.
    # Space: O(n), we store every element in a set.
    num_set = set(A)
    for i, num1 in enumerate(A):
        first_complement = t - num1
        # Problem now reduces to 2Sum.
        for _, num2 in enumerate(A[i:], start=i):
            second_complement = first_complement - num2
            if second_complement in num_set:
                return True
    return False


def has_three_sum_epi(A: List[int], t: int) -> bool:
    # Same approach as below: reduce the problem to 2Sum,
    # and then use invariants.
    # The only difference is this solution is more Pythonic.
    # Time: O(n^2)
    # Space: O(1)
    A.sort()
    return any([has_two_sum(A, t - a) for a in A])


def has_three_sum_binary_search(A: List[int], t: int) -> bool:
    # Inefficient approach based on invariants and binary search.
    # Better than brute-force, but not optimal.
    # Time: O(n^2 * log n)
    # Space: O(1)
    A.sort()
    for i, num1 in enumerate(A):
        first_complement = t - num1
        for _, num2 in enumerate(A[i:], start=i):
            second_complement = first_complement - num2
            # Use binary search to find the second complement.
            idx = bisect.bisect_left(A, x=second_complement)
            if idx < len(A) and A[idx] == second_complement:
                return True
    return False


if __name__ == "__main__":
    exit(generic_test.generic_test_main("three_sum.py", "three_sum.tsv", has_three_sum))
