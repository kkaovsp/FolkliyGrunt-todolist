"""
Calculator module providing basic arithmetic operations.

This module serves as a configuration item for arithmetic calculations,
supporting add, subtract, multiply, and divide operations.
"""


def add(a: float, b: float) -> float:
    """
    Add two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b
    """
    return a + b


def subtract(a: float, b: float) -> float:
    """
    Subtract two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Difference of a and b (a - b)
    """
    return a - b


def multiply(a: float, b: float) -> float:
    """
    Multiply two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Product of a and b
    """
    return a * b


def divide(a: float, b: float) -> float:
    """
    Divide two numbers.

    Args:
        a: Dividend (numerator)
        b: Divisor (denominator)

    Returns:
        Quotient of a and b (a / b)

    Raises:
        ValueError: If b is zero (division by zero)
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
