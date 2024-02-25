import functools
from typing import List

from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook

RED, WHITE, BLUE = range(3)


def dutch_flag_partition(pivot_index: int, A: List[int]) -> None:
    # One-pass solution based on loop invariants.
    # Partition the array into four regions:
    # lower - for elements less than the pivot
    # equal - for elements equal to the pivot
    # greater - for elements greater than the pivot
    # unclassified - for elements yet to be classified
    # You have to pay *VERY* close attention to how the loop invariant
    # is initialized and maintained.
    # Time: O(n)
    # Space: O(1)
    pivot = A[pivot_index]
    # Notice how we don't have an explicit pointer for the equal region.
    # That's because the iterator implicitly tracks the equal region.
    lower, greater = -1, len(A)

    i = 0
    while i < greater:
        if A[i] < pivot:
            lower += 1
            A[i], A[lower] = A[lower], A[i]
            # Key insight: as the lower region grows,
            # the equal region must also shift to the right.
            i += 1
        elif A[i] == pivot:
            i += 1
        else:
            # *DON'T* increment i!
            # Doing so would erroneously grow the equal region.
            greater -= 1
            A[i], A[greater] = A[greater], A[i]


@enable_executor_hook
def dutch_flag_partition_wrapper(executor, A, pivot_idx):
    count = [0, 0, 0]
    for x in A:
        count[x] += 1
    pivot = A[pivot_idx]

    executor.run(functools.partial(dutch_flag_partition, pivot_idx, A))

    i = 0
    while i < len(A) and A[i] < pivot:
        count[A[i]] -= 1
        i += 1
    while i < len(A) and A[i] == pivot:
        count[A[i]] -= 1
        i += 1
    while i < len(A) and A[i] > pivot:
        count[A[i]] -= 1
        i += 1

    if i != len(A):
        raise TestFailure("Not partitioned after {}th element".format(i))
    elif any(count):
        raise TestFailure("Some elements are missing from original array")


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "dutch_national_flag.py",
            "dutch_national_flag.tsv",
            dutch_flag_partition_wrapper,
        )
    )
