from typing import List

from test_framework import generic_test


import bisect


def intersect_two_sorted_arrays(A: List[int], B: List[int]) -> List[int]:
    # Simultaneously iterate through A and B,
    # adding equal elements to the result as we go.
    # Update the pointers depending on the result of the
    # comparison between A[i] and B[j], accounting for the
    # sorted property of the two arrays.
    # Take special care to skip over the duplicates.
    # Works best when arrays are of similar size.
    # Time: O(m + n) -- maybe O(min(m, n))???
    # Space: O(1)
    result = []

    i, j = 0, 0
    while i < len(A) and j < len(B):
        if A[i] < B[j]:
            i += 1
        elif A[i] == B[j]:
            result.append(A[i])
            i += 1
            j += 1
            # Skip over duplicates
            while i < len(A) and A[i] == A[i - 1]:
                i += 1
            while j < len(B) and B[j] == B[j - 1]:
                j += 1
        else:
            j += 1

    return result


def intersect_two_sorted_arrays_binary_search_epi(
    A: List[int], B: List[int]
) -> List[int]:
    # Iterate through the smaller of the two arrays.
    # (We don't actually compare the array sizes here,
    # but assume that the caller is passing in the smaller one first.)
    # For each element, perform a binary search to try to find it
    # in the other array.
    # Take care to skip over duplicates.
    # Works best when one array is much smaller than the other.
    # Notice the fancy list comprehension.
    def is_present(x):
        i = bisect.bisect_left(B, x)
        return i < len(B) and B[i] == x

    return [
        x for (i, x) in enumerate(A) if (i == 0 or A[i] != A[i - 1]) and is_present(x)
    ]


def intersect_two_sorted_arrays_epi(A: List[int], B: List[int]) -> List[int]:
    # Very similar to my solution, the only big difference being
    # how they handle duplicates.
    i, j, intersection = 0, 0, []
    while i < len(A) and j < len(B):
        if A[i] == B[j]:
            if i == 0 or A[i] != A[i - 1]:
                intersection.append(A[i])
            i, j = i + 1, j + 1
        elif A[i] < B[j]:
            i += 1
        else:  # A[i] > B[j]
            j += 1
    return intersection


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "intersect_sorted_arrays.py",
            "intersect_sorted_arrays.tsv",
            intersect_two_sorted_arrays,
        )
    )
