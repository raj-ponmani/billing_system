from typing import Dict

# default denominations available in shop;
DEFAULT_DENOMINATIONS = [2000, 500, 200, 100, 50, 20, 10, 5, 2, 1]


def calculate_change_distribution(balance: float, denominations=None) -> Dict[int, int]:
    """
    Returns a dict {denomination: count} for integer part of balance.
    """
    if denominations is None:
        denominations = DEFAULT_DENOMINATIONS
    result = {}
    remaining = int(round(balance))
    for d in denominations:
        if remaining <= 0:
            break
        count, remaining = divmod(remaining, d)
        if count:
            result[d] = count
    return result
