# Simple Calculator

A Python-based calculator supporting basic arithmetic operations.

## Features

- **Addition** - Add two numbers using `+` or `add`
- **Subtraction** - Subtract two numbers using `-` or `subtract`
- **Multiplication** - Multiply two numbers using `*` or `multiply`
- **Division** - Divide two numbers using `/` or `divide` (with zero-division protection)

## Files

- `calculator.py` - Core calculator module with arithmetic functions
- `calculator_cli.py` - Interactive command-line interface
- `test_calculator.py` - Comprehensive unit tests

## Usage

### As a Module

```python
from calculator import add, subtract, multiply, divide, calculate

# Using individual functions
result = add(10, 5)  # Returns 15
result = divide(20, 4)  # Returns 5

# Using the calculate function
result = calculate('+', 10, 5)  # Returns 15
result = calculate('add', 10, 5)  # Also returns 15
```

### Interactive CLI

Run the interactive calculator:

```bash
python calculator_cli.py
```

Example interactions:
```
Enter calculation (e.g., '5 + 3' or 'quit'): 10 + 5
Result: 10.0 + 5 = 15.0

Enter calculation (e.g., '5 + 3' or 'quit'): 20 / 4
Result: 20.0 / 4 = 5.0

Enter calculation (e.g., '5 + 3' or 'quit'): quit
Goodbye!
```

## Testing

Run the test suite:

```bash
pytest test_calculator.py -v
```

All functions include comprehensive test coverage for:
- Positive and negative numbers
- Float arithmetic
- Edge cases (zero, division by zero)
- Error handling
