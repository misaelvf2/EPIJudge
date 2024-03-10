from test_framework import generic_test
from test_framework.test_failure import TestFailure


class Stack:
    # Straightforward implementation.
    # Use Python list internally to store elements.
    # Keep track of current max value with a variable, initialized to -inf.
    # Two cases to watch out for:
    # When pushing a new element, check to see if it is greater than the current max.
    # When popping, check to see if popped element was current max. If so,
    # recompute the new max in O(n) time, taking care to reset the max
    # to -inf if the list is empty.
    # Time: O(n) for popping, O(1) for all other operations.
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
