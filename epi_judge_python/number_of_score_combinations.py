from typing import List

from test_framework import generic_test


import functools


def num_combinations_for_final_score_epi(
    final_score: int, individual_play_scores: List[int]
) -> int:
    # Basically the same as my solution, just written a bit differently.
    # They initialize the table with 1s in the 0 column directly, rather than
    # in two steps like I do.
    # Time: O(s * k), where s is the final score, and k is the length of individual_play_scores.
    # Space: O(s * k)

    # One way to reach 0.
    num_combinations_for_score = [
        [1] + [0] * final_score for _ in individual_play_scores
    ]

    for i in range(len(individual_play_scores)):
        for j in range(1, final_score + 1):
            without_this_play = num_combinations_for_score[i - 1][j] if i >= 1 else 0
            with_this_play = (
                num_combinations_for_score[i][j - individual_play_scores[i]]
                if j >= individual_play_scores[i]
                else 0
            )
            num_combinations_for_score[i][j] = without_this_play + with_this_play

    return num_combinations_for_score[-1][-1]


def num_combinations_for_final_score(
    final_score: int, individual_play_scores: List[int]
) -> int:
    # Bottom-up dynamic programming approach.
    # We fill in a 2D table, where the rows represent
    # the end index int othe individual_play_scores list, and
    # the columns represent scores from i = 0, 1, ..., final_score.
    # We first initialize the 0 column with the value 1, representing
    # the fact that there is only one way values from individual_play_scores
    # can be combined to sum to 0--namely, by selecting no values.
    # The table is then filled in by direct reference to the recurrence relation:
    # T(n, i) = 1, if n == 0
    #         = T(n - S[i], i) + T(n, i - 1), if n > 0
    # The tricky part is keeping the row and columns straight (i.e., in this implementation,
    # the rows and columns are inverted relative to the order suggested by the recurrence relation).
    # Also, in contrast to the bottom-up approach, we think of the index as being the "end index"
    # rather than the "start index", that way the values are in ascending order.
    # Time: O(s * k), where s is the final score, and k is the length of individual_play_scores.
    # Space: O(s * k)
    table = [[0] * (final_score + 1) for _ in range(len(individual_play_scores))]

    # Initialize 0 column.
    for i in range(len(individual_play_scores)):
        table[i][0] = 1

    # Fill in the table.
    for i, play_score in enumerate(individual_play_scores):
        for j in range(1, final_score + 1):
            combinations = 0
            # Include play_score in combination.
            if j - play_score >= 0:
                combinations += table[i][j - play_score]
            # Don't include play_score combination.
            if i - 1 >= 0:
                combinations += table[i - 1][j]
            table[i][j] = combinations

    return table[len(individual_play_scores) - 1][final_score]


def _num_combinations_for_final_score(
    final_score: int, individual_play_scores: List[int]
) -> int:
    # Top-down dynamic programming approach.
    # Similar to the (bad) approach below, but with a much simpler framing:
    # at each step, we make a decision of whether to include or not include the current value
    # in the combination. This leads to a *much* simpler implementation, and the recursive tree
    # is a binary tree, in contrast to the bad approach, where the nodes have up to S children.
    # We still encode the state with (current_score, start) pairs to ensure unique combinations.
    # The new recurrence relation looks like this:
    # T(n, i) = 1, if n == 0
    #         = T(n - S[i], i) + T(n, i + 1), if n > 0
    @functools.lru_cache(None)
    def helper(current_score: int, start: int) -> int:
        # Base case
        if current_score == 0:
            return 1
        # Recursive case
        combinations = 0
        # Include play_score in combination.
        if current_score - individual_play_scores[start] >= 0:
            combinations += helper(current_score - individual_play_scores[start], start)
        # Don't include play_score in combination.
        if start + 1 < len(individual_play_scores):
            combinations += helper(current_score, start + 1)
        return combinations

    return helper(final_score, 0)


def num_combinations_for_final_score_bad(
    # UNNECESSARILY CONVOLUTED Top-down dynamic programming approach.
    # Leaving this here for future reference and reminder to myself to not keep falling into this dumb trap.
    # We break down the problem as follows: to find the number of unique combinations
    # of values in individual_play_scores that sum up to final_score, make a selection s
    # among the values in individual_play_values, subtract it from final_score, and find
    # the number of unique combinations of values in individual_play_scores that sum up to
    # final_score - s. Base case is final_score = 0, where the number of unique combinations
    # is 1 (there is only one way to sum up to 0: don't select any of the values).
    # The recurrence relation looks something like this:
    # T(n) = 1, if n == 0
    #      = Sum of T(n - s) for all s in S, if n > 0
    # The tricky part of this problem is ensuring we only count unique solutions.
    # One way to achieve this is to store the solutions as sequences of values from
    # S. To ensure uniqueness, we encode the sequences as sorted
    # tuples, and store them in a set.
    # A more elegant approach is to prune the search tree to avoid going down repeated sequences
    # in the first place. To achieve that, we make the following observation:
    # the left branch of the recursion tree will have all possible combations
    # of values with at least one s0 value from S. Therefore, any branch to the right
    # need not include in its sequence, as it will already have been covered by the branch to the left.
    # We can generalize this idea into the following rule: for every iteration of possible choices,
    # prune the possible choices to only include the current choice and choices to the right of it.
    # For instance, if S = {2, 3, 4}, when s = 3, the recursive call should look something like
    # rec(score - 4, S={3, 4}).
    # Instead of explicitly passing the set of values down the call stack, we pass the index
    # for the current choice.
    final_score: int,
    individual_play_scores: List[int],
) -> int:
    @functools.lru_cache(None)
    def combinations_rec(score: int, start: int):
        # Base case
        if score == 0:
            return 1
        # Recursive case
        total = 0
        for i, play_score in enumerate(individual_play_scores[start:], start=start):
            if score - play_score >= 0:
                total += combinations_rec(score - play_score, i)
        return total

    return combinations_rec(final_score, 0)


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "number_of_score_combinations.py",
            "number_of_score_combinations.tsv",
            num_combinations_for_final_score,
        )
    )
