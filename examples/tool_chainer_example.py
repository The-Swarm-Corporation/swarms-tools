# Example usage
from loguru import logger

from swarms_tools.structs import tool_chainer

if __name__ == "__main__":
    logger.add("tool_chainer.log", rotation="500 MB", level="INFO")

    # Example tools
    def tool1():
        return "Tool1 Result"

    def tool2():
        return "Tool2 Result"

    # def tool3():
    #     raise ValueError("Simulated error in Tool3")

    tools = [tool1, tool2]

    # Parallel execution
    parallel_results = tool_chainer(tools, parallel=True)
    print("Parallel Results:", parallel_results)

    # Sequential execution
    # sequential_results = tool_chainer(tools, parallel=False)
    # print("Sequential Results:", sequential_results)
