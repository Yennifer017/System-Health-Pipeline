def build_summary_message(summary: dict) -> str:
    """
    Builds a human-readable summary message.
    """

    return (
        "📊 System Summary\n\n"
        f"📁 Total logs: {summary['total']}\n"
        f"🚨 Critical: {summary['critical']}\n"
        f"⚠️ Warning: {summary['warning']}\n"
        f"ℹ️ Info: {summary['info']}"
    )


def build_log_message(logs: list[dict], title: str) -> str:
    """
    Builds a Telegram-friendly message from a list of logs.
    """

    if not logs:
        return f"{title}\n\nNo se encontraron logs"

    message = [title, ""]

    for log in logs:
        message.append(
            "\n".join([
                f"🕒 {log['timestamp']}",
                f"🖥 CPU : {log['cpu']}% ({log['cpu_status']})",
                f"💾 Disco: {log['disk']}% ({log['disk_status']})",
                f"🧠 RAM : {log['ram']} MB ({log['ram_status']})",
                "-" * 30
            ])
        )

    return "\n".join(message)