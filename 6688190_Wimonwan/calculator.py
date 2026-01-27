def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
# Update implementation for clarity
def calculate_velocity(distance, time):
    if time <= 0:
        raise ValueError("Time must be greater than zero")
    return distance / time