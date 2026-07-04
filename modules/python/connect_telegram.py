import os
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from checker import (load_analysis, summarize_logs, get_logs_by_level, get_last_logs)
from mss_builder import (build_summary_message, build_log_message)
from parse_commands import parse_command

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
JSON_PATH = ROOT / "output" / "analysis.json"

def load_data():
    return load_analysis(JSON_PATH)


async def summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    summary = summarize_logs(data)
    message = build_summary_message(summary)
    await update.message.reply_text(message)


async def critical(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    limit = parse_command(context.args)
    logs = get_logs_by_level(data, "CRITICAL", limit)
    message = build_log_message(
        logs,
        title=f"🚨 Last {len(logs)} Critical Logs"
    )
    await update.message.reply_text(message)


async def warning(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    limit = parse_command(context.args)
    logs = get_logs_by_level(data, "WARNING", limit)
    message = build_log_message(
        logs,
        title=f"⚠️ Last {len(logs)} Warning Logs"
    )
    await update.message.reply_text(message)


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    limit = parse_command(context.args)
    logs = get_logs_by_level(data, "INFO", limit)
    message = build_log_message(
        logs,
        title=f"ℹ️ Last {len(logs)} Info Logs"
    )

    await update.message.reply_text(message)


async def all_logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    limit = parse_command(context.args)
    summary = summarize_logs(data)
    logs = get_last_logs(data, limit)
    message = (
        build_summary_message(summary)
        + "\n\n"
        + build_log_message(logs, title=f"📋 Ultimos Logs")
    )
    await update.message.reply_text(message)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        """
        Comandos disponibles

        /summary

        /all [n]
        /critical [n]
        /warning [n]
        /info [n]

        Por defecto: 5 logs
        Máximo: 20 logs
        """
    )


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("summary", summary))
    app.add_handler(CommandHandler("critical", critical))
    app.add_handler(CommandHandler("warning", warning))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("all", all_logs))

    print("Telegram bot running...")

    app.run_polling()


if __name__ == "__main__":
    main()