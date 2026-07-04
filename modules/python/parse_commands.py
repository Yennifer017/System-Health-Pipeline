def parse_command(command: str) -> tuple[str, int | None]:
    """
    Parses commands such as:

    /critical
    /critical 10
    /warning 5
    /info
    /sumary
    """

    parts = command.split()

    action = parts[0].lower()

    limit = None

    if len(parts) == 2 and parts[1].isdigit():
        limit = int(parts[1])

    return action, limit