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

def main():
    while True:
        print("\nSimple Calculator")
        print("Operations: +, -, *, /")
        op = input("Enter operation (or 'q' to quit): ").strip()

        if op.lower() == 'q':
            break

        if op not in ['+', '-', '*', '/']:
            print("Invalid operation. Please use +, -, *, or /")
            continue

        try:
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
        except ValueError:
            print("Invalid number. Please enter numeric values.")
            continue

        try:
            if op == '+':
                result = add(a, b)
            elif op == '-':
                result = subtract(a, b)
            elif op == '*':
                result = multiply(a, b)
            elif op == '/':
                result = divide(a, b)

            print(f"Result: {result}")
        except ValueError as e:
            print(e)

if __name__ == "__main__":
    main()