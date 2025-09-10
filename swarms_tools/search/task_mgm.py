"""
A structure for agent collaboration to be organized in a schema and tracking progress of task completion.
Primarily for Sequential Multiagentic Systems

Based on manus-taskplan.md structure with phase-based organization and continuous task completion tracking.

Args:
- tasks: tasks finalized to be completed with status tracking
- phases: bigger groups of tasks needed to be completed
- request (refined or not to make more detailed)
- completion tracking: continuous updates as agents complete tasks

EXAMPLE -
if __name__ == "__main__":
    user_request = "Develop a web scraper for collecting news articles"
    phase_name = "Development Phase"
    agent_roles = ["Research Agent", "Design Agent", "Implementation Agent", "QA Agent"]
    plan = plan_phase_for_task(task_goal, phase_name, agent_roles)
    print(plan.json(indent=2))
"""

import os
import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class Task(BaseModel):
    id: str = Field(..., description="Unique identifier for the task")
    description: str = Field(..., description="A detailed description of the task")
    agent: str = Field(..., description="The agent or role responsible for this task")
    completed: bool = Field(default=False, description="Whether the task is completed")
    
    def display_with_checkbox(self) -> str:
        """
        Return the task description with checkbox indicator and agent info.
        The agent is always included in a machine-readable form for easy retrieval.
        """
        checkbox = "[X]" if self.completed else "[ ]"
        return f"{checkbox} {self.description} ##AGENT:{self.agent if self.agent else 'None'}##"


class Phase(BaseModel):
    id: str = Field(..., description="Unique identifier for the phase")
    phase_name: str = Field(..., description="The name of the phase")
    objective: str = Field(..., description="The main objective of this phase")
    tasks: List[Task] = Field(..., description="A list of tasks to be completed in this phase")
    is_active: bool = Field(default=False, description="Whether this phase is currently active")
    
    def display_tasks(self) -> List[str]:
        """Return all tasks with checkbox indicators and agent info"""
        return [task.display_with_checkbox() for task in self.tasks]


class TaskPlan(BaseModel):
    project_name: str = Field(..., description="Name of the overall project")
    phases: List[Phase] = Field(..., description="List of phases in the project")
    overall_completed: bool = Field(default=False, description="Whether the entire project is completed")


class TaskManager:
    """Manager class for handling task completion updates and coordination"""
    
    def __init__(self, task_plan: TaskPlan):
        self.task_plan = task_plan
        self.task_index: Dict[str, tuple[int, int]] = {}  # task_id -> (phase_idx, task_idx)
        self._build_index()
    
    def _build_index(self):
        """Build index for quick task lookup"""
        for phase_idx, phase in enumerate(self.task_plan.phases):
            for task_idx, task in enumerate(phase.tasks):
                self.task_index[task.id] = (phase_idx, task_idx)
    
    def update_task_completion(self, task_id: str, completed: bool, agent: Optional[str] = None) -> bool:
        """
        Update the completion status of a task.
        
        Args:
            task_id: The ID of the task to update
            completed: New completion status for the task
            agent: Agent performing the update (optional)
            
        Returns:
            bool: True if update was successful
        """
        if task_id not in self.task_index:
            return False
            
        phase_idx, task_idx = self.task_index[task_id]
        task = self.task_plan.phases[phase_idx].tasks[task_idx]
        
        # Update task completion
        task.completed = completed
            
        # Check if phase is complete
        self._check_phase_completion(phase_idx)
        
        # Check if project is complete
        self._check_project_completion()
        
        return True
    
    def _check_phase_completion(self, phase_idx: int):
        """Check if a phase is complete and update accordingly"""
        phase = self.task_plan.phases[phase_idx]
        all_tasks_completed = all(task.completed for task in phase.tasks)
        
        if all_tasks_completed:
            # Activate next phase if available
            if phase_idx + 1 < len(self.task_plan.phases):
                self.task_plan.phases[phase_idx + 1].is_active = True
    
    def _check_project_completion(self):
        """Check if the entire project is complete"""
        all_phases_completed = all(
            all(task.completed for task in phase.tasks)
            for phase in self.task_plan.phases
        )
        
        self.task_plan.overall_completed = all_phases_completed
    
    def get_next_available_task(self, agent: str) -> Optional[Task]:
        """Get the next available task for a specific agent"""
        for phase in self.task_plan.phases:
            if not phase.is_active:
                continue
                
            for task in phase.tasks:
                if task.agent == agent and not task.completed:
                    return task
        return None
    
    def get_completion_percentage(self) -> float:
        """Get overall project completion percentage"""
        total_tasks = sum(len(phase.tasks) for phase in self.task_plan.phases)
        if total_tasks == 0:
            return 100.0
            
        completed_tasks = sum(
            sum(1 for task in phase.tasks if task.completed)
            for phase in self.task_plan.phases
        )
        
        return (completed_tasks / total_tasks) * 100
    
    def display_project_status(self) -> str:
        """Return a formatted string showing the current project status with checkboxes and agent info"""
        output = f"## {self.task_plan.project_name}\n\n"
        
        for phase in self.task_plan.phases:
            output += f"## {phase.phase_name}\n"
            for task in phase.tasks:
                output += f"{task.display_with_checkbox()}\n"
            output += "\n"
        
        completion_pct = self.get_completion_percentage()
        output += f"**Overall Completion: {completion_pct:.1f}%**\n"
        
        return output


