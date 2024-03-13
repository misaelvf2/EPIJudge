from typing import List

from test_framework import generic_test

import heapq


def merge_sorted_arrays(sorted_arrays: List[List[int]]) -> List[int]:
    result = []
    heap = []
    iterators = [iter(x) for x in sorted_arrays]

    # Initialize the heap with the first element in each array
    for i, it in enumerate(iterators):
        heapq.heappush(heap, (next(it), i))

    # Merge the arrays
    while heap:
        # Get the next smallest element
        min_elem, min_idx = heapq.heappop(heap)
        result.append(min_elem)
        # Advance the iterator on the list whose element we just consumed,
        # and add the next element to the heap
        next_iter = iterators[min_idx]
        next_elem = next(next_iter, None)
        if next_elem is not None:
            heapq.heappush(heap, (next_elem, min_idx))

    return result


def merge_sorted_arrays_combine(sorted_arrays: List[List[int]]) -> List[int]:
    # Similar to the below approach.
    # Create one big array, then heapify it.
    # Finally, use heap sort to return the merged result.
    # Time: O(n log n)
    # Space: O(n)
    heap = []
    for arr in sorted_arrays:
        heap += arr
    heapq.heapify(heap)
    return [heapq.heappop(heap) for _ in range(len(heap))]


def merge_sorted_arrays_inefficient(sorted_arrays: List[List[int]]) -> List[int]:
    # Create a heap. Iterate through each array in turn,
    # pushing elements onto the heap as we see them.
    # Use heap sort to return the merged result.
    # This doesn't exploit the fact that the arrays are sorted.
    # Time: O(n log n)
    # Space: O(n)
    heap = []
    for arr in sorted_arrays:
        for elem in arr:
            heapq.heappush(heap, elem)

    return [heapq.heappop(heap) for _ in range(len(heap))]


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "sorted_arrays_merge.py", "sorted_arrays_merge.tsv", merge_sorted_arrays
        )
    )
