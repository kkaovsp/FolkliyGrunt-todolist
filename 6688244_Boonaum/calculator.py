"""Simple Python calculator with basic arithmetic operations."""


def add(a, b):
    """Add two numbers and return the result."""
    return a + b


def subtract(a, b):
    """Subtract two numbers and return the result."""
    return a - b


def multiply(a, b):
    """Multiply two numbers and return the result."""
    return a * b


def divide(a, b):
    """Divide two numbers and return the result.
    
    Raises:
        ValueError: If attempting to divide by zero.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def velocity(distance, time):
    if time == 0:
        raise ValueError("Time cannot be zero")
    return distance / time


if __name__ == "__main__":
    # Example usage
    print(f"5 + 3 = {add(5, 3)}")
    print(f"10 - 4 = {subtract(10, 4)}")
    print(f"6 * 7 = {multiply(6, 7)}")
    print(f"20 / 4 = {divide(20, 4)}")
