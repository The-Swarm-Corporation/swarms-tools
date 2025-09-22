import os
from swarms_tools.evolver.self_evolve import modify_file_content

# Test that the function exists and is callable
assert callable(modify_file_content)

# Create a sample file to test modification
sample_file = "temp_sample_file.py"
original_content = '''def hello_world():
    """A simple hello world function."""
    print("Hello, World!")
    return "Hello, World!"

if __name__ == "__main__":
    hello_world()
'''

# Write the original content
with open(sample_file, 'w') as f:
    f.write(original_content)

# Test file modification functionality
old_content = 'print("Hello, World!")'
new_content = 'print("Hello, Evolved World!")'

result = modify_file_content(sample_file, old_content, new_content)
assert result is not None

# Verify the modification worked by reading the file
with open(sample_file, 'r') as f:
    modified_content = f.read()

assert "Hello, Evolved World!" in modified_content
assert "Hello, World!" not in modified_content

# Test multiple modifications on a complex file
complex_file = "temp_complex_file.py"
complex_content = '''class Calculator:
    def __init__(self):
        self.result = 0
    
    def divide(self, x, y):
        if y == 0:
            return "Error: Division by zero"
        return x / y
'''

with open(complex_file, 'w') as f:
    f.write(complex_content)

# Test error handling improvement
old_error = 'if y == 0:\n            return "Error: Division by zero"'
new_error = 'if y == 0:\n            raise ValueError("Division by zero is not allowed")'

result1 = modify_file_content(complex_file, old_error, new_error)
assert result1 is not None

# Verify the change was applied
with open(complex_file, 'r') as f:
    final_content = f.read()

assert "raise ValueError" in final_content
assert "return \"Error: Division by zero\"" not in final_content

# Test that the function handles non-existent content gracefully
result2 = modify_file_content(complex_file, "non_existent_content", "replacement")
assert result2 is not None  # Should return some result even if no change made

# Clean up test files
os.remove(sample_file)
os.remove(complex_file)
