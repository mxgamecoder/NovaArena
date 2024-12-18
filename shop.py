from telegram import ReplyKeyboardMarkup

async def show_shop_menu(update, context):
    # Define the shop items with emojis
    shop_items = [
        '💎 Diamonds - 50 Coins', 
        '🏅 Gold - 30 Coins', 
        '📦 Mystery Box - 100 Coins', 
        '🎟️ Bonus Ticket - 20 Coins',
        '🔋 Energy Boost - 15 Coins',
        '🎯 Accuracy Charm - 25 Coins'
    ]
    
    # Create the shop menu with a back option
    shop_keyboard = [
        [shop_items[0], shop_items[1]],
        [shop_items[2], shop_items[3]],
        [shop_items[4], shop_items[5]],
        ['🔙 Back']
    ]
    
    # Send the shop list as a message with a keyboard
    await update.message.reply_text(
        "🛒 *Shop*:\nBrowse and buy items to boost your adventure:",
        reply_markup=ReplyKeyboardMarkup(shop_keyboard, resize_keyboard=True)
    )