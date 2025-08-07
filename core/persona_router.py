def route_command(command, twin):
    # Simple keyword trigger to Echo
    if 'echo' in command.lower() or 'glenn' in command.lower():
        return f"Echo here. You said: '{command}'"
    return f"I heard you, but I don't yet know how to handle: '{command}'"
