def short(message: str) -> str:
    if len(message) > 400:
        return message[:200] + "\n...\n" + message[-200:]
    return message