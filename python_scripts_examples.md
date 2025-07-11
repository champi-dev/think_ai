# Python Script Examples

Here are some Python scripts that cover a variety of topics in different areas of science.

## 1. Simple Calculator

A basic calculator for performing arithmetic operations.

```python
def simple_calculator():
    print("Simple Calculator")
    num1 = float(input("Enter first number: "))
    operator = input("Enter operator (+, -, *, /): ")
    num2 = float(input("Enter second number: "))
    
    if operator == '+':
        result = num1 + num2
    elif operator == '-':
        result = num1 - num2
    elif operator == '*':
        result = num1 * num2
    elif operator == '/':
        if num2 != 0:
            result = num1 / num2
        else:
            result = "Error! Division by zero is not allowed."
    else:
        result = "Invalid operator"
    
    print(f"Result: {result}")

simple_calculator()
```

## 2. Temperature Conversion

Convert temperatures between Celsius and Fahrenheit.

```python
def temperature_converter():
    print("Temperature Converter")
    unit = input("Enter 'C' for Celsius or 'F' for Fahrenheit: ").upper()
    
    if unit == 'C':
        celsius = float(input("Enter temperature in Celsius: "))
        fahrenheit = (celsius * 9/5) + 32
        print(f"{celsius}°C is {fahrenheit:.2f}°F")
    elif unit == 'F':
        fahrenheit = float(input("Enter temperature in Fahrenheit: "))
        celsius = (fahrenheit - 32) * 5/9
        print(f"{fahrenheit}°F is {celsius:.2f}°C")
    else:
        print("Invalid input")

temperature_converter()
```

## 3. Fibonacci Sequence Generator

Generate the Fibonacci sequence up to a specified number of terms.

```python
def fibonacci_sequence():
    num_terms = int(input("Enter the number of terms: "))
    
    if num_terms <= 0:
        print("Please enter a positive integer.")
    elif num_terms == 1:
        fib_sequence = [0]
    else:
        fib_sequence = [0, 1]
        for i in range(2, num_terms):
            next_term = fib_sequence[-1] + fib_sequence[-2]
            fib_sequence.append(next_term)
    
    print(f"Fibonacci sequence up to {num_terms} terms: {fib_sequence}")

fibonacci_sequence()
```

## 4. Gravity and Motion Calculator

Calculate motion under gravity (free fall).

```python
def gravity_motion():
    print("Gravity and Motion Calculator")
    g = 9.81  # acceleration due to gravity (m/s²)
    
    initial_velocity = float(input("Enter initial velocity (m/s): "))
    time = float(input("Enter time (seconds): "))
    
    # Calculate final velocity: v = u + gt
    final_velocity = initial_velocity + g * time
    
    # Calculate distance: s = ut + 0.5gt²
    distance = initial_velocity * time + 0.5 * g * time**2
    
    print(f"\nResults:")
    print(f"Final velocity: {final_velocity:.2f} m/s")
    print(f"Distance fallen: {distance:.2f} m")

gravity_motion()
```