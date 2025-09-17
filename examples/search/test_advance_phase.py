""" 
This is a test for task_mgm, end_task, run_task, and advance_phase.
"""

import os
from swarms import Agent
from swarms_tools.search.task_mgm import task_planner_with_todo
from swarms_tools.search.advance_phase import run_phase_tasks_from_todo

def main():
    market_researcher = Agent(
        agent_name="MarketResearcher",
        model_name="gpt-4o-mini",
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

    project_name = "SF Ice Cream Shop 40% Growth Plan"

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

    task_planner_with_todo(project_name, phase_dicts, create_todo=True)
    
    todo_md_path = os.path.join(os.getcwd(), "todo.md")

    phase_names = []
    with open(todo_md_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("## "):
                phase_name = line[3:].strip()
                if phase_name != project_name:
                    phase_names.append(phase_name)

    for phase_name in phase_names:
        print(f"\n=== Running Phase: {phase_name} ===")
        phase_result = run_phase_tasks_from_todo(
            todo_md_path=todo_md_path,
            phase_name=phase_name,
            AGENTS=AGENTS
        )

        print("Phase execution completed.")
        print(f"Phase result:\n{phase_result}")

        completed_tasks = 0
        total_tasks = 0
        in_phase = False
        with open(todo_md_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("## "):
                    current_phase = line[3:].strip()
                    if current_phase == phase_name:
                        in_phase = True
                        continue
                    elif in_phase:
                        break
                if in_phase:
                    if line.startswith("[X]"):
                        completed_tasks += 1
                        total_tasks += 1
                    elif line.startswith("[ ]"):
                        total_tasks += 1
        if total_tasks > 0:
            print(f"Phase '{phase_name}' completion: {completed_tasks}/{total_tasks} tasks completed.")
        else:
            print(f"[DEBUG] Phase '{phase_name}' not found or has no tasks in todo.md.")

    print("\nAll phases complete. Final todo.md preview:\n")
    with open(todo_md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines[:30]:
            print(line.rstrip())
        if len(lines) > 30:
            print("... (truncated) ...")

    print("\nDemo complete: All phases and tasks have been run and logged using the multiagent system tools and swarms.Agent.")

if __name__ == "__main__":
    main()