import functools
from typing import List

from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook

RED, WHITE, BLUE = range(3)


def dutch_flag_partition(pivot_index: int, A: List[int]) -> None:
    # Optimized, single-pass solution based on loop invariants.
    # lower, equal, and greater point to where the next element in each respective region would go.
    # Tricky implementation! Need to pay very careful attention to the loop invariant conditions.
    # Time: O(n)
    # Space: O(1)
    pivot = A[pivot_index]
    lower, equal, greater = 0, 0, len(A) - 1

    # Each loop iteration shrinks the unclassified region by one.
    # The unclassified region shrinks from either the left or the right.
    # Notice how the loop terminates when the equal region meets the greater region!
    while equal <= greater:
        # Element should go in lower region, so we swap and grow the lower region.
        if A[equal] < pivot:
            A[lower], A[equal] = A[equal], A[lower]
            lower += 1
            equal += 1
        # Element is in correct region, so no need to swap; just grow the equal region.
        # This works because the equal region is immediately to the right of the lower region.
        elif A[equal] == pivot:
            equal += 1
        # Element should go in greater region, so we swap and grow the greater region.
        else:
            A[greater], A[equal] = A[equal], A[greater]
            # Notice how we don't increment the equal pointer.
            # This is because the lower region hasn't grown, which would cause the equal region to "shift" to the right.
            greater -= 1


def dutch_flag_partition_optimized(pivot_index: int, A: List[int]) -> None:
    # Optimized, two-pass solution.
    # Avoids repeated work by keeping track of smaller/greater regions.
    # Time: O(n)
    # Space: O(1)
    pivot = A[pivot_index]
    smaller = 0
    # First pass groups all smaller elements to the left.
    for i, num in enumerate(A):
        if num < pivot:
            A[i], A[smaller] = A[smaller], A[i]
            smaller += 1
    greater = len(A) - 1
    # Second pass groups all greater elements to the right.
    for i, num in enumerate(reversed(A)):
        if num > pivot:
            A[-(i + 1)], A[greater] = A[greater], A[-(i + 1)]
            greater -= 1


def dutch_flag_partition_unoptimized_space(pivot_index: int, A: List[int]) -> None:
    # Create and populate three new arrays for elements lower, equal, and greater than the pivot.
    # Easiest solution, but unoptimized for space.
    # Time: O(n)
    # Space: O(n)
    pivot = A[pivot_index]
    lower, equal, greater = [], [], []
    for num in A:
        if num < pivot:
            lower.append(num)
        elif num == pivot:
            equal.append(num)
        else:
            greater.append(num)

    for i, num in enumerate(lower + equal + greater):
        A[i] = num


def dutch_flag_partition_unoptimized(pivot_index: int, A: List[int]) -> None:
    # Unoptimized solution. Perform two passes over array.
    # First pass groups the lower elements on the left.
    # Second pass groups greater elements on the right.
    # Time: O(n^2)
    # Space: O(1)
    pivot = A[pivot_index]
    i = 0
    while i < len(A):
        j = i + 1
        while j < len(A):
            if A[j] < pivot:
                A[i], A[j] = A[j], A[i]
                break
            j += 1
        i += 1
    i = len(A) - 1
    while i >= 0:
        j = i - 1
        while j >= 0:
            if A[j] > pivot:
                A[i], A[j] = A[j], A[i]
                break
            j -= 1
        i -= 1


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
