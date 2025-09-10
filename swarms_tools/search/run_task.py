"""
Runs the task at hand, optionally using an agent, without a timeout constraint.
This tool provides integration with a multi-agent system, allowing a specified agent to execute the task.

Args taken:
- agent: The agent object OR agent name (string) to execute the task.
- task_description: The description or prompt for the agent to process
- args: Tuple of positional arguments to pass to the agent (optional)
- kwargs: Dictionary of keyword arguments to pass to the agent (optional)

Example usage:
    result = run_task_without_timeout(
        agent=agent_object,
        task_description="Research the latest trends in AI.",
    )
    # OR, if agent is a string name and AGENTS is available in global scope:
    result = run_task_without_timeout(
        agent="MarketResearcher",
        task_description="Research the latest trends in AI.",
        agents_dict=AGENTS
    )
"""

import time
from datetime import datetime
from typing import Any, Dict, Optional, Tuple

class TaskRunner:
    """
    A simple task runner for agent-based execution without timeout.
    """
    def __init__(
        self,
        time_start: Optional[datetime] = None,
    ):
        self.time_start = time_start or datetime.now()
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.execution_time: Optional[float] = None
        self.success = False
        self.error_message: Optional[str] = None

        print(f"   Scheduled start: {self.time_start}")

    def _wait_for_start_time(self) -> bool:
        """Wait until the scheduled start time if specified."""
        if self.time_start and datetime.now() < self.time_start:
            wait_seconds = (self.time_start - datetime.now()).total_seconds()
            print(f"   Waiting {wait_seconds:.1f} seconds until scheduled start time...")
            if wait_seconds > 0:
                time.sleep(wait_seconds)
        return True

    def run(
        self,
        agent: Any,
        task_description: str,
        args: Tuple = (),
        kwargs: Dict = {},
    ) -> Dict[str, Any]:
        """
        Execute the task using the provided agent.

        Args:
            agent: The agent object to execute the task.
            task_description: The description or prompt for the agent
            args: Positional arguments for the agent (optional)
            kwargs: Keyword arguments for the agent (optional)

        Returns:
            Dictionary containing execution results and metadata
        """
        print("=" * 60)

        if not self._wait_for_start_time():
            return self._create_failure_result("Failed to wait for start time")

        self.start_time = datetime.now()
        result = None

        try:
            agent_obj = agent

            # Prefer agent_obj(task_description, *args, **kwargs) if agent_obj is callable
            if callable(agent_obj):
                result = agent_obj(task_description, *args, **kwargs)
            # Otherwise, try agent_obj.run(task_description, *args, **kwargs)
            elif hasattr(agent_obj, "run") and callable(getattr(agent_obj, "run")):
                result = agent_obj.run(task_description, *args, **kwargs)
            else:
                raise ValueError("Agent must be callable or have a 'run' method.")

            self.success = True

        except Exception as e:
            self.success = False
            self.error_message = f"Agent execution error: {str(e)}"
        finally:
            self.end_time = datetime.now()
            self.execution_time = (self.end_time - self.start_time).total_seconds()

        return self._create_result(result if self.success else None)

    def _create_result(self, task_result: Any = None) -> Dict[str, Any]:
        """Create the result dictionary with execution metadata."""
        return {
            "success": self.success,
            "result": task_result,
            "execution_time": self.execution_time,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "error_message": self.error_message,
            "scheduled_start": self.time_start.isoformat() if self.time_start else None
        }

    def _create_failure_result(self, message: str) -> Dict[str, Any]:
        """Create a failure result dictionary."""
        self.success = False
        self.error_message = message
        return self._create_result()

def run_task_without_timeout(
    agent: Any,
    task_description: str,
    args: Tuple = (),
    kwargs: Dict = {},
    time_start: Optional[datetime] = None,
) -> Dict[str, Any]:
    """
    Run a task using the specified agent, without a timeout.

    Args:
        agent: The agent object to execute the task
        task_description: The description or prompt for the agent
        args: Positional arguments for the agent (optional)
        kwargs: Keyword arguments for the agent (optional)
        time_start: Scheduled start time (optional)

    Returns:
        Dictionary with execution results
    """
    runner = TaskRunner(
        time_start=time_start,
    )
    result = runner.run(agent, task_description, args, kwargs)
    return result