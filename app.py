
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

TOKEN = os.environ["BOT_TOKEN"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً بك في بوت نزع الموسيقى 🎬\n\n"
        "ابعثلي فيديو من جهازك، ثم اختار الخدمة."
    )


async def receive_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎙️ فصل الموسيقى عن الكلام", callback_data="separate")],
        [InlineKeyboardButton("🔇 حذف الصوت كاملًا", callback_data="mute")],
        [InlineKeyboardButton("ℹ️ معالجة العلامة المائية", callback_data="watermark")],
    ]
    await update.message.reply_text(
        "استلمت الفيديو. اختار الخدمة:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def choose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    messages = {
        "separate": "فصل الموسيقى عن الكلام لم تتم إضافته بعد.",
        "mute": "حذف الصوت لم تتم إضافته بعد.",
        "watermark": "معالجة العلامة المائية لم تتم إضافتها بعد.",
    }
    await query.message.reply_text(messages.get(query.data, "خيار غير معروف."))


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO, receive_video))
    app.add_handler(CallbackQueryHandler(choose))
    app.run_polling()


if __name__ == "__main__":
    main()
