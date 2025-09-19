import sys

def notify_user(query: str) -> str:
    """
    User notification and input handler for agent requests and status.

    - If the agent needs user input, prompt the user and return their response.
    - If the agent is reporting status, print the status and return None.
    """

    query_lower = query.lower().strip()

    input_triggers = [
        "input", "need", "require", "waiting", "please provide", "user action", "enter", "your response", "respond", "type", "confirm"
    ]
    status_triggers = [
        "status", "progress", "update", "complete", "done", "finished", "processing"
    ]

    if (
        any(word in query_lower for word in input_triggers)
        or query_lower.endswith("?")
        or query_lower.startswith("please")
        or query_lower.startswith("enter")
    ):
        print(f"\n[AGENT REQUEST] {query}")
        sys.stdout.flush()
        try:
            user_response = input("Your input: ")
        except EOFError:
            print("[ERROR] No input received (EOF). Returning empty string.")
            return ""
        return user_response
    elif any(word in query_lower for word in status_triggers):
        print(f"\n[AGENT STATUS] {query}")
        sys.stdout.flush()
        return None

    else:
        print(f"\n[AGENT MESSAGE] {query}")
        sys.stdout.flush()
        return None