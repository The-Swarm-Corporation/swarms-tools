"""
Makes sure that all tasks are marked with a [X] (or completed) AND begins running next task of next phase.

"""

import os
from typing import Dict, Any
from swarms_tools.search.run_task import run_task_without_timeout
from swarms_tools.search.end_task import end_task
import re

def run_phase_tasks_from_todo(
    todo_md_path: str,
    phase_name: str,
    AGENTS: Dict[str, Any]
) -> str:
    """
    Runs all incomplete tasks in the specified phase from the todo.md file, marking each as completed after execution.
    For each task, extracts the agent name from the task description (format: ##AGENT:AgentName##) and uses the 
    corresponding agent object from the AGENTS dictionary to execute the task.

    Args:
        todo_md_path: Full path to the todo.md file.
        phase_name: Name of the phase to run tasks for.
        AGENTS: Dictionary mapping agent names to agent objects.

    Returns:
        String stating what tasks have been run.
    """

    def extract_task_info_from_line(line: str):
        """
        Extracts the task description and agent name from a todo.md task line.
        Returns (task_description, agent_name, task_id)
        """
        agent_match = re.search(r"##AGENT:([A-Za-z0-9_]+)##", line)
        agent_name = agent_match.group(1) if agent_match else None

        id_match = re.search(r"##ID:([a-f0-9\-]+)##", line)
        task_id = id_match.group(1) if id_match else None

        desc_match = re.match(
            r"\[\s?\]\s*(.*?)(?:\s+##ID:.*?##)?(?:\s+##AGENT:.*?##)?$",
            line.strip()
        )
        task_description = desc_match.group(1).strip() if desc_match else line.strip()
        return task_description, agent_name, task_id

    if not os.path.exists(todo_md_path):
        raise FileNotFoundError(f"todo.md not found at {todo_md_path}")

    with open(todo_md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    phase_header = f"## {phase_name}"
    phase_start = None
    phase_end = None
    for idx, line in enumerate(lines):
        if line.strip() == phase_header:
            phase_start = idx
            break
    if phase_start is None:
        raise ValueError(f"Phase '{phase_name}' not found in todo.md")

    for idx in range(phase_start + 1, len(lines)):
        if lines[idx].strip().startswith("## ") and idx > phase_start:
            phase_end = idx
            break
    if phase_end is None:
        phase_end = len(lines)

    task_line_tuples = []
    for i in range(phase_start + 1, phase_end):
        line = lines[i]
        if re.match(r"\[\s?\]|\[X\]", line.strip()):
            task_line_tuples.append((i, line.rstrip("\n")))

    if not task_line_tuples:
        raise ValueError(f"No tasks found for phase '{phase_name}'")

    run_task_descriptions = []

    for line_number, task_line in task_line_tuples:
        if re.match(r"\[\s\]", task_line.strip()):
            task_description, agent_name, task_id = extract_task_info_from_line(task_line)
            if not agent_name or agent_name not in AGENTS:
                raise ValueError(f"Agent '{agent_name}' not found for task on line {line_number+1}")

            agent_obj = AGENTS[agent_name]

            print(f"Running task on line {line_number+1}: '{task_description}' with agent '{agent_name}'")

            result = run_task_without_timeout(
                agent=agent_obj,
                task_description=task_description,
                args=(),
                kwargs={},
            )

            print(f"\n--- Result for task '{task_description}' (Agent: {agent_name}) ---")
            print(result)

            run_task_descriptions.append(
                f"Task: '{task_description}' (Agent: {agent_name}) - completed.\nResult:\n{result}"
            )

            end_task(line_number)

    if not run_task_descriptions:
        return f"No incomplete tasks found for phase '{phase_name}'."
    else:
        return (
            f"Tasks run for phase '{phase_name}':\n\n" +
            "\n\n".join(run_task_descriptions)
        )
