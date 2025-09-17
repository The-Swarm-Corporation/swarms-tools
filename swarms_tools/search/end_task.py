"""
Ends the task at hand by marking off its task on todo.md using a line number.
Will be run by the run_task tool when task is run and time is completed.

This tool provides:
- Task completion marking in todo.md with [X]
- Integration with task management system
- Automatic status updates and logging

Args taken:
- line_number: the line number (0-based) of the task to mark as completed in todo.md
- agent: optional agent name performing the completion (defaults to "TaskRunner")
"""

import os
import sys
import re

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

def end_task(line_number: int) -> str:
    """
    Marks the task as completed in the todo.md file by replacing the [ ] with [X] for the given line number.

    Args:
        line_number: The 0-based line number of the task to mark as completed in todo.md
        agent: Name of the agent performing the completion (not used here, but kept for compatibility)

    Returns:
        String containing completion results and metadata
    """

    todo_md_path = os.path.join(os.getcwd(), "todo.md")
    if not os.path.exists(todo_md_path):
        return (
            f"Task completion failed.\n"
            f"Line number: {line_number}\n"
            f"Error: todo.md not found at {todo_md_path}\n"
            f"todo.md path: {todo_md_path}\n"
        )

    with open(todo_md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if line_number < 0 or line_number >= len(lines):
        return (
            f"Task completion failed.\n"
            f"Line number: {line_number}\n"
            f"Error: Line number out of range in todo.md\n"
            f"todo.md path: {todo_md_path}\n"
        )

    line = lines[line_number]
    new_line = re.sub(r"^\[\s\]", "[X]", line)
    if new_line != line:
        lines[line_number] = new_line
        found = True
    elif line.startswith("[X]"):
        found = True
    else:
        found = False

    if not found:
        return (
            f"Task completion failed.\n"
            f"Line number: {line_number}\n"
            f"Error: Task line does not start with [ ] or [X]\n"
            f"todo.md path: {todo_md_path}\n"
        )

    with open(todo_md_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    num_completed = 0
    num_total = 0
    for line_content in lines:
        if re.match(r"^\s*\[X\]", line_content):
            num_completed += 1
            num_total += 1
        elif re.match(r"^\s*\[\s\]", line_content):
            num_total += 1
    completion_pct = (num_completed / num_total) * 100 if num_total > 0 else 100.0

    output = []
    output.append(f"Task at line {line_number} marked as completed in todo.md")
    output.append(f"   Completion percentage: {completion_pct:.1f}%")
    output.append(f"   (Marked down in: {todo_md_path})")

    output.append("=" * 50)
    summary = (
        f"Line number: {line_number}\n"
        f"Success: {True}\n"
        f"Completion Percentage: {completion_pct:.1f}%\n"
        f"todo.md path: {todo_md_path}\n"
    )
    output.append(summary)
    return "\n".join(output)