from typing import List, Dict, Any
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_detailed_plan(
    task_input: str,
    available_agents: List[str],
    model: str = "gpt-4-turbo"
) -> List[Dict[str, Any]]:
    """
    Uses an AI model to generate a highly detailed, specific, and executable plan for the given task.
    Each step is an object in the returned list.

    Args:
        task_input (str): The description of the task to plan for.
        available_agents (List[str]): List of all agents available in the swarm.
        model (str): The OpenAI model to use.

    Returns:
        List[Dict[str, Any]]: A list of step objects, each representing a step in the plan.
    """
    agents_str = "\n".join(f"- {agent}" for agent in available_agents)
    prompt = (
        "You are an expert multi-agent system orchestrator responsible for creating comprehensive execution plans for a team of specialized agents. "
        "Your role is to analyze complex tasks and break them down into a structured, sequential plan that can be distributed across multiple agents with different capabilities.\n\n"
        "Given the following task, create a detailed execution plan that:\n"
        "1. Identifies the optimal sequence of operations\n"
        "2. Determines which type of agent should handle each step\n"
        "3. Specifies clear inputs, outputs, and success criteria\n"
        "4. Accounts for dependencies and potential failure points\n"
        "5. Includes verification and quality control measures\n\n"
        "Available agent types include (but are not limited to):\n"
        f"{agents_str}\n\n"
        "Return the plan as a JSON array where each step contains:\n"
        "- task_number: Task identifier\n"
        "- description: Clear, specific description of what needs to be accomplished. Be REALLY specific on what agents will be used, where the agents will look for/work in, and an into-depth format of what it will be doing.\n"
        "- action_items: Detailed list of specific tasks to be performed (e.g. The code fetches and displays projects with title, description, and other details. To show the description below the title, I will modify the JSX to position the `<p>` element containing `project.description` immediately after the project title `<h3>`. This will ensure the description appears directly below each post's title while maintaining the existing layout. The next step is editing the rendering section accordingly.)\n"
        "- agent: The specific agent (by name) responsible for executing this step\n"
        f"Task: {task_input}\n\n"
        "Plan:"
    )
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.2,
    )
    # The model should return a JSON array as the content
    import json
    content = response.choices[0].message.content
    try:
        plan = json.loads(content)
        # If the plan is wrapped in a dict, extract the list
        if isinstance(plan, dict):
            # Try to find the first list value
            for v in plan.values():
                if isinstance(v, list):
                    return v
        elif isinstance(plan, list):
            return plan
    except Exception:
        # Fallback: return the raw content in a single step
        return [{"step_number": 1, "description": content, "action_items": []}]
    return []

def update_plan_with_input(
    plan: List[Dict[str, Any]],
    update_input: str,
    available_agents: List[str],
    model: str = "gpt-4-turbo"
) -> List[Dict[str, Any]]:
    """
    Uses an AI model to update the given plan based on new input.

    Args:
        plan (List[Dict[str, Any]]): The current plan as a list of step objects.
        update_input (str): The new input or change to consider (e.g., feedback, new requirements).
        available_agents (List[str]): List of all agents available in the swarm.
        model (str): The OpenAI model to use.

    Returns:
        List[Dict[str, Any]]: The updated plan as a list of step objects.
    """
    import json
    plan_json = json.dumps(plan, indent=2)
    agents_str = "\n".join(f"- {agent}" for agent in available_agents)
    prompt = (
        "You are an expert multi-agent system orchestrator responsible for creating comprehensive execution plans for a team of specialized agents. "
        "Your role is to analyze complex tasks and break them down into a structured, sequential plan that can be distributed across multiple agents with different capabilities.\n\n"
        "Given the following task, create a detailed execution plan that:\n"
        "1. Identifies the optimal sequence of operations\n"
        "2. Determines which type of agent should handle each step\n"
        "3. Specifies clear inputs, outputs, and success criteria\n"
        "4. Accounts for dependencies and potential failure points\n"
        "5. Includes verification and quality control measures\n\n"
        "Available agent types include (but are not limited to):\n"
        f"{agents_str}\n\n"
        "Return the plan as a JSON array where each step contains:\n"
        "- task_number: Task identifier\n"
        "- description: Clear, specific description of what needs to be accomplished. Be REALLY specific on what agents will be used, where the agents will look for/work in, and an into-depth format of what it will be doing.\n"
        "- action_items: Detailed list of specific tasks to be performed (e.g. The code fetches and displays projects with title, description, and other details. To show the description below the title, I will modify the JSX to position the `<p>` element containing `project.description` immediately after the project title `<h3>`. This will ensure the description appears directly below each post's title while maintaining the existing layout. The next step is editing the rendering section accordingly.)\n"
        "- agent: The specific agent (by name) responsible for executing this step\n"
        "- modification_status: \"unchanged\", \"modified\", \"added\", or \"removed\" (to track what changed)\n"
        "- modification_reason: Brief explanation of why this step was changed (only if modified/added/removed)\n\n"
        "When updating the plan:\n"
        "1. Clearly identify which steps are affected by the new input\n"
        "2. Renumber steps sequentially after modifications\n"
        "3. Update dependencies to reflect any structural changes\n"
        "4. Ensure the updated plan maintains logical flow and completeness\n"
        "5. Preserve valuable work and insights from the original plan where applicable\n\n"
        f"Existing Plan:\n{plan_json}\n\n"
        f"New Input: \n{update_input}\n\n"
        "Updated Plan:"

    )
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.2,
    )
    content = response.choices[0].message.content
    try:
        updated_plan = json.loads(content)
        if isinstance(updated_plan, dict):
            for v in updated_plan.values():
                if isinstance(v, list):
                    return v
        elif isinstance(updated_plan, list):
            return updated_plan
    except Exception:
        return [{"step_number": 1, "description": content, "action_items": []}]
    return []

# Example argument for generate_detailed_plan
if __name__ == '__main__':
    example_task = "I need to learn a lot about the effects of global warming on sea coral."
    example_agents = [
        "Alice - Research Agent (conducts web searches, gathers scientific articles and data on global warming effects on sea coral, compiles raw findings)",
        "Bob - Code Agent (writes scripts to process and visualize coral reef data, automates extraction of relevant statistics from datasets)",
        "Carol - Content Agent (writes and edits the research report, synthesizes findings into clear, accessible language, formats the document for presentation)",
        "Dave - Analysis Agent (analyzes collected data, identifies trends and key impacts, prepares summary tables and charts for the report)",
        "Eve - Coordination Agent (assigns tasks, tracks progress, ensures all sections of the report are completed and integrated, manages deadlines)"
    ]
    plan = generate_detailed_plan(example_task, available_agents=example_agents)
    print("Initial Plan:")
    for step in plan:
        print(step)

    # Example: updating the plan with new input
    print("\n--- Updating Plan with New Input ---")
    update_input = "Include a section on the economic impact of coral bleaching."
    # Assume update_plan_with_input is defined in this module
    try:
        updated_plan = update_plan_with_input(
            plan=plan,
            update_input=update_input,
            available_agents=example_agents
        )
        print("Updated Plan:")
        for step in updated_plan:
            print(step)
    except Exception as e:
        print(f"Error updating plan: {e}")
