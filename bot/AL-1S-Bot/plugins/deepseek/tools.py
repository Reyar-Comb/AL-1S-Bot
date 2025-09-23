def short(message: str) -> str:
    if len(message) > 25:
        return message[:25] + "..."
    return message