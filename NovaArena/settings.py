from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

# Function to show settings menu
async def show_settings(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "⚙️ *Settings Menu*:\n"
        "Adventurer, here you can customize your journey! Choose wisely:",
        reply_markup=ReplyKeyboardMarkup([
            ['🌐 Change Language', '🔔 Toggle Notifications'],
            ['🔒 Privacy Settings', '🔑 Change Account Info'],
            ['🗑️ Delete Account', '📄 Export Data'],
            ['🔙 Back']
        ], resize_keyboard=True)
    )