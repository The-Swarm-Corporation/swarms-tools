"""
Makes sure that all tasks are marked with a [X] (or completed) AND begins running next task of next phase.

"""

import os
from typing import List, Dict, Any
from swarms_tools.search.run_task import run_task_without_timeout  # Import here to avoid circular import
from swarms_tools.search.end_task import end_task
from swarms_tools.search.task_mgm import TaskPlan, Phase, Task
import re
import uuid

def load_task_plan_from_todo(todo_md_path: str):
    """
    Loads a TaskPlan object from a todo.md file by parsing its Markdown content.
    This reconstructs the TaskPlan (project name, phases, tasks, and completion status)
    from the todo.md file, similar to how update_task_completion_with_logging writes it.
    """


    if not os.path.exists(todo_md_path):
        raise FileNotFoundError(f"todo.md not found at {todo_md_path}")

    with open(todo_md_path, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    # Parse project name (first line, starts with "# ")
    if not lines or not lines[0].startswith("# "):
        raise ValueError("todo.md does not start with a project name header")
    project_name = lines[0][2:].strip()

    phases = []
    phase_name = None
    phase_tasks = []
    objective = ""  # Not present in todo.md, so leave blank
    phase_id = None

    def flush_phase():
        nonlocal phase_name, phase_tasks, phase_id
        if phase_name is not None:
            phases.append(
                Phase(
                    id=phase_id or str(uuid.uuid4()),
                    phase_name=phase_name,
                    objective=objective,
                    tasks=phase_tasks,
                    is_active=False,
                )
            )
        phase_name = None
        phase_tasks = []
        phase_id = None

    for line in lines[1:]:
        if line.startswith("## "):
            flush_phase()
            phase_name = line[3:].strip()
            phase_id = str(uuid.uuid4())
        elif line.startswith("[ ]") or line.startswith("[X]"):
            # Task line
            completed = line.startswith("[X]")
            # Remove checkbox and leading space
            desc = line[3:].strip()
            # Try to extract agent from description if present (not in todo.md, so leave blank)
            agent = ""
            task_id = str(uuid.uuid4())
            phase_tasks.append(
                Task(
                    id=task_id,
                    description=desc,
                    agent=agent,
                    completed=completed,
                )
            )
        elif line.startswith("**Overall Completion:"):
            # End of tasks
            flush_phase()
            break
        # else: skip blank lines and other content

    # If file ends without "Overall Completion", flush last phase
    if phase_name and phase_tasks:
        flush_phase()

    # Determine overall_completed from completion percentage
    overall_completed = False
    for line in lines:
        m = re.match(r"\*\*Overall Completion: ([\d\.]+)%\*\*", line)
        if m:
            pct = float(m.group(1))
            overall_completed = pct >= 100.0
            break

    return TaskPlan(
        project_name=project_name,
        phases=phases,
        overall_completed=overall_completed,
    )

def run_phase_tasks_from_todo(
    todo_md_path: str,
    phase_name: str,
    AGENTS: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Runs all incomplete tasks in the specified phase from the todo.md file, marking each as completed after execution.
    For each task, extracts the agent name from the task description (format: ##AGENT:AgentName##) and uses the 
    corresponding agent object from the AGENTS dictionary to execute the task.

    Args:
        todo_md_path: Full path to the todo.md file.
        phase_name: Name of the phase to run tasks for.
        agent: Default agent name to use if no agent is specified in task description.
        AGENTS: Dictionary mapping agent names to agent objects.

    Returns:
        List of result dictionaries for each task.
    """
    import re
    
    def extract_agent_from_description(description: str) -> str:
        """
        Extract the agent name from a task description using the format ##AGENT:AgentName##.
        Returns the agent name as a string, or None if not found.
        """
        match = re.search(r"##AGENT:([A-Za-z0-9_]+)##", description)
        if match:
            return match.group(1)
        return None
    
    def get_task_and_agent_by_phase(todo_md_path: str, phase_name: str, task_index: int):
        """
        Get a specific task and its agent from a phase by index.
        Similar to test_retrieve_agent.py but focused on a specific phase.
        """
        task_plan = load_task_plan_from_todo(todo_md_path)
        try:
            phase = next((p for p in task_plan.phases if p.phase_name == phase_name), None)
            if phase is None:
                raise ValueError(f"Phase '{phase_name}' not found")
            
            task = phase.tasks[task_index]
            agent_name = extract_agent_from_description(task.description)
            return task, agent_name
        except IndexError:
            raise ValueError(f"Task index {task_index} not found in phase '{phase_name}'")

    if not os.path.exists(todo_md_path):
        raise FileNotFoundError(f"todo.md not found at {todo_md_path}")

    # Get all tasks for the specified phase
    # Load the task plan from the todo.md file
    task_plan = load_task_plan_from_todo(todo_md_path)
    phase = next((p for p in task_plan.phases if p.phase_name == phase_name), None)
    phase_tasks = phase.tasks if phase else []
    if not phase_tasks:
        raise ValueError(f"No tasks found for phase '{phase_name}'")

    results = []

    for task_index, _ in enumerate(phase_tasks):
        # Use the helper to get the up-to-date task and agent name
        task, task_agent_name = get_task_and_agent_by_phase(todo_md_path, phase_name, task_index)
        if not task.completed:
            agent_obj = AGENTS[task_agent_name]

            print(f"Running task '{task.description}' with agent '{task_agent_name}'")

            # Run the task
            result = run_task_without_timeout(
                agent=agent_obj,
                task_description=getattr(task, "description", ""),
                args=getattr(task, "args", ()),
                kwargs=getattr(task, "kwargs", {}),
            )
            results.append(result)

            task_id = str(uuid.uuid4())

            # Mark the task as completed in todo.md
            end_task(task_id, task_plan, agent=task_agent_name)
    
    return results
