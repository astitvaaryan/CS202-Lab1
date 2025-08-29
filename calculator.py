# calculator.py
"""
A simple command-line calculator to perform basic arithmetic operations.
"""

def add(x, y):
    """Return the sum of two numbers."""
    return x + y

def subtract(x, y):
    """Return the difference of two numbers."""
    return x - y

def multiply(x, y):
    """Return the product of two numbers."""
    return x * y

def divide(x, y):
    """
    Return the quotient of two numbers.
    Handles division by zero.
    """
    if y == 0:
        return "Error! Division by zero."
    return x / y

def main():
    """Main function to run the calculator."""
    print("Simple Calculator")
    num1 = int(input("Enter first number: "))
    num2 = int(input("Enter second number: "))

    print(f"Sum: {add(num1, num2)}")
    print(f"Difference: {subtract(num1, num2)}")
    print(f"Product: {multiply(num1, num2)}")
    print(f"Quotient: {divide(num1, num2)}")

if __name__ == "__main__":
    main()
