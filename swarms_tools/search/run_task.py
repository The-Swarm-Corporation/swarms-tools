"""
Runs the task at hand in a certain time frame and a certain time.
Compared to just running it, this makes sure the task is completed in the assigned timeframe.

This tool provides controlled execution of tasks with:
- Time-based execution constraints
- Integration with task management system

Args taken:
- task_name: Name of the task to run
- task_func: The function to execute as the task
- args: Tuple of positional arguments to pass to the task function
- kwargs: Dictionary of keyword arguments to pass to the task function
- timeout_seconds: Maximum allowed time (in seconds) for task execution
- time_start: Optional datetime specifying when to start the task
- max_retries: Maximum number of retry attempts if the task fails
- task_plan: Optional TaskPlan object for task management integration
- task_id: Optional unique identifier for the task within the task plan

Example usage:
    result = run_task_with_timeout(
        task_name="Data Processing Task",
        task_func=my_data_processing_function,
        args=("input_data.csv", "output.json"),
        kwargs={"verbose": True},
        timeout_seconds=300,  # 5 minutes
        task_plan=current_task_plan,
        task_id="task_123"
    )
"""

import time
import threading
from datetime import datetime
from typing import Any, Dict, Callable, Optional, Tuple, Union

class TaskTimeoutError(Exception):
    """Custom exception for task timeout"""
    pass


class TaskExecutionError(Exception):
    """Custom exception for task execution errors"""
    pass


