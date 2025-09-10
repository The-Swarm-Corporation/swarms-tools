import os
from swarms import Agent
from swarms_tools.search.task_mgm import (
    task_planner_with_todo,
)
from swarms_tools.search.advance_phase import run_phase_tasks_from_todo


# --- Define specialized agents using swarms.Agent ---
market_researcher = Agent(
    agent_name="MarketResearcher",
    model_name = "gpt-4o-mini",
    agent_description="Expert in market research for local businesses."
)

content_creator = Agent(
    agent_name="ContentCreator",
    model_name="gpt-4o-mini",
    agent_description="Creative content and campaign planner for food and beverage brands."
)
ad_specialist = Agent(
    agent_name="AdSpecialist",
    model_name="gpt-4o-mini",
    agent_description="Digital advertising and analytics specialist."
)

AGENTS = {
    "MarketResearcher": market_researcher,
    "ContentCreator": content_creator,
    "AdSpecialist": ad_specialist
}

# --- Step 1: Use ProjectManager agent to create the phases and tasks ---
project_name = "SF Ice Cream Shop 40% Growth Plan"

# Directly use the fallback plan
phase_dicts = [
    {
        "phase_name": "Market Research",
        "objective": "Understand the local market, competitors, and customer preferences.",
        "tasks": [
            {"description": "Analyze local competitors' marketing strategies.", "agent": "MarketResearcher"},
            {"description": "Survey local customers for flavor and service preferences.", "agent": "MarketResearcher"},
            {"description": "Identify peak sales periods and slow days.", "agent": "MarketResearcher"},
        ],
    },
    {
        "phase_name": "Content & Promotion Planning",
        "objective": "Develop creative content and promotional ideas to attract new customers.",
        "tasks": [
            {"description": "Draft a 5-month content calendar for social media.", "agent": "ContentCreator"},
            {"description": "Design a 'Summer Flavors' launch campaign.", "agent": "ContentCreator"},
            {"description": "Plan a local event or collaboration with SF businesses.", "agent": "ContentCreator"},
        ],
    },
    {
        "phase_name": "Advertising & Execution",
        "objective": "Launch ads, track results, and optimize for growth.",
        "tasks": [
            {"description": "Set up targeted Facebook and Instagram ads.", "agent": "AdSpecialist"},
            {"description": "Monitor ad performance and adjust budget weekly.", "agent": "AdSpecialist"},
            {"description": "Report on sales growth and campaign ROI monthly.", "agent": "AdSpecialist"},
        ],
    },
]

# --- Step 2: Create the TaskPlan and todo.md ---
task_plan = task_planner_with_todo(project_name, phase_dicts, create_todo=True)
todo_md_path = os.path.join(os.getcwd(), "todo.md")

# --- Step 3: Run each phase, using the agent attached to each task ---
for phase in task_plan.phases:
    print(f"\n=== Running Phase: {phase.phase_name} ===")
    phase_results = []

    # If you want to pass the agent object, you can do so here; otherwise, just pass the agent name
    result = run_phase_tasks_from_todo(
        todo_md_path=todo_md_path,
        phase_name=phase.phase_name,
        AGENTS=AGENTS
    )

    phase_results.extend(result)

    # Print results for each task
    for i, result in enumerate(phase_results):
        print(f"Task {i+1} result: {result}")
    # Reload the task plan to reflect updates by reading todo.md directly
    with open(todo_md_path, "r", encoding="utf-8") as f:
        todo_md_content = f.read()
    print(f"Updated todo.md content after phase '{phase.phase_name}':\n")
    print(todo_md_content)
    completed_tasks = sum(1 for t in phase.tasks if t.completed)
    total_tasks = len(phase.tasks)
    print(f"Phase '{phase.phase_name}' completion: {completed_tasks}/{total_tasks} tasks completed.")

# --- Step 4: Final status ---
print("\nAll phases complete. Final todo.md preview:\n")
with open(todo_md_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines[:30]:
        print(line.rstrip())
    if len(lines) > 30:
        print("... (truncated) ...")

print("\nDemo complete: All phases and tasks have been run and logged using the multiagent system tools and swarms.Agent.")
