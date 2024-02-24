import functools
from typing import List

from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook

RED, WHITE, BLUE = range(3)


def dutch_flag_partition(pivot_index: int, A: List[int]) -> None:
    # Two-pass solution based on loop invariants.
    # Partition the array into three regions:
    # lower - for elements less than the pivot
    # greater - for elements greater than the pivot
    # unclassified - for elements yet to be classified in one region or the other.
    # The first pass populates the lower and greater regions;
    # the second pass populates a new equal region
    # in between the lower and greater regions.
    # You have to pay special attention to how the loop invariant
    # is initialized and maintained.
    # Time: O(n)
    # Space: O(1)
    pivot = A[pivot_index]
    lower, greater = -1, len(A)

    i = 0
    while i < greater:
        if A[i] < pivot:
            lower += 1
            A[lower], A[i] = A[i], A[lower]
            i += 1
        elif A[i] > pivot:
            # Notice how i isn't incremented in this case.
            # Doing so would erroneously take the swapped element
            # at A[greater] outside the unclassified region.
            greater -= 1
            A[greater], A[i] = A[i], A[greater]
        else:
            i += 1
    # At this point, we know the equal region is bounded
    # by lower < i < greater
    i = lower + 1
    while i < greater:
        A[i] = pivot
        i += 1


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
