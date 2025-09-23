def short(message: str) -> str:
    if len(message) > 50:
        return message[:20] + "..." + message[-20:]
    return message