def update_task_completion(task_plan: TaskPlan, task_id: str, completed: bool, agent: Optional[str] = None) -> Dict[str, Any]:
    """
    Tool function for updating task completion status.
    This can be called by agents when they complete tasks.

    Args:
        task_plan: The current task plan
        task_id: ID of the task to update
        completed: New completion status for the task
        agent: Agent performing the update
        
    Returns:
        Dict containing update result and current project status
    """
    
    print(f"   Updating task {task_id} to {'completed' if completed else 'incomplete'}")
    
    manager = TaskManager(task_plan)
    success = manager.update_task_completion(task_id, completed, agent)
    
    if success:
        print("   Task updated successfully!")
    else:
        print("   Failed to update task")
        return {
            "success": False,
            "task_id": task_id,
            "message": "Failed to update task"
        }

    # Prepare the todo.md content
    todo_lines = []
    todo_lines.append(f"# {task_plan.project_name}")
    todo_lines.append("")  # Empty line after title
    
    for phase in task_plan.phases:
        todo_lines.append(f"## {phase.phase_name}")
        for task in phase.tasks:
            todo_lines.append(task.display_with_checkbox())            
        todo_lines.append("")  # Blank line after each phase

    completion_pct = manager.get_completion_percentage()
    todo_lines.append(f"**Overall Completion: {completion_pct:.1f}%**")
    todo_lines.append("")  # Final empty line

    # Write to todo.md in the current working directory
    todo_md_path = os.path.join(os.getcwd(), "todo.md")
    
    try:
        with open(todo_md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(todo_lines))
        print(f"   todo.md updated at: {todo_md_path}")
        
        # Show a preview of the file
        print("\n   todo.md preview:")
        print("=" * 50)
        for i, line in enumerate(todo_lines[:10]):  # Show first 10 lines
            print(line)
        if len(todo_lines) > 10:
            print("...")
        print("=" * 50)
        
    except Exception as e:
        print(f"   Error writing todo.md: {e}")
        todo_md_path = ""

    return {
        "success": success,
        "task_id": task_id,
        "completed": completed if success else None,
        "completion_percentage": completion_pct,
        "project_completed": task_plan.overall_completed,
        "message": f"Task {task_id} {'marked as completed' if completed else 'marked as incomplete'}",
        "todo_md_path": todo_md_path
    }




#Actual connection from PM agent -> task_mgm tool
#ONLY DOES PHASE BY PHASE (e.g. if 6 phases, function will have to be called 6 times)
def task_planner(
    project_name: str,
    phase_dicts: list[dict]
) -> TaskPlan:
    """
    Converts a list of phase dictionaries (each representing a phase and its subtasks)
    into a TaskPlan object with proper Phase and Task objects.

    Args:
        project_name (str): The name of the overall project.
        phase_dicts (list[dict]): List of dictionaries, each representing a phase.
            Each phase dict should have:
                - "phase_name": str
                - "objective": str
                - "tasks": list of dicts, each with:
                    - "description": str
                    - "agent": str

    Returns:
        TaskPlan: A TaskPlan object containing all phases and tasks.
    """
    phases = []
    for phase_dict in phase_dicts:
        phase_name = phase_dict.get("phase_name", "Unnamed Phase")
        objective = phase_dict.get("objective", "")
        tasks_data = phase_dict.get("tasks", [])
        tasks = []
        for task_data in tasks_data:
            task = Task(
                id=str(uuid.uuid4()),
                description=task_data.get("description", ""),
                agent=task_data.get("agent", "Unassigned"),
                completed=task_data.get("completed", False),
            )
            tasks.append(task)
        phase = Phase(
            id=str(uuid.uuid4()),
            phase_name=phase_name,
            objective=objective,
            tasks=tasks
        )
        phases.append(phase)
    return TaskPlan(
        project_name=project_name,
        phases=phases,
        overall_completed=False
    )