class TaskRunner:
    """
    A comprehensive task runner with timeout and monitoring capabilities.
    
    This class provides:
    - Controlled execution with timeouts
    - Resource monitoring
    - Integration with task management system
    - Detailed logging and reporting
    """
    
    def __init__(self, 
                 task_name: str,
                 timeout_seconds: Union[int, float],
                 time_start: Optional[datetime] = None,
                 max_retries: int = 0):
        """
        Initialize the TaskRunner.
        
        Args:
            task_name: Name of the task to run
            timeout_seconds: Maximum time allowed for task execution
            time_start: When the task should start (optional)
            max_retries: Maximum number of retry attempts on failure
        """
        self.task_name = task_name
        self.timeout_seconds = timeout_seconds
        self.time_start = time_start or datetime.now()
        self.max_retries = max_retries
        
        # Execution tracking
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.execution_time: Optional[float] = None
        self.retries_used = 0
        self.success = False
        self.error_message: Optional[str] = None
        
        # Resource tracking
        self.memory_usage: Optional[float] = None
        self.cpu_usage: Optional[float] = None
        
        print(f"   TaskRunner initialized for: {task_name}")
        print(f"   Timeout: {timeout_seconds} seconds")
        print(f"   Scheduled start: {self.time_start}")
    
    def _wait_for_start_time(self) -> bool:
        """Wait until the scheduled start time if specified."""
        if self.time_start and datetime.now() < self.time_start:
            wait_seconds = (self.time_start - datetime.now()).total_seconds()
            print(f"   Waiting {wait_seconds:.1f} seconds until scheduled start time...")
            
            if wait_seconds > 0:
                time.sleep(wait_seconds)
                return True
        return True
    
    def _execute_with_timeout(self, task_func: Callable, args: Tuple, kwargs: Dict) -> Any:
        """
        Execute the task function with timeout protection.
        
        Args:
            task_func: The function to execute
            args: Positional arguments for the function
            kwargs: Keyword arguments for the function
            
        Returns:
            The result of the task function
            
        Raises:
            TaskTimeoutError: If the task exceeds the timeout
            TaskExecutionError: If the task fails with an exception
        """
        result = None
        exception_raised = None
        
        def task_wrapper():
            nonlocal result, exception_raised
            try:
                result = task_func(*args, **kwargs)
            except Exception as e:
                exception_raised = e
        
        # Start the task in a separate thread
        task_thread = threading.Thread(target=task_wrapper, daemon=True)
        task_thread.start()
        
        # Wait for completion with timeout
        task_thread.join(timeout=self.timeout_seconds)
        
        if task_thread.is_alive():
            # Task is still running - it timed out
            raise TaskTimeoutError(f"Task '{self.task_name}' exceeded timeout of {self.timeout_seconds} seconds")
        
        if exception_raised:
            raise TaskExecutionError(f"Task '{self.task_name}' failed with error: {str(exception_raised)}")
        
        return result
    
    def _retry_execution(self, task_func: Callable, args: Tuple, kwargs: Dict) -> Any:
        """Execute task with retry logic."""
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                print(f"   Attempt {attempt + 1}/{self.max_retries + 1} for task: {self.task_name}")
                return self._execute_with_timeout(task_func, args, kwargs)
            except (TaskTimeoutError, TaskExecutionError) as e:
                last_exception = e
                self.retries_used = attempt + 1
                
                if attempt < self.max_retries:
                    wait_time = min(2 ** attempt, 30)  # Exponential backoff, max 30s
                    print(f"   Task failed, retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    print(f"   Task failed after {self.max_retries + 1} attempts")
        
        raise last_exception
    
    def run(self, task_func: Callable, args: Tuple = (), kwargs: Dict = {}) -> Dict[str, Any]:
        """
        Execute the task with full monitoring and control.
        
        Args:
            task_func: The function to execute
            args: Positional arguments for the function
            kwargs: Keyword arguments for the function
            
        Returns:
            Dictionary containing execution results and metadata
        """
        print(f"\nStarting task execution: {self.task_name}")
        print("=" * 60)
        
        # Wait for scheduled start time
        if not self._wait_for_start_time():
            return self._create_failure_result("Failed to wait for start time")
        
        self.start_time = datetime.now()
        
        try:
            # Execute the task (with retry logic if enabled)
            if self.max_retries > 0:
                result = self._retry_execution(task_func, args, kwargs)
            else:
                result = self._execute_with_timeout(task_func, args, kwargs)
            
            self.success = True
            print(f"Task '{self.task_name}' completed successfully")
            
        except TaskTimeoutError as e:
            self.success = False
            self.error_message = str(e)
            print(f"Task '{self.task_name}' timed out")
            
        except TaskExecutionError as e:
            self.success = False
            self.error_message = str(e)
            print(f"Task '{self.task_name}' failed with error")
            
        except Exception as e:
            self.success = False
            self.error_message = f"Unexpected error: {str(e)}"
            print(f"Unexpected error in task '{self.task_name}': {str(e)}")
        
        finally:
            self.end_time = datetime.now()
            self.execution_time = (self.end_time - self.start_time).total_seconds()
        
        return self._create_result(result if self.success else None)
    
    def _create_result(self, task_result: Any = None) -> Dict[str, Any]:
        """Create the result dictionary with execution metadata."""
        return {
            "task_name": self.task_name,
            "success": self.success,
            "result": task_result,
            "execution_time": self.execution_time,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "timeout_seconds": self.timeout_seconds,
            "retries_used": self.retries_used,
            "error_message": self.error_message,
            "scheduled_start": self.time_start.isoformat() if self.time_start else None
        }
    
    def _create_failure_result(self, message: str) -> Dict[str, Any]:
        """Create a failure result dictionary."""
        self.success = False
        self.error_message = message
        return self._create_result()


def run_task_with_timeout(
    task_name: str,
    task_func: Callable,
    args: Tuple = (),
    kwargs: Dict = {},
    timeout_seconds: Union[int, float] = 300,
    time_start: Optional[datetime] = None,
    max_retries: int = 0,
    task_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Convenience function to run a task with timeout and optional task management integration.
    
    Args:
        task_name: Name of the task
        task_func: Function to execute
        args: Positional arguments for the function
        kwargs: Keyword arguments for the function
        timeout_seconds: Timeout in seconds
        time_start: Scheduled start time
        max_retries: Maximum retry attempts
        task_plan: Optional TaskPlan for status updates
        task_id: Optional task ID for status updates
        
    Returns:
        Dictionary with execution results
    """
    
    runner = TaskRunner(
        task_name=task_name,
        timeout_seconds=timeout_seconds,
        time_start=time_start,
        max_retries=max_retries
    )
    
    result = runner.run(task_func, args, kwargs)
    
    return result



# # Example usage and testing functions
# def example_task_function(duration: int = 2, should_fail: bool = False) -> str:
#     """Example task function for testing."""
#     import time
#     
#     print(f"   Example task running for {duration} seconds...")
#     time.sleep(duration)
#     
#     if should_fail:
#         raise ValueError("Task intentionally failed")
#     
#     return f"Task completed successfully after {duration} seconds"
# 
# 
# def test_task_runner():
#     """Test function for the TaskRunner."""
#     print("Testing TaskRunner...")
#     
#     # Test 1: Successful task
#     print("\nTesting successful task:")
#     runner = TaskRunner("Test Task 1", timeout_seconds=10)
#     result = runner.run(example_task_function, args=(1,), kwargs={"should_fail": False})
#     print(f"Result: {result}")
#     
#     # Test 2: Timeout task
#     print("\nTesting timeout task:")
#     runner = TaskRunner("Test Task 2", timeout_seconds=1)
#     result = runner.run(example_task_function, args=(3,), kwargs={"should_fail": False})
#     print(f"Result: {result}")
#     
#     # Test 3: Failing task
#     print("\nTesting failing task:")
#     runner = TaskRunner("Test Task 3", timeout_seconds=10)
#     result = runner.run(example_task_function, args=(1,), kwargs={"should_fail": True})
#     print(f"Result: {result}")
#     
#     print("\nTaskRunner testing completed")
# 
# 
# if __name__ == "__main__":
#     # Run tests when executed directly
#     test_task_runner()