"""
Self Evolution Example

This example demonstrates how to use the self-evolution tools to enable AI agents
to modify and improve their own code and behavior over time.

Requirements:
- Install required dependencies: loguru, python-dotenv
- The self-evolution tool may require additional dependencies based on implementation

Usage:
    python self_evolve_example.py
"""

import os
from dotenv import load_dotenv
from loguru import logger
from swarms_tools.evolver.self_evolve import modify_file_content

# Load environment variables
load_dotenv()


def main():
    """
    Main function demonstrating self-evolution capabilities.
    """
    logger.info("Starting Self Evolution example...")
    
    try:
        # Example 1: Modify file content using the self-evolution tool
        logger.info("Example 1: Modifying file content")
        
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
        
        logger.info(f"Created sample file: {sample_file}")
        logger.info("Original content:")
        logger.info(original_content)
        
        # Define the modification
        old_content = 'print("Hello, World!")'
        new_content = 'print("Hello, Evolved World!")'
        
        # Apply the modification
        result = modify_file_content(sample_file, old_content, new_content)
        logger.info(f"Modification result: {result}")
        
        # Read and display the modified content
        with open(sample_file, 'r') as f:
            modified_content = f.read()
        
        logger.info("Modified file content:")
        logger.info(modified_content)
        
        # Clean up the temporary file
        os.remove(sample_file)
        logger.info("Cleaned up temporary file")
        
        # Example 2: Multiple modifications
        logger.info("Example 2: Multiple modifications")
        
        # Create a more complex sample file
        complex_file = "temp_complex_file.py"
        complex_content = '''class Calculator:
    def __init__(self):
        self.result = 0
    
    def add(self, x, y):
        return x + y
    
    def multiply(self, x, y):
        return x * y
    
    def divide(self, x, y):
        if y == 0:
            return "Error: Division by zero"
        return x / y

# Test the calculator
calc = Calculator()
print(calc.add(5, 3))
print(calc.multiply(4, 6))
print(calc.divide(10, 2))
'''
        
        with open(complex_file, 'w') as f:
            f.write(complex_content)
        
        logger.info(f"Created complex sample file: {complex_file}")
        
        # First modification: Add error handling
        old_error_handling = 'if y == 0:\n            return "Error: Division by zero"'
        new_error_handling = 'if y == 0:\n            raise ValueError("Division by zero is not allowed")'
        
        result1 = modify_file_content(complex_file, old_error_handling, new_error_handling)
        logger.info(f"Error handling modification: {result1}")
        
        # Second modification: Add logging
        old_init = 'def __init__(self):\n        self.result = 0'
        new_init = 'def __init__(self):\n        self.result = 0\n        print("Calculator initialized")'
        
        result2 = modify_file_content(complex_file, old_init, new_init)
        logger.info(f"Logging modification: {result2}")
        
        # Read and display the final modified content
        with open(complex_file, 'r') as f:
            final_content = f.read()
        
        logger.info("Final modified content:")
        logger.info(final_content)
        
        # Clean up
        os.remove(complex_file)
        logger.info("Cleaned up complex file")
        
        # Example 3: Demonstrate evolution workflow
        logger.info("Example 3: Evolution workflow demonstration")
        
        # This would typically involve:
        # 1. Analyzing current performance
        # 2. Identifying areas for improvement
        # 3. Generating new code variants
        # 4. Testing the variants
        # 5. Selecting the best performing variant
        # 6. Updating the agent's code
        
        evolution_steps = [
            "1. Performance Analysis: Monitor agent performance metrics",
            "2. Code Analysis: Identify bottlenecks and improvement opportunities", 
            "3. Variant Generation: Create new code implementations",
            "4. Testing: Evaluate variants against test cases",
            "5. Selection: Choose the best performing variant",
            "6. Integration: Update the agent with the new code"
        ]
        
        for step in evolution_steps:
            logger.info(step)
        
        # Example 4: Self-modification safety considerations
        logger.info("Example 4: Self-modification safety considerations")
        
        safety_guidelines = [
            "Always backup original code before modifications",
            "Test modifications in isolated environments",
            "Implement rollback mechanisms",
            "Monitor for unintended side effects",
            "Validate modifications against safety constraints",
            "Maintain version control of evolved code"
        ]
        
        for guideline in safety_guidelines:
            logger.info(f"Safety: {guideline}")
        
        # Example 5: Error handling in modifications
        logger.info("Example 5: Error handling in modifications")
        
        # Try to modify content that doesn't exist
        error_file = "temp_error_file.py"
        with open(error_file, 'w') as f:
            f.write("print('Hello, World!')")
        
        # Try to replace content that doesn't exist
        result_error = modify_file_content(error_file, "print('Goodbye, World!')", "print('Hello, Universe!')")
        logger.info(f"Error handling result: {result_error}")
        
        # Clean up
        os.remove(error_file)
        logger.info("Cleaned up error test file")
        
        logger.info("Self Evolution examples completed successfully!")
        logger.info("Note: This tool enables safe code modification with proper error handling")
        
    except Exception as e:
        logger.error(f"Error with self-evolution: {e}")
        logger.info("Make sure the self-evolution tool is properly configured")


if __name__ == "__main__":
    main()
