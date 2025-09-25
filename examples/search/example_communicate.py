from swarms import Agent
from swarms_tools.search.msg_notify_user import notify_user

agent = Agent(
    agent_name="Psychologist",
    agent_description=(
        "A supportive psychologist agent that checks in on the user's mood, asks gentle follow-up questions, "
        "and offers empathetic, encouraging advice. "
        "You can use the notify_user tool to interact with the user: ask questions, report status, or share supportive messages. "
        "Always provide clear status updates (e.g., 'Processing your response...', 'Thank you for sharing', 'Preparing advice...') "
        "when appropriate, to demonstrate status reporting. "
        "You may ask about feelings, offer coping strategies, or encourage the user to elaborate. "
        "Be gentle, non-judgmental, and concise in your interactions."
    ),
    max_loops=1,
    model_name="gpt-4o-mini",
    tools=[notify_user],
    dynamic_temperature_enabled=True,
)


"""
#TEST -> Message & Get User Input
"""

agent.run(
    "Send messages while thinking on helping me as I am really sad and stressed becasue of college applications." 
)