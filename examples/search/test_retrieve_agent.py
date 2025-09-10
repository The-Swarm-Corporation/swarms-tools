from swarms_tools.search.advance_phase import load_task_plan_from_todo
import re

def extract_agent_from_description(description):
    """
    Given a task description line from todo.md, extract the agent name if present in the format ##AGENT:AgentName##.
    Returns the agent name as a string, or None if not found.
    """
    match = re.search(r"##AGENT:([A-Za-z0-9_]+)##", description)
    if match:
        return match.group(1)
    return None

def get_task_and_agent_by_indices(todo_md_path, phase_index, task_index):
    """
    Given a todo.md file, a phase number, and a task number, retrieve and print the task and its agent.
    Indices are zero-based.

    This version extracts the agent from the task description if present in the format ##AGENT:AgentName##.
    """
    task_plan = load_task_plan_from_todo(todo_md_path)
    try:
        phase = task_plan.phases[phase_index]
        task = phase.tasks[task_index]
        # The agent may be embedded in the description as ##AGENT:AgentName##
        agent = extract_agent_from_description(task.description)
        print(f"Phase {phase_index} ('{phase.phase_name}') Task {task_index}:")
        print(f"  Task Description: {task.description}")
        print(f"  Agent: {agent if agent else '(not found)'}")
        return task, agent
    except IndexError:
        print(f"Invalid phase_index ({phase_index}) or task_index ({task_index}).")
        return None, None

if __name__ == "__main__":
    todo_md_path = "todo.md"
    # Example: retrieve the 2nd phase (index 1), 3rd task (index 2)
    phase_index = 1
    task_index = 2
    get_task_and_agent_by_indices(todo_md_path, phase_index, task_index)
