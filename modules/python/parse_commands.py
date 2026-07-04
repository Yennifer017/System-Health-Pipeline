def parse_command(args: list[str]) -> int | None:
    """
    Parses the optional numeric argument of a Telegram command.

    Examples:
        /critical      -> None
        /critical 10   -> 10
        /critical 100  -> 20
        /critical abc  -> None
    """
    if not args:
        return None

    try:
        limit = int(args[0])
        if limit < 1:
            return None
        return limit
    except ValueError:
        return None