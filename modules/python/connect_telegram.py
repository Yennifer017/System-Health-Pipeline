import os
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from checker import (load_analysis, summarize_logs, get_logs_by_level, get_last_logs)
from mss_builder import (build_summary_message, build_log_message)
from parse_commands import parse_command
from telegram import BotCommand
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler


ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
JSON_PATH = ROOT / "output" / "analysis.json"

def load_data():
    return load_analysis(JSON_PATH)


async def reply(update: Update, text: str):
    if update.message:
        await update.message.reply_text(text)
    else:
        await update.callback_query.edit_message_text(text)


async def post_init(application):
    await application.bot.set_my_commands([
        BotCommand("summary", "Resumen del análisis"),
        BotCommand("all", "Mostrar últimos logs"),
        BotCommand("critical", "Mostrar errores críticos"),
        BotCommand("warning", "Mostrar warnings"),
        BotCommand("info", "Mostrar logs informativos"),
        BotCommand("start", "Mostrar menú principal"),
    ])


async def summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    summary = summarize_logs(data)
    message = build_summary_message(summary)
    await reply(update, message)


async def critical(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    limit = parse_command(context.args)
    logs = get_logs_by_level(data, "CRITICAL", limit)
    message = build_log_message(
        logs,
        title=f"🚨 Last {len(logs)} Critical Logs"
    )
    await reply(update, message)


async def warning(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    limit = parse_command(context.args)
    logs = get_logs_by_level(data, "WARNING", limit)
    message = build_log_message(
        logs,
        title=f"⚠️ Last {len(logs)} Warning Logs"
    )
    await reply(update, message)


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    limit = parse_command(context.args)
    logs = get_logs_by_level(data, "INFO", limit)
    message = build_log_message(
        logs,
        title=f"ℹ️ Last {len(logs)} Info Logs"
    )
    await reply(update, message)


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
    await reply(update, message)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton("📊 Resumen", callback_data="summary")
        ],
        [
            InlineKeyboardButton("📋 Últimos logs", callback_data="all_logs")
        ],
        [
            InlineKeyboardButton("🚨 Critical", callback_data="critical"),
        ],
        [
            InlineKeyboardButton("⚠️ Warning", callback_data="warning"),
        ],
        [
            InlineKeyboardButton("ℹ️ Info", callback_data="info")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        """
            🤖 Pipeline Monitor

            Selecciona una opción.

            📌 Los botones muestran los últimos 5 registros.
            Usa, por ejemplo, `/critical 10` o `/all 20` para consultar otra cantidad.
        """,
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    if query.data == "summary":
        await summary(update, context)
    elif query.data == "all_logs":
        await all(update, context)
    elif query.data == "critical":
        await critical(update, context)
    elif query.data == "warning":
        await warning(update, context)
    elif query.data == "info":
        await info(update, context)


def main():
    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .post_init(post_init)
        .build()
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("summary", summary))
    app.add_handler(CommandHandler("critical", critical))
    app.add_handler(CommandHandler("warning", warning))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("all", all_logs))
    app.add_handler(CallbackQueryHandler(button))

    print("Telegram bot running...")

    app.run_polling()


if __name__ == "__main__":
    main()