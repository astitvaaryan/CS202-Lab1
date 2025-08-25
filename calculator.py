# calculator.py

def add(x,y):
    """A function to add two numbers"""
    return x+y

def subtract(x, y):
    """A function to subtract two numbers"""
    return x - y

def multiply(x, y):
    """A function to multiply two numbers"""
    return x * y

def divide(x, y):
    """A function to divide two numbers"""
    if y == 0:
        return "Error! Division by zero."
    return x / y

def main():
    print("Simple Calculator")
    a = int(input("Enter first number: "))
    b = int(input("Enter second number: "))

    print("Sum:", add(a,b))
    print("Difference:", subtract(a, b))
    print("Product:", multiply(a, b))
    print("Quotient:", divide(a, b))

    # This is a long line that pylint will flag just for demonstration purposes to show how it works.
    long_variable_name_for_no_good_reason = "This is just to make the line exceed the character limit for pylint."
    print(long_variable_name_for_no_good_reason)

if __name__ == "__main__":
    main()