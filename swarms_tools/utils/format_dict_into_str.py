def format_dict_into_str(d: dict) -> str:
    """
    Formats every key and value in the dictionary as 'key: value' per line, with a blank line between each pair.
    """
    return "\n\n".join(f"{k}: {v}" for k, v in d.items())
