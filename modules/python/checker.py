import json

MIN_LIMIT = 1
DEFAULT = 5
MAX_LIMIT = 20


def load_analysis(path: str) -> list[dict]:
    """
    Reads the analysis JSON file.

    Args:
        path: Path to analysis.json.

    Returns:
        List of metric records.
    """
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def validate_limit(limit: int | None,
                   default: int = DEFAULT,
                   maximum: int = MAX_LIMIT) -> int:
    """
    Validates the requested limit.

    If no limit is provided, the default value is used.
    Limits larger than the maximum are capped.
    """

    if limit is None:
        return default

    if limit < MIN_LIMIT:
        return default

    return min(limit, maximum)


def get_last_logs(data: list[dict],
                  limit: int = 10) -> list[dict]:
    """
    Returns the last N records.
    """
    if(limit is None):
        limit = DEFAULT
    return data[-limit:]


def get_logs_by_level(data: list[dict],
                      level: str,
                      limit: int = DEFAULT) -> list[dict]:
    """
    Returns the latest records that contain the requested severity.

    A record is included if CPU, Disk or RAM matches the severity.
    """

    level = level.upper()
    limit = validate_limit(limit)

    logs = [
        row for row in data
        if (
            row["cpu_status"] == level
            or row["disk_status"] == level
            or row["ram_status"] == level
        )
    ]

    return logs[-limit:]


def summarize_logs(data: list[dict]) -> dict:
    """
    Computes a summary of all records.
    """

    summary = {
        "total": len(data),
        "critical": 0,
        "warning": 0,
        "info": 0
    }

    for row in data:

        statuses = (
            row["cpu_status"],
            row["disk_status"],
            row["ram_status"]
        )

        if "CRITICAL" in statuses:
            summary["critical"] += 1

        elif "WARNING" in statuses:
            summary["warning"] += 1

        else:
            summary["info"] += 1

    return summary


def get_all_summary(data: list[dict]) -> dict:
    """
    Summary plus the latest 10 logs.
    """

    return {
        "summary": summarize_logs(data),
        "logs": get_last_logs(data, 10)
    }
