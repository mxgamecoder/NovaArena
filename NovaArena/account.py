from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext

# Update the show_account_menu to add the referral option
async def show_account_menu(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "👤 *Account Options*:\n"
        "Here you can view and manage your account details. Choose an option:",
        reply_markup=ReplyKeyboardMarkup([
            ['⭐️ Nova', '📝 Profile'],
            ['🏆 Achievements', '🎁 Bonus'],
            ['👥 Friends', '📊 Stats'],
            ['🔙 Back']
        ], resize_keyboard=True)
    )
    
    # Handler to go back to the main menu
async def back_to_menu(update: Update, context: CallbackContext) -> None:
    await show_account_menu(update, context)