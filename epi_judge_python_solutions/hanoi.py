import functools
from typing import List

from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook

NUM_PEGS = 3


def compute_tower_hanoi_epi(num_rings: int) -> List[List[int]]:
    # EPI's solution. Essentially the same as my solution, with some slight differences.
    # Also, they explicitly track the pegs and rings for some reason, even though it isn't necessary.
    # Probably just there for illustration/debugging purposes.
    # Time: O(2^n)
    # Space: O(n)
    def compute_tower_hanoi_steps(
        num_rings_to_move: int, from_peg: int, to_peg: int, use_peg: int
    ):
        if num_rings_to_move > 0:
            compute_tower_hanoi_steps(num_rings_to_move - 1, from_peg, use_peg, to_peg)
            pegs[to_peg].append(pegs[from_peg].pop())
            result.append([from_peg, to_peg])
            compute_tower_hanoi_steps(num_rings_to_move - 1, use_peg, to_peg, from_peg)

    result = []
    pegs = [list(reversed(range(1, num_rings + 1)))] + [[] for _ in range(1, NUM_PEGS)]

    compute_tower_hanoi_steps(num_rings, 0, 1, 2)
    return result


def compute_tower_hanoi_iterative(num_rings: int) -> List[List[int]]:
    # How to simulate the call stack for a recursive relation that looks like this?
    # T(n) = T(n - 1) + 1 + T(n - 1)
    # This is effectively an inorder depth-first search binary tree traversal.
    # Time: O(2^n), hard to see from the iterative code, but we're still doing the same
    # amount of work as the recursive approach.
    # Space: O(n), we still have a stack, we're just managing it explicitly.
    solution = []
    stack = []
    current = [num_rings, 0, 1, 2]

    while current[0] >= 1 or stack:
        # Move as far left as possible.
        # Move top n - 1 rings to spare peg.
        while current[0] >= 1:
            stack.append(current)
            n, source, target, spare = current
            next = [n - 1, source, spare, target]
            current = next
        # Reached base case.
        # Move bottom ring to target.
        n, source, target, spare = stack.pop()
        solution.append([source, target])
        # Now move right.
        # Move top n - 1 rings from spare peg to target peg.
        current = [n - 1, spare, target, source]

    return solution


def compute_tower_hanoi(num_rings: int) -> List[List[int]]:
    # Recursive solution to the Tower of Hanoi problem.
    # The tricky part is figuring out the correct recursive "framing" of the problem.
    # IMO, it is not terribly intuitive.
    # It's easy to fall into the trap of thinking that the subproblem is moving
    # the top n - 1 rings to the target peg, but that doesn't get us anywhere
    # because then the bottom ring would be put on top of the smaller rings.
    # The correct framing is this: to move n rings from a source peg to a target peg,
    # first move the top n - 1 rings to the spare peg. Then, move the nth ring
    # (i.e., the largest ring) to the target peg. Then, move the top n - 1 rings
    # from the spare peg to the target peg.
    # Recurrence relation:
    # T(n) = 1, n = 1
    #        T(n) + 1 + T(n), n > 1
    # Time: O(2^n), every function call makes two recursive calls.
    # Space: O(n), the depth of the call stack is linear in the number of rings.
    def tower_hanoi_rec(
        n: int, source: int, target: int, spare: int
    ) -> List[List[int]]:
        # Base case
        if n == 1:
            return [[source, target]]
        # Temporarily move top n - 1 rings to spare peg
        sub_results = tower_hanoi_rec(n - 1, source, spare, target)
        # Move bottom ring to target peg
        sub_results.extend([[source, target]])
        # Move top n - 1 rings from spare peg to target peg
        sub_results.extend(tower_hanoi_rec(n - 1, spare, target, source))
        return sub_results

    return tower_hanoi_rec(num_rings, 0, 1, 2)


@enable_executor_hook
def compute_tower_hanoi_wrapper(executor, num_rings):
    pegs = [list(reversed(range(1, num_rings + 1)))] + [[] for _ in range(1, NUM_PEGS)]

    result = executor.run(functools.partial(compute_tower_hanoi, num_rings))

    for from_peg, to_peg in result:
        if pegs[to_peg] and pegs[from_peg][-1] >= pegs[to_peg][-1]:
            raise TestFailure(
                "Illegal move from {} to {}".format(
                    pegs[from_peg][-1], pegs[to_peg][-1]
                )
            )
        pegs[to_peg].append(pegs[from_peg].pop())
    expected_pegs1 = [[], [], list(reversed(range(1, num_rings + 1)))]
    expected_pegs2 = [[], list(reversed(range(1, num_rings + 1))), []]
    if pegs not in (expected_pegs1, expected_pegs2):
        raise TestFailure("Pegs doesn't place in the right configuration")


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "hanoi.py", "hanoi.tsv", compute_tower_hanoi_wrapper
        )
    )
