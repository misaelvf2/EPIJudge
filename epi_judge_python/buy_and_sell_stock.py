from typing import List

from test_framework import generic_test


def buy_and_sell_stock_once(prices: List[float]) -> float:
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
