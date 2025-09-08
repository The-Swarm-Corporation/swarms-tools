"""
Ends the task at hand by marking off its task on todo.md using update_task_completion_with_logging.
Will be run by the run_task tool when task is run and time is completed.

This tool provides:
- Task completion marking in todo.md with [X]
- Integration with task management system
- Automatic status updates and logging

Args taken:
- task_id: unique identifier of the task to mark as completed
- task_plan: the TaskPlan object containing the task
- agent: optional agent name performing the completion (defaults to "TaskRunner")
"""

import os
import sys
from typing import Dict, Any
from swarms_tools.search.task_mgm import TaskPlan, update_task_completion_with_logging

# Add path to import task management
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

def end_task(task_id: str, task_plan: TaskPlan, agent: str = "TaskRunner") -> Dict[str, Any]:
    """
    Mark a task as completed in the todo.md file using its task_id.

    This function:
    1. Updates the task status to completed
    2. Updates the todo.md file with [X] marker for the specific task_id
    3. The todo.md file is located at:
        todo_md_path = os.path.join(os.getcwd(), "todo.md")

    Args:
        task_id: ID of the task to mark as completed
        task_plan: The TaskPlan object containing the task
        agent: Name of the agent performing the completion
        
    Returns:
        Dictionary containing completion results and metadata
    """

    print(f"\nEnding task with ID: {task_id}")
    print("=" * 50)

    # The location of the todo.md file
    todo_md_path = os.path.join(os.getcwd(), "todo.md")
    print(f"   The todo.md file will be updated at: {todo_md_path}")

    if not update_task_completion_with_logging:
        error_msg = "Task management module not available"
        print(f"Error: {error_msg}")
        return {
            "success": False,
            "task_id": task_id,
            "error": error_msg,
            "todo_md_path": todo_md_path
        }

    # Update the task completion status for the specific task_id
    try:
        print("   Marking task as completed...")
        result = update_task_completion_with_logging(
            task_plan=task_plan,
            task_id=task_id,
            completed=True,
            agent=agent
        )

        if result["success"]:
            print(f"Task with ID '{task_id}' marked as completed in todo.md")
            print(f"   Completion percentage: {result['completion_percentage']:.1f}%")
            print(f"   (Marked down in: {todo_md_path})")

            # Show the updated task status
            for phase in task_plan.phases:
                for task in phase.tasks:
                    if task.id == task_id:
                        print(f"   Task status: {task.display_with_checkbox()}")
                        break

        else:
            print(f"Failed to mark task with ID '{task_id}' as completed")
            print(f"   Error: {result.get('message', 'Unknown error')}")
            print(f"   (Attempted to mark down in: {todo_md_path})")

        print("=" * 50)
        # Always include the todo_md_path in the result for clarity
        result["todo_md_path"] = todo_md_path
        return result

    except Exception as e:
        error_msg = f"Error updating task completion: {str(e)}"
        print(f"Error: {error_msg}")
        print("=" * 50)

        return {
            "success": False,
            "task_id": task_id,
            "error": error_msg,
            "todo_md_path": todo_md_path
        }


# # Example Usage (mirroring test_todo_generation.py's example)
# if __name__ == "__main__":
#     # Example project and phases, similar to test_todo_generation.py
#     project_name = "Example Project"
#     phase_dicts = [
#         {
#             "phase_name": "Planning Phase",
#             "objective": "Define requirements and plan project",
#             "tasks": [
#                 {
#                     "description": "Research requirements",
#                     "agent": "Research Agent"
#                 },
#                 {
#                     "description": "Create project plan",
#                     "agent": "Project Manager"
#                 }
#             ]
#         },
#         {
#             "phase_name": "Development Phase",
#             "objective": "Implement and test the solution",
#             "tasks": [
#                 {
#                     "description": "Write code",
#                     "agent": "Developer Agent"
#                 },
#                 {
#                     "description": "Test implementation",
#                     "agent": "QA Agent"
#                 }
#             ]
#         }
#     ]

#     # Import the task planner and todo generator
#     from swarms_tools.search.task_mgm import task_planner_with_todo

#     # Create the TaskPlan and todo.md
#     task_plan = task_planner_with_todo(project_name, phase_dicts)

#     # Get the ID for the first task in Phase 1
#     first_task_id = task_plan.phases[0].tasks[1].id
#     sec_task_id = task_plan.phases[1].tasks[0].id

#     # Use end_task to mark Phase 1, Task 1 as completed
#     result = end_task(first_task_id, task_plan)
#     result = end_task(sec_task_id, task_plan)
#     print("\nend_task result:")
#     print(result)