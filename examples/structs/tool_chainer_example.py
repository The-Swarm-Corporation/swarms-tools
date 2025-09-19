"""
Tool Chainer Example

This example demonstrates how to use the tool chainer utility to execute multiple tools
in parallel or sequentially, with proper error handling and result aggregation.

Requirements:
- Install required dependencies: loguru, concurrent.futures

Usage:
    python tool_chainer_example.py
"""

import time
import random
from loguru import logger
from swarms_tools.structs.tool_chainer import tool_chainer


def sample_tool_1():
    """
    Sample tool that simulates a quick operation.
    """
    logger.info("Executing sample tool 1...")
    time.sleep(0.5)  # Simulate work
    return "Tool 1 completed successfully"


def sample_tool_2():
    """
    Sample tool that simulates a medium operation.
    """
    logger.info("Executing sample tool 2...")
    time.sleep(1.0)  # Simulate work
    return "Tool 2 completed successfully"


def sample_tool_3():
    """
    Sample tool that simulates a longer operation.
    """
    logger.info("Executing sample tool 3...")
    time.sleep(1.5)  # Simulate work
    return "Tool 3 completed successfully"


def sample_tool_with_error():
    """
    Sample tool that simulates an error condition.
    """
    logger.info("Executing sample tool with error...")
    time.sleep(0.3)  # Simulate work
    raise ValueError("Simulated error in tool execution")


def sample_tool_random():
    """
    Sample tool with random execution time.
    """
    delay = random.uniform(0.1, 2.0)
    logger.info(f"Executing random tool with delay: {delay:.2f}s")
    time.sleep(delay)
    return f"Random tool completed after {delay:.2f}s"


