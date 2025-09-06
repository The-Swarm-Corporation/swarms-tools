from typing import List, Dict, Any
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_detailed_plan(task_input: str, model: str = "gpt-4-turbo") -> List[Dict[str, Any]]:
    """
    Uses an AI model to generate a highly detailed, specific, and executable plan for the given task.
    Each step is an object in the returned list.

    Args:
        task_input (str): The description of the task to plan for.
        model (str): The OpenAI model to use.

    Returns:
        List[Dict[str, Any]]: A list of step objects, each representing a step in the plan.
    """
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
        "- Research agents (web search, data analysis, information gathering)\n"
        "- Code agents (development, debugging, testing, file operations)\n"
        "- Content agents (writing, editing, creative tasks)\n"
        "- Analysis agents (data processing, evaluation, reporting)\n"
        "- Coordination agents (task management, status tracking)\n\n"
        "Return the plan as a JSON array where each step contains:\n"
        "- step_number: Sequential identifier\n"
        "- description: Clear, specific description of what needs to be accomplished\n"
        "- agent_type: The type of agent best suited for this step\n"
        "- action_items: Detailed list of specific tasks to be performed\n"
        "- inputs: Required inputs/resources/dependencies from previous steps\n"
        "- outputs: Expected deliverables/artifacts to be produced\n"
        "- success_criteria: Measurable criteria for step completion\n"
        "- estimated_duration: Rough time estimate (in appropriate units)\n"
        "- priority: High/Medium/Low priority level\n"
        "- dependencies: Array of step numbers this step depends on (empty array if none)\n"
        "- failure_contingency: Brief plan for handling potential failures\n"
        "- verification_method: How to confirm the step was completed successfully\n\n"
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

def update_plan_with_input(plan: List[Dict[str, Any]], update_input: str, model: str = "gpt-4-turbo") -> List[Dict[str, Any]]:
    """
    Uses an AI model to update the given plan based on new input.

    Args:
        plan (List[Dict[str, Any]]): The current plan as a list of step objects.
        update_input (str): The new input or change to consider (e.g., feedback, new requirements).
        model (str): The OpenAI model to use.

    Returns:
        List[Dict[str, Any]]: The updated plan as a list of step objects.
    """
    import json
    plan_json = json.dumps(plan, indent=2)
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
        "- Research agents (web search, data analysis, information gathering)\n"
        "- Code agents (development, debugging, testing, file operations)\n"
        "- Content agents (writing, editing, creative tasks)\n"
        "- Analysis agents (data processing, evaluation, reporting)\n"
        "- Coordination agents (task management, status tracking)\n\n"
        "Return the plan as a JSON array where each step contains:\n"
        "- step_number: Sequential identifier\n"
        "- description: Clear, specific description of what needs to be accomplished\n"
        "- agent_type: The type of agent best suited for this step\n"
        "- action_items: Detailed list of specific tasks to be performed\n"
        "- inputs: Required inputs/resources/dependencies from previous steps\n"
        "- outputs: Expected deliverables/artifacts to be produced\n"
        "- success_criteria: Measurable criteria for step completion\n"
        "- estimated_duration: Rough time estimate (in appropriate units)\n"
        "- priority: High/Medium/Low priority level\n"
        "- dependencies: Array of step numbers this step depends on (empty array if none)\n"
        "- failure_contingency: Brief plan for handling potential failures\n"
        "- verification_method: How to confirm the step was completed successfully\n"
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
    plan = generate_detailed_plan(example_task)
    for step in plan:
        print(step)
