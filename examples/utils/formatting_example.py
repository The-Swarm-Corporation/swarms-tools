"""
Formatting Utilities Example

This example demonstrates how to use the formatting utility functions to convert
Python objects into well-formatted strings for display and logging purposes.

Requirements:
- Install required dependencies: loguru

Usage:
    python formatting_example.py
"""

from loguru import logger
from swarms_tools.utils.format_dict_into_str import format_dict_into_str
from swarms_tools.utils.formatted_string import format_object_to_string


def main():
    """
    Main function demonstrating formatting utilities usage.
    """
    logger.info("Starting Formatting Utilities example...")
    
    try:
        # Example 1: Basic dictionary formatting
        logger.info("Example 1: Basic dictionary formatting")
        
        simple_dict = {
            "name": "Alice Johnson",
            "age": 30,
            "city": "New York",
            "occupation": "Software Engineer"
        }
        
        formatted_simple = format_dict_into_str(simple_dict)
        logger.info("Simple dictionary formatted:")
        logger.info(formatted_simple)
        
        # Example 2: Complex nested object formatting
        logger.info("Example 2: Complex nested object formatting")
        
        complex_data = {
            "user_profile": {
                "personal_info": {
                    "name": "Bob Smith",
                    "age": 28,
                    "email": "bob.smith@example.com"
                },
                "professional_info": {
                    "company": "Tech Corp",
                    "position": "Senior Developer",
                    "skills": ["Python", "JavaScript", "React", "Node.js"],
                    "experience_years": 5
                },
                "preferences": {
                    "notifications": True,
                    "theme": "dark",
                    "language": "en"
                }
            },
            "activity_log": [
                {"action": "login", "timestamp": "2024-01-15T10:30:00Z"},
                {"action": "view_profile", "timestamp": "2024-01-15T10:31:00Z"},
                {"action": "update_settings", "timestamp": "2024-01-15T10:32:00Z"}
            ],
            "statistics": {
                "total_logins": 150,
                "last_login": "2024-01-15T10:30:00Z",
                "account_age_days": 365
            }
        }
        
        formatted_complex = format_object_to_string(complex_data)
        logger.info("Complex object formatted:")
        logger.info(formatted_complex)
        
        # Example 3: List formatting
        logger.info("Example 3: List formatting")
        
        list_data = [
            {"product": "Laptop", "price": 999.99, "category": "Electronics"},
            {"product": "Mouse", "price": 29.99, "category": "Accessories"},
            {"product": "Keyboard", "price": 79.99, "category": "Accessories"},
            {"product": "Monitor", "price": 299.99, "category": "Electronics"}
        ]
        
        formatted_list = format_object_to_string(list_data)
        logger.info("List formatted:")
        logger.info(formatted_list)
        
        # Example 4: Mixed data types
        logger.info("Example 4: Mixed data types")
        
        mixed_data = {
            "string_value": "Hello World",
            "number_value": 42,
            "float_value": 3.14159,
            "boolean_value": True,
            "null_value": None,
            "list_value": [1, 2, 3, "four", 5.0],
            "nested_dict": {
                "inner_string": "Nested content",
                "inner_number": 100,
                "inner_list": ["a", "b", "c"]
            }
        }
        
        formatted_mixed = format_object_to_string(mixed_data)
        logger.info("Mixed data types formatted:")
        logger.info(formatted_mixed)
        
        # Example 5: API response formatting
        logger.info("Example 5: API response formatting")
        
        api_response = {
            "status": "success",
            "data": {
                "users": [
                    {
                        "id": 1,
                        "name": "John Doe",
                        "email": "john@example.com",
                        "permissions": ["read", "write"]
                    },
                    {
                        "id": 2,
                        "name": "Jane Smith", 
                        "email": "jane@example.com",
                        "permissions": ["read"]
                    }
                ],
                "pagination": {
                    "page": 1,
                    "per_page": 10,
                    "total": 2,
                    "total_pages": 1
                }
            },
            "message": "Users retrieved successfully"
        }
        
        formatted_api = format_object_to_string(api_response)
        logger.info("API response formatted:")
        logger.info(formatted_api)
        
        # Example 6: Configuration formatting
        logger.info("Example 6: Configuration formatting")
        
        config_data = {
            "database": {
                "host": "localhost",
                "port": 5432,
                "name": "myapp_db",
                "credentials": {
                    "username": "admin",
                    "password": "secret123"
                }
            },
            "redis": {
                "host": "localhost",
                "port": 6379,
                "db": 0
            },
            "logging": {
                "level": "INFO",
                "file": "app.log",
                "max_size": "10MB",
                "backup_count": 5
            }
        }
        
        formatted_config = format_object_to_string(config_data)
        logger.info("Configuration formatted:")
        logger.info(formatted_config)
        
        # Example 7: Custom indentation
        logger.info("Example 7: Custom indentation")
        
        custom_indent_data = {
            "level1": {
                "level2": {
                    "level3": {
                        "value": "Deeply nested value"
                    }
                }
            }
        }
        
        formatted_custom = format_object_to_string(custom_indent_data, indent=2)
        logger.info("Custom indentation (2 spaces):")
        logger.info(formatted_custom)
        
        formatted_custom_wide = format_object_to_string(custom_indent_data, indent=8)
        logger.info("Custom indentation (8 spaces):")
        logger.info(formatted_custom_wide)
        
        # Example 8: Large dataset formatting
        logger.info("Example 8: Large dataset formatting")
        
        large_dataset = {
            "metadata": {
                "total_records": 1000,
                "generated_at": "2024-01-15T10:30:00Z",
                "version": "1.0"
            },
            "records": [
                {
                    "id": i,
                    "name": f"Record {i}",
                    "value": i * 10,
                    "category": "A" if i % 2 == 0 else "B"
                }
                for i in range(1, 6)  # Show first 5 records
            ]
        }
        
        formatted_large = format_object_to_string(large_dataset)
        logger.info("Large dataset formatted (first 5 records):")
        logger.info(formatted_large)
        
        # Example 9: Error handling
        logger.info("Example 9: Error handling")
        
        try:
            # Test with invalid data
            invalid_data = {"key": object()}  # object() is not serializable
            formatted_invalid = format_object_to_string(invalid_data)
            logger.info("Invalid data formatted:")
            logger.info(formatted_invalid)
        except Exception as e:
            logger.warning(f"Expected error with invalid data: {e}")
        
        # Example 10: Performance comparison
        logger.info("Example 10: Performance comparison")
        
        import time
        
        # Test with different data sizes
        small_data = {"key": "value"}
        medium_data = {f"key_{i}": f"value_{i}" for i in range(100)}
        large_data = {f"key_{i}": f"value_{i}" for i in range(1000)}
        
        # Time small data
        start_time = time.time()
        format_object_to_string(small_data)
        small_time = time.time() - start_time
        
        # Time medium data
        start_time = time.time()
        format_object_to_string(medium_data)
        medium_time = time.time() - start_time
        
        # Time large data
        start_time = time.time()
        format_object_to_string(large_data)
        large_time = time.time() - start_time
        
        logger.info(f"Small data formatting time: {small_time:.4f}s")
        logger.info(f"Medium data formatting time: {medium_time:.4f}s")
        logger.info(f"Large data formatting time: {large_time:.4f}s")
        
        # Example 11: Different formatting styles
        logger.info("Example 11: Different formatting styles")
        
        sample_data = {
            "user": {
                "name": "John Doe",
                "age": 30,
                "hobbies": ["reading", "swimming", "coding"]
            }
        }
        
        # Default indentation (4 spaces)
        default_formatted = format_object_to_string(sample_data)
        logger.info("Default indentation (4 spaces):")
        logger.info(default_formatted)
        
        # Compact indentation (1 space)
        compact_formatted = format_object_to_string(sample_data, indent=1)
        logger.info("Compact indentation (1 space):")
        logger.info(compact_formatted)
        
        # Wide indentation (8 spaces)
        wide_formatted = format_object_to_string(sample_data, indent=8)
        logger.info("Wide indentation (8 spaces):")
        logger.info(wide_formatted)
        
        logger.info("Formatting Utilities examples completed successfully!")
        logger.info("Note: These utilities are optimized for logging and display purposes")
        logger.info("They handle nested structures and provide clean, readable output")
        
    except Exception as e:
        logger.error(f"Error with formatting utilities: {e}")


if __name__ == "__main__":
    main()
