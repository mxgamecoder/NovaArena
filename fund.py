from telegram import ReplyKeyboardMarkup

async def show_fund_menu(update, context):
    # Define a list of fund-related options with emojis
    fund_options = [
        '💰 Deposit Funds', 
        '🏦 Withdraw Funds', 
        '⚙️ Set wallet Address', 
        '💸 Transaction History'
    ]
    
    # Create the fund menu with a back option
    fund_keyboard = [
        [fund_options[0], fund_options[1]],
        [fund_options[2], fund_options[3]],
        ['🔙 Back']
    ]
    
    # Send the fund options as a message with a keyboard
    await update.message.reply_text(
        "💰 *Fund Menu*:\nChoose an option to manage your funds:",
        reply_markup=ReplyKeyboardMarkup(fund_keyboard, resize_keyboard=True)
    )