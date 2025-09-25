def modify_file_content(
    file_path: str,
    old_content: str,
    new_content: str
) -> str:
    """
    Efficiently modify ONLY the specified string content in a file.

    Args:
        file_path (str): Path to the file to modify.
        old_content (str): The old string to be replaced (must be a string).
        new_content (str): The new string to replace the old one (must be a string).

    Returns:
        str: A message indicating the result of the operation.
    """
    try:
        # Read the current file contents
        with open(file_path, 'r') as file:
            content = file.read()

        # Replace the old content with the new content
        if old_content not in content:
            return f"Old content not found in {file_path}."

        modified_content = content.replace(old_content, new_content)

        # Write back to the file
        with open(file_path, 'w') as file:
            file.write(modified_content)

        message = (
            f"Transfer complete: Updated {file_path}.\n"
            f"Replaced: {old_content}\nWith: {new_content}"
        )
        print(message)
        return message
    except Exception as e:
        error_message = f"Failed to update {file_path}: {str(e)}"
        print(error_message)
        return error_message

# # Example usage
# if __name__ == '__main__':
#     file_path = '/Users/akshparekh/Documents/swarms-tools/exa_search_api.py'
#     old_content = '"What are the best performing semiconductor stocks?"'
#     new_content = '"What are the top AI semiconductor companies?"'
#     modify_file_content(file_path, old_content, new_content)