def generate_todo_md(task_plan: TaskPlan, filename: str = "todo.md") -> str:
    """
    Generate and write a todo.md file for the given task plan.
    
    Args:
        task_plan: The TaskPlan object to generate todo.md for
        filename: Name of the file to create (default: "todo.md")
        
    Returns:
        str: Path to the created file
    """
    
    manager = TaskManager(task_plan)
    
    # Prepare the todo.md content
    todo_lines = []
    todo_lines.append(f"# {task_plan.project_name}")
    todo_lines.append("")  # Empty line after title
    
    for phase in task_plan.phases:
        todo_lines.append(f"## {phase.phase_name}")
        for task in phase.tasks:
            todo_lines.append(task.display_with_checkbox())
        todo_lines.append("")  # Blank line after each phase

    completion_pct = manager.get_completion_percentage()
    todo_lines.append(f"**Overall Completion: {completion_pct:.1f}%**")
    todo_lines.append("")  # Final empty line

    # Write to file in the current working directory
    todo_md_path = os.path.join(os.getcwd(), filename)
    
    try:
        with open(todo_md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(todo_lines))
        print(f"   todo.md created successfully at: {todo_md_path}")
        print(f"todo.md found at: {todo_md_path}")
        return todo_md_path
    except Exception as e:
        print(f"   Error creating todo.md: {e}")
        print(f"todo.md NOT found at: {todo_md_path}")
        return ""


def task_planner_with_todo(
    project_name: str,
    phase_dicts: list[dict],
    create_todo: bool = True
) -> TaskPlan:
    """
    Enhanced version of task_planner that automatically creates todo.md file.
    
    Args:
        project_name (str): The name of the overall project.
        phase_dicts (list[dict]): List of dictionaries, each representing a phase.
        create_todo (bool): Whether to create todo.md file automatically
        
    Returns:
        TaskPlan: A TaskPlan object containing all phases and tasks.
    """
    task_plan = task_planner(project_name, phase_dicts)
    
    if create_todo:
        generate_todo_md(task_plan)
    
    return task_plan


def update_task_completion_with_logging(
    task_plan: TaskPlan, 
    task_id: str, 
    completed: bool, 
    agent: Optional[str] = None
) -> Dict[str, Any]:
    """
    Enhanced version of update_task_completion with better logging and error handling.
    
    Args:
        task_plan: The current task plan
        task_id: ID of the task to update
        completed: New completion status for the task
        agent: Agent performing the update
        
    Returns:
        Dict containing update result and current project status
    """
    
    print(f"   Updating task {task_id} to {'completed' if completed else 'incomplete'}")
    
    manager = TaskManager(task_plan)
    success = manager.update_task_completion(task_id, completed, agent)
    
    if success:
        print("   Task updated successfully!")
    else:
        print("   Failed to update task 1")
        return {
            "success": False,
            "task_id": task_id,
            "message": "Failed to update task 1"
        }

    # Prepare the todo.md content
    todo_lines = []
    todo_lines.append(f"# {task_plan.project_name}")
    todo_lines.append("")  # Empty line after title
    
    for phase in task_plan.phases:
        todo_lines.append(f"## {phase.phase_name}")
        for task in phase.tasks:
            todo_lines.append(task.display_with_checkbox())
        todo_lines.append("")  # Blank line after each phase

    completion_pct = manager.get_completion_percentage()
    todo_lines.append(f"**Overall Completion: {completion_pct:.1f}%**")
    todo_lines.append("")  # Final empty line

    # Write to todo.md in the current working directory
    todo_md_path = os.path.join(os.getcwd(), "todo.md")
    
    try:
        with open(todo_md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(todo_lines))
        print(f"todo.md updated at: {todo_md_path}")
        
        # Show a preview of the file
        print("\ntodo.md preview:")
        print("=" * 50)
        for i, line in enumerate(todo_lines[:10]):  # Show first 10 lines
            print(line)
        if len(todo_lines) > 10:
            print("...")
        print("=" * 50)
        
    except Exception as e:
        print(f"Error writing todo.md: {e}")
        todo_md_path = ""

    return {
        "success": success,
        "task_id": task_id,
        "completed": completed if success else None,
        "completion_percentage": completion_pct,
        "project_completed": task_plan.overall_completed,
        "message": f"Task {task_id} {'marked as completed' if completed else 'marked as incomplete'}",
        "todo_md_path": todo_md_path
    }