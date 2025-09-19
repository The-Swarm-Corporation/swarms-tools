"""
Code Executor Example

This example demonstrates how to use the code executor tool to safely execute Python code
and capture the output. The tool formats code using Black and stores artifacts in a directory.

Requirements:
- Install required dependencies: black, loguru

Usage:
    python code_executor_example.py
"""

import os
from loguru import logger
from swarms_tools.devs.code_executor import code_executor_wrapper


def main():
    """
    Main function demonstrating code executor usage.
    """
    logger.info("Starting Code Executor example...")
    
    try:
        # Example 1: Simple mathematical calculation
        logger.info("Example 1: Simple mathematical calculation")
        math_code = """
import math

# Calculate the area of a circle
radius = 5
area = math.pi * radius ** 2
print(f"Area of circle with radius {radius}: {area:.2f}")

# Calculate factorial
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

result = factorial(5)
print(f"Factorial of 5: {result}")
"""
        
        result1 = code_executor_wrapper(
            code=math_code,
            max_output_length=1000,
            artifacts_directory="artifacts/example1"
        )
        logger.info(f"Math calculation result:\n{result1}")
        
        # Example 2: Data processing
        logger.info("Example 2: Data processing example")
        data_code = """
import json
from datetime import datetime

# Create sample data
data = {
    "users": [
        {"name": "Alice", "age": 30, "city": "New York"},
        {"name": "Bob", "age": 25, "city": "San Francisco"},
        {"name": "Charlie", "age": 35, "city": "Chicago"}
    ],
    "timestamp": datetime.now().isoformat()
}

# Process data
total_users = len(data["users"])
avg_age = sum(user["age"] for user in data["users"]) / total_users
cities = [user["city"] for user in data["users"]]

print(f"Total users: {total_users}")
print(f"Average age: {avg_age:.1f}")
print(f"Cities: {', '.join(set(cities))}")
print(f"Data timestamp: {data['timestamp']}")
"""
        
        result2 = code_executor_wrapper(
            code=data_code,
            max_output_length=1000,
            artifacts_directory="artifacts/example2"
        )
        logger.info(f"Data processing result:\n{result2}")
        
        # Example 3: Error handling example
        logger.info("Example 3: Error handling example")
        error_code = """
# This will cause an error
undefined_variable = some_undefined_function()
print("This won't be reached")
"""
        
        try:
            result3 = code_executor_wrapper(
                code=error_code,
                max_output_length=1000,
                artifacts_directory="artifacts/example3"
            )
            logger.info(f"Error handling result:\n{result3}")
        except Exception as e:
            logger.info(f"Expected error caught: {e}")
        
        # Example 4: File operations
        logger.info("Example 4: File operations")
        file_code = """
import os
import tempfile

# Create a temporary file and write to it
with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
    f.write("Hello from code executor!")
    temp_file = f.name

# Read the file back
with open(temp_file, 'r') as f:
    content = f.read()

print(f"File content: {content}")
print(f"File size: {os.path.getsize(temp_file)} bytes")

# Clean up
os.unlink(temp_file)
print("Temporary file cleaned up")
"""
        
        result4 = code_executor_wrapper(
            code=file_code,
            max_output_length=1000,
            artifacts_directory="artifacts/example4"
        )
        logger.info(f"File operations result:\n{result4}")
        
        # Example 5: Network operations (basic)
        logger.info("Example 5: Network operations")
        network_code = """
import urllib.request
import json

# Simple HTTP request
try:
    response = urllib.request.urlopen('https://httpbin.org/json')
    data = json.loads(response.read().decode())
    print(f"HTTP request successful")
    print(f"Response keys: {list(data.keys())}")
except Exception as e:
    print(f"Network request failed: {e}")
"""
        
        result5 = code_executor_wrapper(
            code=network_code,
            max_output_length=1000,
            artifacts_directory="artifacts/example5"
        )
        logger.info(f"Network operations result:\n{result5}")
        
        # Example 6: Different language (python vs python3)
        logger.info("Example 6: Using different Python interpreter")
        try:
            result6 = code_executor_wrapper(
                code="print('Hello from Python!')",
                language="python",  # Try python instead of python3
                artifacts_directory="artifacts/example6"
            )
            logger.info(f"Python interpreter result:\n{result6}")
        except Exception as e:
            logger.warning(f"Python interpreter not available: {e}")
        
        logger.info("Code Executor examples completed successfully!")
        logger.info("Check the artifacts/ directory for stored outputs and logs")
        
    except Exception as e:
        logger.error(f"Error with code executor: {e}")


if __name__ == "__main__":
    main()
