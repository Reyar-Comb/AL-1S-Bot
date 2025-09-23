def short(message: str) -> str:
    if len(message) > 15:
        return message[:15] + "..."
    return message