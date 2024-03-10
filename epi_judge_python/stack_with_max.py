from test_framework import generic_test
from test_framework.test_failure import TestFailure
import heapq
from collections import namedtuple

StackNode = namedtuple("StackNode", ["element", "max"])


class Stack:
    # O(1) amortized time for all operations.
    # Any time we push a new item onto the stack, we also store the maximum value
    # in the "sub-stack" that includes it. This works because the stack is only
    # mutated at the top and never at the bottom.
    # Time: O(1) amortized time for all operations.
    # Space: O(n)
    def __init__(self):
        self._stack = []

    def empty(self) -> int:
        return len(self._stack) == 0

    def max(self) -> int:
        return self._stack[-1].max

    def pop(self) -> int:
        if self.empty():
            raise IndexError
        return self._stack.pop().element

    def push(self, x: int) -> None:
        self._stack.append(
            StackNode(element=x, max=x if self.empty() else max(x, self.max()))
        )


class Stack_heap_failed:
    # This is an attempt at using a heap to reduce the runtime.
    # Unfortunately, this attempt fails to do so because the
    # heapify operation runs in O(n) space. There's probably a way to
    # do better.
    def __init__(self):
        self._stack = []
        self._heap = []
        self._size = 0

    def empty(self) -> bool:
        return self._size == 0

    def max(self) -> int:
        if self._size == 0:
            raise IndexError
        return -self._heap[0]

    def pop(self) -> int:
        if self._size == 0:
            raise IndexError
        elem = self._stack.pop()
        self._size -= 1
        prev_max = self._heap[0]
        if elem == prev_max:
            self._heap = self._stack[:]
            heapq.heapify(self._heap)
        return -elem

    def push(self, x: int) -> None:
        self._stack.append(-x)
        heapq.heappush(self._heap, -x)
        self._size += 1


class Stack_list:
    # Straightforward implementation.
    # Use Python list internally to store elements.
    # Keep track of current max value with a variable, initialized to -inf.
    # Two cases to watch out for:
    # When pushing a new element, check to see if it is greater than the current max.
    # When popping, check to see if popped element was current max. If so,
    # recompute the new max in O(n) time, taking care to reset the max
    # to -inf if the list is empty.
    # Note that we might be able to do O(log n) to recompute the max if we used a heap internally instead.
    # Time: O(n) for popping, O(1) for all other operations.
    # NOTE: Might actually be O(1) amortized time for popping, given that we only recompute if the popped item was the previous max.
    # Space: O(n) for internal list.
    def __init__(self):
        self._stack = []
        self._size = 0
        self._max = float("-inf")

    def empty(self) -> bool:
        return self._size == 0

    def max(self) -> int:
        if self._size == 0:
            raise IndexError
        return self._max

    def pop(self) -> int:
        if self._size == 0:
            raise IndexError
        elem = self._stack.pop()
        self._size -= 1
        if elem == self._max:
            if self._size > 0:
                self._max = max(self._stack)
            else:
                self._max = float("-inf")
        return elem

    def push(self, x: int) -> None:
        self._stack.append(x)
        self._size += 1
        self._max = max(self._max, x)

    def _recompute_max(self) -> int:
        return max(self._stack)


def stack_tester(ops):
    try:
        s = Stack()

        for op, arg in ops:
            if op == "Stack":
                s = Stack()
            elif op == "push":
                s.push(arg)
            elif op == "pop":
                result = s.pop()
                if result != arg:
                    raise TestFailure(
                        "Pop: expected " + str(arg) + ", got " + str(result)
                    )
            elif op == "max":
                result = s.max()
                if result != arg:
                    raise TestFailure(
                        "Max: expected " + str(arg) + ", got " + str(result)
                    )
            elif op == "empty":
                result = int(s.empty())
                if result != arg:
                    raise TestFailure(
                        "Empty: expected " + str(arg) + ", got " + str(result)
                    )
            else:
                raise RuntimeError("Unsupported stack operation: " + op)
    except IndexError:
        raise TestFailure("Unexpected IndexError exception")


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "stack_with_max.py", "stack_with_max.tsv", stack_tester
        )
    )
