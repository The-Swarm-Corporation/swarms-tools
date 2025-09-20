import os
from swarms_tools.evolver.self_evolve import modify_file_content

# Create a sample file to modify
sample_file = "temp_sample_file.py"
original_content = '''def hello_world():
    """A simple hello world function."""
    print("Hello, World!")
    return "Hello, World!"

if __name__ == "__main__":
    hello_world()
'''

# Write the original content to a temporary file
with open(sample_file, 'w') as f:
    f.write(original_content)

print("Original content:")
print(original_content)

# Define the modification
old_content = 'print("Hello, World!")'
new_content = 'print("Hello, Evolved World!")'

# Apply the modification
result = modify_file_content(sample_file, old_content, new_content)
print(f"Modification result: {result}")

# Read and display the modified content
with open(sample_file, 'r') as f:
    modified_content = f.read()

print("\nModified file content:")
print(modified_content)

# Demonstrate multiple modifications on a more complex file
complex_file = "temp_complex_file.py"
complex_content = '''class Calculator:
    def __init__(self):
        self.result = 0
    
    def divide(self, x, y):
        if y == 0:
            return "Error: Division by zero"
        return x / y

calc = Calculator()
print(calc.divide(10, 2))
'''

with open(complex_file, 'w') as f:
    f.write(complex_content)

# First modification: Improve error handling
old_error = 'if y == 0:\n            return "Error: Division by zero"'
new_error = 'if y == 0:\n            raise ValueError("Division by zero is not allowed")'

result1 = modify_file_content(complex_file, old_error, new_error)
print(f"\nError handling modification: {result1}")

# Second modification: Add logging
old_init = 'def __init__(self):\n        self.result = 0'
new_init = 'def __init__(self):\n        self.result = 0\n        print("Calculator initialized")'

result2 = modify_file_content(complex_file, old_init, new_init)
print(f"Logging modification: {result2}")

# Read final modified content
with open(complex_file, 'r') as f:
    final_content = f.read()

print("\nFinal modified content:")
print(final_content)

# Clean up
os.remove(sample_file)
os.remove(complex_file)
print("\nCleaned up temporary files")
