from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
from config import BOT_TOKEN, ADMIN_CHAT_ID

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Залишити заявку", callback_data="apply")],
        [InlineKeyboardButton("Отримати інформацію", callback_data="info")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Вітаємо! Оберіть опцію:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "apply":
        user_data[query.from_user.id] = {}
        await query.message.reply_text("Введіть ваше ім’я:")
        context.user_data["stage"] = "name"
    elif query.data == "info":
        await query.message.reply_text("Ось коротка інформація: ...")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    stage = context.user_data.get("stage")

    if stage == "name":
        user_data[user_id]["name"] = update.message.text
        await update.message.reply_text("Введіть номер телефону:")
        context.user_data["stage"] = "phone"
    elif stage == "phone":
        user_data[user_id]["phone"] = update.message.text
        name = user_data[user_id]["name"]
        phone = user_data[user_id]["phone"]
        await update.message.reply_text("Дякуємо! Дані надіслано.")
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"Нова заявка:\n👤 Ім’я: {name}\n📞 Телефон: {phone}"
        )
        context.user_data.clear()

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