def main():
    """
    Main function demonstrating tool chainer usage.
    """
    logger.info("Starting Tool Chainer example...")
    
    try:
        # Example 1: Parallel execution of multiple tools
        logger.info("Example 1: Parallel execution")
        tools_parallel = [sample_tool_1, sample_tool_2, sample_tool_3]
        
        start_time = time.time()
        parallel_results = tool_chainer(tools_parallel, parallel=True)
        parallel_duration = time.time() - start_time
        
        logger.info(f"Parallel execution completed in {parallel_duration:.2f} seconds")
        logger.info(f"Parallel results:\n{parallel_results}")
        
        # Example 2: Sequential execution of multiple tools
        logger.info("Example 2: Sequential execution")
        tools_sequential = [sample_tool_1, sample_tool_2, sample_tool_3]
        
        start_time = time.time()
        sequential_results = tool_chainer(tools_sequential, parallel=False)
        sequential_duration = time.time() - start_time
        
        logger.info(f"Sequential execution completed in {sequential_duration:.2f} seconds")
        logger.info(f"Sequential results:\n{sequential_results}")
        
        # Example 3: Mixed execution with error handling
        logger.info("Example 3: Mixed execution with error handling")
        tools_mixed = [sample_tool_1, sample_tool_with_error, sample_tool_2]
        
        mixed_results = tool_chainer(tools_mixed, parallel=True)
        logger.info(f"Mixed execution results:\n{mixed_results}")
        
        # Example 4: Random execution times to demonstrate parallel benefits
        logger.info("Example 4: Random execution times")
        random_tools = [sample_tool_random for _ in range(5)]
        
        start_time = time.time()
        random_results = tool_chainer(random_tools, parallel=True)
        random_parallel_duration = time.time() - start_time
        
        start_time = time.time()
        random_sequential_results = tool_chainer(random_tools, parallel=False)
        random_sequential_duration = time.time() - start_time
        
        logger.info(f"Random parallel execution: {random_parallel_duration:.2f}s")
        logger.info(f"Random sequential execution: {random_sequential_duration:.2f}s")
        logger.info(f"Speed improvement: {random_sequential_duration/random_parallel_duration:.2f}x")
        
        # Example 5: Real-world tool simulation
        logger.info("Example 5: Real-world tool simulation")
        
        def fetch_user_data():
            """Simulate fetching user data from API."""
            time.sleep(0.8)
            return {"users": 150, "active": 120}
        
        def fetch_analytics():
            """Simulate fetching analytics data."""
            time.sleep(1.2)
            return {"page_views": 5000, "sessions": 800}
        
        def fetch_notifications():
            """Simulate fetching notifications."""
            time.sleep(0.6)
            return {"unread": 5, "total": 25}
        
        real_world_tools = [fetch_user_data, fetch_analytics, fetch_notifications]
        
        start_time = time.time()
        real_world_results = tool_chainer(real_world_tools, parallel=True)
        real_world_duration = time.time() - start_time
        
        logger.info(f"Real-world parallel execution: {real_world_duration:.2f}s")
        logger.info(f"Real-world results:\n{real_world_results}")
        
        # Example 6: Large number of tools
        logger.info("Example 6: Large number of tools")
        
        def quick_tool(i):
            """Quick tool with index."""
            time.sleep(0.1)
            return f"Quick tool {i} completed"
        
        large_tool_list = [lambda i=i: quick_tool(i) for i in range(10)]
        
        start_time = time.time()
        large_parallel_results = tool_chainer(large_tool_list, parallel=True)
        large_parallel_duration = time.time() - start_time
        
        start_time = time.time()
        large_sequential_results = tool_chainer(large_tool_list, parallel=False)
        large_sequential_duration = time.time() - start_time
        
        logger.info(f"Large parallel execution: {large_parallel_duration:.2f}s")
        logger.info(f"Large sequential execution: {large_sequential_duration:.2f}s")
        logger.info(f"Speed improvement: {large_sequential_duration/large_parallel_duration:.2f}x")
        
        # Example 7: Error recovery
        logger.info("Example 7: Error recovery demonstration")
        
        def reliable_tool():
            """A reliable tool that always succeeds."""
            time.sleep(0.2)
            return "Reliable tool completed"
        
        def unreliable_tool():
            """An unreliable tool that sometimes fails."""
            time.sleep(0.3)
            if random.random() < 0.5:  # 50% chance of failure
                raise RuntimeError("Random failure occurred")
            return "Unreliable tool completed"
        
        error_recovery_tools = [reliable_tool, unreliable_tool, reliable_tool]
        
        error_recovery_results = tool_chainer(error_recovery_tools, parallel=True)
        logger.info(f"Error recovery results:\n{error_recovery_results}")
        
        # Example 8: Performance comparison
        logger.info("Example 8: Performance comparison")
        
        def cpu_intensive_tool():
            """Simulate CPU-intensive work."""
            time.sleep(0.5)
            # Simulate some computation
            result = sum(i * i for i in range(1000))
            return f"CPU intensive result: {result}"
        
        cpu_tools = [cpu_intensive_tool for _ in range(4)]
        
        start_time = time.time()
        cpu_parallel_results = tool_chainer(cpu_tools, parallel=True)
        cpu_parallel_duration = time.time() - start_time
        
        start_time = time.time()
        cpu_sequential_results = tool_chainer(cpu_tools, parallel=False)
        cpu_sequential_duration = time.time() - start_time
        
        logger.info(f"CPU intensive parallel: {cpu_parallel_duration:.2f}s")
        logger.info(f"CPU intensive sequential: {cpu_sequential_duration:.2f}s")
        logger.info(f"Speed improvement: {cpu_sequential_duration/cpu_parallel_duration:.2f}x")
        
        logger.info("Tool Chainer examples completed successfully!")
        logger.info("Note: Parallel execution is most beneficial for I/O-bound operations")
        logger.info("Sequential execution may be better for CPU-bound operations with shared resources")
        
    except Exception as e:
        logger.error(f"Error with tool chainer: {e}")


if __name__ == "__main__":
    main()
