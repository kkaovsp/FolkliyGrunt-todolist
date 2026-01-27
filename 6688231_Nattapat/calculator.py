
"""
Simple calculator module supporting basic arithmetic operations.
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
        a: First number (minuend)
        b: Second number (subtrahend)
        
    Returns:
        Difference of a and b
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
        a: Dividend
        b: Divisor
        
    Returns:
        Quotient of a divided by b
        
    Raises:
        ValueError: If divisor is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def calculate(operation: str, a: float, b: float) -> float:
    """
    Perform a calculation based on the operation string.
    
    Args:
        operation: One of '+', '-', '*', '/', 'add', 'subtract', 'multiply', 'divide'
        a: First number
        b: Second number
        
    Returns:
        Result of the calculation
        
    Raises:
        ValueError: If operation is invalid or division by zero
    """
    operations = {
        '+': add,
        '-': subtract,
        '*': multiply,
        '/': divide,
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide,
    }
    
    if operation not in operations:
        raise ValueError(f"Invalid operation: {operation}. Use '+', '-', '*', '/', or their full names.")
    
    return operations[operation](a, b)


def calculate_velocity(distance: float, time: float) -> float:
    """
    Calculate velocity given distance and time.
    
    Args:
        distance: Distance traveled
        time: Time elapsed
        
    Returns:
        Velocity (distance / time)
        
    Raises:
        ValueError: If time is not greater than zero
    """
    if time <= 0:
        raise ValueError("Time must be greater than zero")
    return distance / time

