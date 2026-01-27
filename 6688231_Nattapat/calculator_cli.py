"""
Simple calculator command-line interface.
"""

from calculator import calculate


def main():
    """Run the calculator in interactive mode."""
    print("Simple Calculator")
    print("=" * 40)
    print("Supported operations:")
    print("  + or 'add'      : Addition")
    print("  - or 'subtract' : Subtraction")
    print("  * or 'multiply' : Multiplication")
    print("  / or 'divide'   : Division")
    print("Type 'quit' to exit")
    print("=" * 40)
    
    while True:
        try:
            user_input = input("\nEnter calculation (e.g., '5 + 3' or 'quit'): ").strip()
            
            if user_input.lower() == 'quit':
                print("Goodbye!")
                break
            
            # Parse input
            parts = user_input.split()
            
            if len(parts) != 3:
                print("Error: Invalid format. Use '<number> <operation> <number>'")
                continue
            
            try:
                a = float(parts[0])
                operation = parts[1]
                b = float(parts[2])
            except ValueError:
                print("Error: Invalid number format")
                continue
            
            # Perform calculation
            result = calculate(operation, a, b)
            print(f"Result: {a} {operation} {b} = {result}")
            
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
