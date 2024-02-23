import functools
from typing import List

from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook

RED, WHITE, BLUE = range(3)


def dutch_flag_partition(pivot_index: int, A: List[int]) -> None:
    # Time: O(n)
    # Space: O(n)
    # Determine partition sizes to determine where elements
    # will end up at in the final array
    # Use temporary array to simplify insertion logic
    # at cost of extra space utilization
    lower_count, equal_count, _ = partition_sizes(pivot_index, A)
    lower = 0
    equal = lower_count
    greater = lower_count + equal_count

    result = [0] * len(A)
    for num in A:
        if num < A[pivot_index]:
            result[lower] = num
            lower += 1
        elif num == A[pivot_index]:
            result[equal] = num
            equal += 1
        else:
            result[greater] = num
            greater += 1

    for i, num in enumerate(result):
        A[i] = num


def partition_sizes(pivot_index: int, A: List[int]) -> tuple[int, int, int]:
    lower = equal = greater = 0
    for num in A:
        if num < A[pivot_index]:
            lower += 1
        elif num == A[pivot_index]:
            equal += 1
        else:
            greater += 1
    return (lower, equal, greater)


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
