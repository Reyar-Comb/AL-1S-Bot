def short(message: str) -> str:
    if len(message) > 1000:
        return message[:500] + "..." + message[-500:]
    return message