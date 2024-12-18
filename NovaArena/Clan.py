from telegram import ReplyKeyboardMarkup

async def show_clan_menu(update, context):
    # Define a list of clan-related options with emojis
    clan_options = [
        '🏰 Join Clan', 
        '⚔️ Clan Battles', 
        '👥 Clan Members', 
        '💬 Clan Chat', 
        '💰 Clan Treasury'
    ]
    
    # Create the clan menu with a back option
    clan_keyboard = [
        [clan_options[0], clan_options[1]],
        [clan_options[2], clan_options[3]],
        ['🔙 Back']
    ]
    
    # Send the clan options as a message with a keyboard
    await update.message.reply_text(
        "🏰 *Clan Menu*:\nChoose an option to manage your clan:",
        reply_markup=ReplyKeyboardMarkup(clan_keyboard, resize_keyboard=True)
    )

# Handle clan button clicks with a storytelling response
async def handle_clan_button_click(update, context):
    story_message = (
        "🌟 **A Glimpse Into the Future!** 🌟\n\n"
        "🔮 You eagerly press the button, hoping to unlock the mysteries of the clans...\n"
        "But alas, the magic of the next season hasn't yet arrived. 🌀\n\n"
        "⚔️ *Fear not, brave adventurer!* ⚔️\n"
        "The world of NovaArena is preparing something epic for its next season. The clans are gathering strength, the battles are becoming fiercer, and the treasury is about to overflow with untold riches! 💰\n\n"
        "📜 Stay tuned, for the legend of your clan is about to begin! 🌠"
    )
    
    await update.message.reply_text(story_message)