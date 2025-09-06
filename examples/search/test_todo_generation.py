"""
Test script to verify that todo.md generation is working properly.
"""

import sys
import os

# Add the parent directory to the path to import task_mgm
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from swarms_tools.search.task_mgm import task_planner_with_todo, generate_todo_md, update_task_completion_with_logging

def test_todo_generation():
    """Test that todo.md files are being created properly."""
    
    print(" Testing todo.md generation...")
    print(f"Current working directory: {os.getcwd()}")
    
    # Test data
    project_name = "Test Project"
    phase_dicts = [
        {
            "phase_name": "Planning Phase",
            "objective": "Plan the project",
            "tasks": [
                {
                    "description": "Research requirements",
                    "agent": "Research Agent"
                },
                {
                    "description": "Create project plan", 
                    "agent": "Planning Agent"
                }
            ]
        },
        {
            "phase_name": "Implementation Phase",
            "objective": "Implement the solution",
            "tasks": [
                {
                    "description": "Write code",
                    "agent": "Developer Agent"
                },
                {
                    "description": "Test implementation",
                    "agent": "QA Agent"
                }
            ]
        }
    ]
    
    print("\n Testing task_planner_with_todo()...")
    try:
        task_plan = task_planner_with_todo(project_name, phase_dicts)
        print("  task_planner_with_todo() completed")
        
        # Check if file exists
        todo_path = os.path.join(os.getcwd(), "todo.md")
        if os.path.exists(todo_path):
            print(f"todo.md found at: {todo_path}")
            with open(todo_path, 'r') as f:
                content = f.read()
                print("File content preview:")
                print(content[:200] + "..." if len(content) > 200 else content)
        else:
            print(f"todo.md NOT found at: {todo_path}")
            
    except Exception as e:
        print(f"  Error in task_planner_with_todo(): {e}")
    
    print("\n Testing generate_todo_md()...")
    try:
        task_plan = task_planner_with_todo(project_name, phase_dicts, create_todo=False)
        generate_todo_md(task_plan, "todo.md")
        
        # Check if file exists
        test_todo_path = os.path.join(os.getcwd(), "todo.md")
        if os.path.exists(test_todo_path):
            print(f"  todo.md found at: {test_todo_path}")
        else:
            print(f"  todo.md NOT found at: {test_todo_path}")
            
    except Exception as e:
        print(f"  Error in generate_todo_md(): {e}")
    
    print("\n Testing update_task_completion_with_logging()...")
    try:
        task_plan = task_planner_with_todo(project_name, phase_dicts, create_todo=False)
        if task_plan.phases and task_plan.phases[0].tasks:
            first_task_id = task_plan.phases[0].tasks[0].id
            result = update_task_completion_with_logging(task_plan, first_task_id, True)
            print(f"  Update result: {result['success']}")
            
            # Check if todo.md was updated
            todo_path = os.path.join(os.getcwd(), "todo.md")
            if os.path.exists(todo_path):
                print(f"  todo.md updated at: {todo_path}")
            else:
                print("  todo.md NOT found after update")
        
    except Exception as e:
        print(f"  Error in update_task_completion_with_logging(): {e}")
    
    print("\n Test completed!")
    print("Check your current directory for todo.md and todo.md files")

if __name__ == "__main__":
    test_todo_generation()
