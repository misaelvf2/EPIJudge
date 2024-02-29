from typing import List

from collections import namedtuple

from test_framework import generic_test


Result = namedtuple("Result", ["max_profit", "min_price", "max_price"])


def buy_and_sell_stock_once(prices: List[int]) -> float:
    # Most time- and space-efficient solution.
    # Key insight is to avoid having to "look ahead"
    # to find the maximum possible sales price for each
    # possible purchase price, and to instead
    # keep track of the minimum possible purchase price
    # as we iterate through the array, only checking potential
    # profit as the difference between each sales price
    # and the minimum sales price seen thus far. Very subtle!
    # Time: O(n)
    # Space: O(1)
    result = 0.0
    min_buy_price = prices[0]

    for num in prices:
        min_buy_price = min(min_buy_price, num)
        result = max(result, num - min_buy_price)

    return result


def buy_and_sell_stock_once_divide_and_conquer(prices: List[int]) -> float:
    # Divide and conquer approach.
    # In the divide step, split the array in half until you get to a base case
    # of either 2 elements or 1 element. Solve the base cases.
    # Then, combine results. The combine step is a little tricky.
    # To combine two sub-results, you have a choice between three things:
    # a. the maximum profit in the "left" sub-result
    # b. the maximum profit in the "right" sub-result
    # c. the maximum profit possible by buying at the minimum price
    # in the left subarray and selling at the maximum price
    # in the right subarray.
    # The other tricky part is knowing what to return from each recursive call.
    # Time: O(n * log n)
    # Space: O(log n)
    def solve(prices, i, j):
        # Base case
        if j - i <= 1:
            max_profit = max(0, prices[j] - prices[i])
            min_price = min(prices[i : j + 1])
            max_price = max(prices[i : j + 1])
            return Result(max_profit, min_price, max_price)
        # Recursive case
        mid = (i + j) // 2
        left = solve(prices, i, mid)
        right = solve(prices, mid + 1, j)
        # Combine results
        max_profit = max(
            left.max_profit, right.max_profit, right.max_price - left.min_price
        )
        min_price = min(left.min_price, right.min_price)
        max_price = max(left.max_price, right.max_price)
        # IMPORTANT: we return the min_price because any potential profit
        # at any subsequent sell price can be made with respect to the minimum price,
        # which is always to the left of the sell price.
        # Returning the max_price at the combine step is not strictly necessary
        # (and in fact, we must take care not to sell at a max_price that comes before the buy price),
        # but we return it for sake of consistency with the return values at the base cases.
        return Result(max_profit, min_price, max_price)

    return solve(prices, 0, len(prices) - 1)[0]


def buy_and_sell_stock_once_space_tradeoff(prices: List[int]) -> float:
    # Efficient solution based on space-time tradeoff.
    # Compute a "suffix max" array which, for each index i = 0, 1, ..., len(A) - 1,
    # stores the maximum price in the subarray which starts at and includes i.
    # This is based on the observation that, for any purchase price,
    # we should only compute the profit for the maximum possible selling price.
    result = 0.0

    maxs = [0] * len(prices)
    max_price = prices[-1]
    # Note how we create the array from right-to-left.
    # Otherwise, we'd have to perform a linear search to find the max for each index,
    # which would give us O(n^2) time...
    for i in reversed(range(len(prices))):
        max_price = max(max_price, prices[i])
        maxs[i] = max_price

    # For each purchase price, only sell at the maximum sales price
    # that comes strictly after the purchase day.
    for i in range(len(prices) - 1):
        # Using the same index for both arrays works because if the maximum
        # sales price happens to be on the same day as the purchase price,
        # then the maximum possible profit is 0.0.
        # On the other hand, if the maximum sales price happens *after*,
        # then suffix max at i will still have that maximum price.
        # This is because the suffix max is computed for the subarray that starts at
        # and includes i.
        result = max(result, maxs[i] - prices[i])

    return result


def buy_and_sell_stock_once_complete_search(prices: List[float]) -> float:
    # Brute-force / Complete search approach.
    # Check potential profit for all (buy, sell) price pairs,
    # where the sell price must after the buy price.
    # Time: O(n^2)
    # Space: O(1)
    result = 0.0

    for i in range(len(prices)):
        for j in range(i + 1, len(prices)):
            result = max(result, prices[j] - prices[i])

    return result


def buy_and_sell_stock_once_only_sell_at_max(prices: List[int]) -> float:
    # For each buying price, only sell at the maximum possible price.
    # In other words, for each index i, find the maximum price in the subarray starting at index i + 1.
    # Unfortunately, finding the max requires linear time, and we do this for every element. Thus, it is
    # as inefficient as the complete search approach.
    # Time: O(n^2)
    # Space: O(1)
    result = 0.0

    for i in range(len(prices) - 1):
        result = max(result, max(prices[i + 1 :]) - prices[i])

    return result


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "buy_and_sell_stock.py", "buy_and_sell_stock.tsv", buy_and_sell_stock_once
        )
    )
