import logging
import os
from dotenv import load_dotenv
import db_op as db

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters
)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
SERVER_PASSWORD = os.getenv("PASSWORD")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    #level=logging.INFO
)

# Define conversation states
PASSWORD = range(1)[0]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    if user.is_bot:
        logging.warning("Bot user detected: %s", user.username)
        await update.message.reply_text("Bots are not allowed")
        return ConversationHandler.END
    elif db.exists(user.id):
        await update.message.reply_text("You are already opted in")
        return ConversationHandler.END
    logging.info("User %s started conversation", user.id)
    await update.message.reply_text("Send the server password")
    return PASSWORD

async def get_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if password == SERVER_PASSWORD:
        await update.message.reply_text(db.add_user(user.id))
    else:
        logging.warning("Incorrect password sent by user %s", user.username)
        await update.message.reply_text("Incorrect password")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

conv = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        PASSWORD: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_password)
        ]
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    allow_reentry=True
)

if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(conv)
    application.run_polling()
