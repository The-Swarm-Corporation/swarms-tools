import time
import random
from swarms_tools.structs.tool_chainer import tool_chainer

def tool1():
    time.sleep(0.5)
    return "Tool 1 completed"

def tool2():
    time.sleep(1.0)
    return "Tool 2 completed"

def tool_with_error():
    time.sleep(0.3)
    raise ValueError("Simulated error in tool execution")

def random_tool():
    delay = random.uniform(0.1, 2.0)
    time.sleep(delay)
    return f"Random tool completed after {delay:.2f}s"

# Example 1: Parallel execution
print("Example 1: Parallel execution")
tools_parallel = [tool1, tool2]
start_time = time.time()
parallel_results = tool_chainer(tools_parallel, parallel=True)
parallel_duration = time.time() - start_time
print(f"Parallel execution completed in {parallel_duration:.2f} seconds")
print(f"Results: {parallel_results}")

# Example 2: Sequential execution
print("\nExample 2: Sequential execution")
tools_sequential = [tool1, tool2]
start_time = time.time()
sequential_results = tool_chainer(tools_sequential, parallel=False)
sequential_duration = time.time() - start_time
print(f"Sequential execution completed in {sequential_duration:.2f} seconds")
print(f"Results: {sequential_results}")

# Example 3: Error handling
print("\nExample 3: Error handling")
tools_mixed = [tool1, tool_with_error, tool2]
mixed_results = tool_chainer(tools_mixed, parallel=True)
print(f"Mixed execution results: {mixed_results}")

# Example 4: Performance comparison with random tools
print("\nExample 4: Performance comparison")
random_tools = [random_tool for _ in range(3)]

start_time = time.time()
random_parallel_results = tool_chainer(random_tools, parallel=True)
random_parallel_duration = time.time() - start_time

start_time = time.time()
random_sequential_results = tool_chainer(random_tools, parallel=False)
random_sequential_duration = time.time() - start_time

print(f"Random parallel execution: {random_parallel_duration:.2f}s")
print(f"Random sequential execution: {random_sequential_duration:.2f}s")
print(f"Speed improvement: {random_sequential_duration/random_parallel_duration:.2f}x")

print("\nTool Chainer examples completed successfully!")
print("Note: Parallel execution is most beneficial for I/O-bound operations")
