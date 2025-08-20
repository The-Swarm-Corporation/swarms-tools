import os
import subprocess
from loguru import logger


def code_executor_wrapper(
    code: str,
    max_output_length: int = 1000,
    artifacts_directory: str = "artifacts",
    language: str = "python3",
) -> str:
    """
    Function wrapper to execute Python code and return the output as a string.
    Logs input and output using loguru and stores outputs in 'artifacts' folder.

    Args:
        code (str): The Python code to execute.
        max_output_length (int): Maximum length of output to return.
        artifacts_directory (str): Directory to store artifacts and logs.
        language (str): Python interpreter to use (default: python3).

    Returns:
        str: The output of the executed code.

    Raises:
        RuntimeError: If there is an error during the execution of the code.
        ValueError: If the code cannot be formatted.
    """

    os.makedirs(artifacts_directory, exist_ok=True)
    logger.info("Logger initialized and artifacts directory set up.")

    def format_code(code: str) -> str:
        try:
            import black

            formatted_code = black.format_str(
                code, mode=black.FileMode()
            )
            return formatted_code
        except Exception as e:
            logger.error(f"Error formatting code: {e}")
            raise ValueError(f"Error formatting code: {e}") from e

    try:
        formatted_code = format_code(code)
        logger.info(f"Executing code:\n{formatted_code}")
        completed_process = subprocess.run(
            [language, "-c", formatted_code],
            capture_output=True,
            text=True,
            check=True,
        )
        output = completed_process.stdout
        logger.info(f"Code output:\n{output}")
        return output
    except subprocess.CalledProcessError as e:
        logger.error(f"Error executing code: {e.stderr}")
        raise RuntimeError(f"Error executing code: {e.stderr}") from e
