from dotenv import load_dotenv
from browser_use import Agent, ChatOpenAI
import asyncio

load_dotenv()


def browser_agent(task: str, model_name: str = "gpt-4.1-mini"):
    """
    Executes a browser-based agent to perform a specified task using a language model.

    This function sets up and runs an asynchronous agent that utilizes a language model
    (default: "gpt-4.1-mini") to complete the provided task. The agent is executed in an
    asyncio event loop, and its output is printed to the console.

    Args:
        task (str):
            A description of the task for the agent to perform. This should be a clear,
            concise instruction or query that the agent can act upon using browser-based tools.
        model_name (str, optional):
            The name of the language model to use for the agent. Defaults to "gpt-4.1-mini".
            This parameter allows you to specify different models as needed.

    Returns:
        None. The function prints the agent's output to the console.

    Example:
        >>> browser_agent("Find the number of stars of the swarms")
        # Output will be printed to the console.

    Notes:
        - The function uses asyncio to run the agent asynchronously.
        - The agent's output is processed with `model_dump()` before being printed.
        - Requires the `Agent` and `ChatOpenAI` classes from the `browser_use` module.
        - Assumes that environment variables (such as API keys) are loaded via dotenv.
    """

    async def run_agent():
        """
        Asynchronously creates and runs the Agent to perform the specified task.

        Returns:
            The result of the agent's run method, which contains the output of the task.
        """
        agent = Agent(
            task=task,
            llm=ChatOpenAI(model=model_name),
        )
        return await agent.run()

    # Run the asynchronous agent and obtain the output.
    out = asyncio.run(run_agent())
    # Process the output with model_dump (for serialization or inspection).
    out.model_dump()
    # Print the final output to the console.
    print(out)


# if __name__ == "__main__":
#     # Example usage: instruct the agent to find the number of stars of the swarms.
#     browser_agent("Find the number of stars of the swarms")
