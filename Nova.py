import logging
import re
import json
import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ContextTypes

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = '7450030858:AAH_lCeQ49K9kJoxAmdfaFnV7cQGLue0myE'
TARGET_USER_ID = 6408716304  # Replace with your target user ID
USER_DATA_FILE = 'user_data.json' #where i store users file 

# Load user data
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

# Function to get a list of user IDs
def get_user_ids():
    user_data = load_user_data()
    return [user_id for user_id in user_data.keys()]
    
# Define your balance file path
BALANCE_FILE = 'balance_data.json'

# Initialize balance_store
if os.path.exists(BALANCE_FILE):
    with open(BALANCE_FILE, 'r') as f:
        balance_store = json.load(f)
else:
    balance_store = {}

# Function to save balance data
def save_balance():
    with open(BALANCE_FILE, 'w') as f:
        json.dump(balance_store, f)

# Function to get balance
def get_balance(user_id):
    return balance_store.get(str(user_id), 0)

# Function to update balance
def update_balance(user_id, amount):
    if str(user_id) not in balance_store:
        balance_store[str(user_id)] = 0
    balance_store[str(user_id)] += amount
    save_balance()
from game import (
    show_game_menu, 
    handle_tic_tac_toe,
    handle_chess_duel,        # Add handler for Chess Duel
    handle_dart_master,       # Add handler for Dart Master
    handle_dice_roll,         # Add handler for Dice Roll Battle
    handle_penalty_shootout,  # Add handler for Penalty Shootout
    handle_racing_challenge,  # Add handler for Racing Challenge
    handle_space_invaders,    # Add handler for Space Invaders
    handle_puzzle_solver,     # Add handler for Puzzle Solver
    handle_bowling_strike,    # Add handler for Bowling Strike
    handle_archery_championship,  # Add handler for Archery Championship
    handle_memory_challenge,  # Add handler for Memory Challenge
    handle_card_game_duel     # Add handler for Card Game Duel
)
from Clan import show_clan_menu,  handle_clan_button_click# Import the clan menu from clan.py
from fund import show_fund_menu  # Import the fund menu from fund.py
from shop import show_shop_menu  # Import the shop menu from shop.py
from stats import show_stats_menu  # Import the stats menu from stats.py
from settings import show_settings # Import the clan menu from settings.py
from account import show_account_menu  # Import the account menu from account.py
from task import show_task_menu  # Import the task menu from task.py
from balance import show_balance, give_bonus, get_balance, update_balance  # Add get_balance and update_balance
from profile import show_profile, show_achievements, award_achievement
# Add these imports at the top if they are not already present
from stats import show_level, show_achievement, show_referrals, show_victories, show_defeats, show_daily_bonus  # Import the functions
from tic import handle_tic_tac_toe_start, handle_tic_tac_toe_move, handle_symbol_choice, handle_new_game_response #Import the Tic Tac Toe functions
from online import join_game
# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# In-memory storage for demonstration (use a database in production)
user_data_store = {
    'usernames': set(),
    'emails': set(),
    'phone_numbers': set()
}


async def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    user_id = str(user.id)
    referrer_id = context.args[0] if context.args else None

    # Load user data at the beginning of the function
    user_data = load_user_data()  # Ensure this function exists and is correctly defined

    # Initialize balance for the user if not present
    if str(user_id) not in balance_store:
        balance_store[str(user_id)] = 0
        save_balance()  # Ensure this function exists and is correctly defined

    # Handle referrals
    if referrer_id:
        if referrer_id == user_id:
            await update.message.reply_text("🚫 Oops! You cannot refer yourself! This is a quest meant for adventurers, not for solitary heroes")
            return

        # Check if the referrer exists
        if referrer_id not in user_referrals:
            user_referrals[referrer_id] = {"count": 0, "referred_users": []}
        
        # Check if the user has already been referred
        if user_id in user_data:
            await update.message.reply_text("⚠️ You've already been referred by someone else. Your journey in NovaArena is still exciting without double referrals!")
            return

        # Update the referral count and save data
        user_referrals[referrer_id]["count"] += 1
        user_referrals[referrer_id]["referred_users"].append(user_id)
        save_referral_data(user_referrals)  # Save updated referral data

        # Update balances
        update_balance(referrer_id, 10)  # Ensure this function exists

        # Notify the referrer about the successful referral
        updated_balance = get_balance(referrer_id)  # Ensure this function exists
        await context.bot.send_message(
            chat_id=referrer_id,
            text=f"🎉 Hark! A new adventurer has joined your quest!\n"
                 f"💸 A bonus of 10 Nova has been credited to your balance.\n"
                 f"Your updated balance is: {updated_balance} ⭐️ Nova."
        )

        # Send a welcome message to the referred user
        await update.message.reply_text(
            "🌟 Welcome to the land of NovaArena! You’ve been guided here through a referral link!"
        )
        
    # Check if the user is already registered in the file
    if str(user_id) in user_data:
        context.user_data.update(user_data[str(user_id)])
        await update.message.reply_text(
            f"🌟 Welcome back, {context.user_data['full_name']}! Ready to continue your journey in NovaArena? 🌟",
            reply_markup=ReplyKeyboardMarkup([
                ['👤 Account', '🏰 Clan', '📜 Continue Story'],
                ['🎮 Play Game', '🛒 Shop', '📊 Stats'],
                ['📝 Task', '⚙️ Settings', '💰 Fund'],
                ['🏆 Leaderboards']
            ], resize_keyboard=True)
        )
    else:
        await update.message.reply_text(
            "🛡️ Greetings, brave adventurer! 🌍 You’ve entered the mystical realm of NovaArena.\n"
            "⚔️ To join our world, you must first prepare yourself. Let’s create your character!"
        )
        await update.message.reply_text(
            "🎭 Choose your class to begin your journey: ⚔️ Warrior, 🧙‍♂️ Mage, 🏹 Archer, or 🛡️ Defender.",
            reply_markup=ReplyKeyboardMarkup([
                ['⚔️ Warrior', '🧙‍♂️ Mage'],
                ['🏹 Archer', '🛡️ Defender']
            ], one_time_keyboard=True, resize_keyboard=True)
        )
        # Set the user's stage to class selection
        context.user_data['stage'] = 'class_selection'
        

# File to store referral data
REFERRAL_FILE = "user_referrals.json"

# Load referral data
def load_referral_data():
    if os.path.exists(REFERRAL_FILE):
        with open(REFERRAL_FILE, "r") as f:
            return json.load(f)
    return {}

# Save referral data
def save_referral_data(user_referrals):
    with open(REFERRAL_FILE, "w") as f:
        json.dump(user_referrals, f)

user_referrals = load_referral_data()  # Load at startup


async def referral_link_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    referral_link = f"https://t.me/NovaArenaGameBot?start={user_id}"

    # Count the number of referrals
    referrals = user_referrals.get(user_id, {"count": 0, "referred_users": []})
    referral_count = referrals["count"]

    # Create the referral story message
    referral_message = (
        f"🌀 **Your Epic Adventure Begins!** 🌀\n\n"
        f"🌟 **Summon Your Friends!** 🌟\n\n"
        f"🌐 **Your Magic Referral Link:**\n\n"
        f"🪄 {referral_link}\n\n"
        f"🏆 **You have already rallied {referral_count} brave adventurers to join the quest!**\n\n"
        "✨ **The more heroes you bring, the greater your fortune!**\n\n"
        "💰 **Rewards:**\n"
        "For every adventurer who joins using your link, you’ll be granted **10 ⭐️ Nova** to help you conquer even more challenges! 🏅\n\n"
        "🗺 **Referral Adventure:**\n"
        "Track your progress and gather your crew right here in the bot. The bigger your party, the more Nova you'll earn to aid in your journey! 🌠"
    )
    await update.message.reply_text(referral_message)


async def handle_message(update: Update, context: CallbackContext) -> None:
    stage = context.user_data.get('stage')
    user_data = load_user_data()  # Assuming this function loads user data
    user_text = update.message.text

    # Handle new game response
    if user_text in ['Yes', 'No']:
        await handle_new_game_response(update, context)
    elif user_text == '↩️ Back':
        await handle_tic_tac_toe(update, context)

    # Handle specific messages for account, clan, and user stats
    elif user_text == '🌐 Online Friend':
        await join_game(update, context)
    elif user_text == '🤖 AI':
        await handle_tic_tac_toe_start(update, context)  # Start the game and ask for symbol choice
    elif user_text == '🔙 Go Back':
        await show_account_menu(update, context)
    elif user_text == 'Back 🔙':
        await show_game_menu(update, context)

    # Clan buttons
    clan_buttons = [
        '💬 Clan Chat',
        '👥 Clan Members',
        '⚔️ Clan Battles',
        '🏰 Join Clan'
    ]

    if user_text in clan_buttons:
        await handle_clan_button_click(update, context)
    elif user_text == '👥 Friends':
        await referral_link_handler(update, context)
    elif user_text == '🏆 Achievements':
        await show_achievements(update, context)
    elif user_text == '📝 Profile':
        await show_profile(update, context)
    elif user_text == '🧙‍♂️ Level':
        await show_level(update, context)
    elif user_text == '🎯 Achievements':
        await show_achievement(update, context)
    elif user_text == '🫂 Referrals':
        await show_referrals(update, context)
    elif user_text == '⭐️ Nova':
        await show_balance(update, context)  # Show the user's balance
    elif user_text == '🏆 Victories':
        await show_victories(update, context)  # Show victories
    elif user_text == '⚔️ Defeats':
        await show_defeats(update, context)  # Show defeats
    elif user_text == '📅 Daily Login Streak':
        await show_daily_bonus(update, context)  # Show daily bonus
    elif user_text == '🔙 Back':
        await back_to_menu(update, context)

    # Other options...
    elif user_text == '📝 Task':
        await show_task_menu(update, context)
    elif user_text == '📊 Stats':
        await show_stats_menu(update, context)
    elif user_text == '🎁 Bonus':
        await give_bonus(update, context)  # Give the user a bonus
    elif user_text == '🛒 Shop':
        await show_shop_menu(update, context)
    elif user_text == '💰 Fund':
        await show_fund_menu(update, context)
    elif user_text == '🏰 Clan':
        await show_clan_menu(update, context)

    # Game options, route each game to its handler
    elif user_text == '❌⭕ Tic Tac Toe':
        await handle_tic_tac_toe(update, context)  # Start the game
    elif user_text in ['❌', '⭕']:  # Check if user selected a symbol
        await handle_symbol_choice(update, context)  # Handle symbol choice
    elif user_text in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '↩️ Back']:
        await handle_tic_tac_toe_move(update, context)  # Handle Tic Tac Toe moves
    elif user_text == '♟️ Chess Duel':
        await handle_chess_duel(update, context)
    elif user_text == '🎯 Dart Master':
        await handle_dart_master(update, context)
    elif user_text == '🎲 Dice Roll Battle':
        await handle_dice_roll(update, context)
    elif user_text == '⚽ Penalty Shootout':
        await handle_penalty_shootout(update, context)
    elif user_text == '🏎️ Racing Challenge':
        await handle_racing_challenge(update, context)
    elif user_text == '👾 Space Invaders':
        await handle_space_invaders(update, context)
    elif user_text == '🧩 Puzzle Solver':
        await handle_puzzle_solver(update, context)
    elif user_text == '🎳 Bowling Strike':
        await handle_bowling_strike(update, context)
    elif user_text == '🏹 Archery Championship':
        await handle_archery_championship(update, context)
    elif user_text == '🧠 Memory Challenge':
        await handle_memory_challenge(update, context)
    elif user_text == '🃏 Card Game Duel':
        await handle_card_game_duel(update, context)
    elif user_text == '🎮 Play Game':
        await show_game_menu(update, context)
    elif user_text == '👤 Account':
        await show_account_menu(update, context)
    elif user_text == '⚙️ Settings':
        await show_settings(update, context)

    # Handle the class selection and registration process here...
    if stage == 'class_selection':
        if user_text in ['⚔️ Warrior', '🧙‍♂️ Mage', '🏹 Archer', '🛡️ Defender']:
            context.user_data['selected_class'] = user_text
            await update.message.reply_text(
                f"Great choice! You have selected {user_text}. Now, every hero must carry a name known across the realms. 🏰 Please provide your full name, brave adventurer!",
                reply_markup=ReplyKeyboardRemove()  # Disable the keyboard
            )
            context.user_data['stage'] = 'full_name'
        else:
            await update.message.reply_text(
                "Hmm, that doesn't seem like a valid class. Please choose one of the following: ⚔️ Warrior, 🧙‍♂️ Mage, 🏹 Archer, or 🛡️ Defender."
            )

    elif stage == 'full_name':
        full_name = user_text
        if len(full_name) < 5:
            await update.message.reply_text(
                "Oh no! 😮 Your name must be at least 5 letters long to be remembered in the legends. 📜 Please try again, and choose a name worthy of the realms!"
            )
        elif not re.match("^[A-Za-z ]+$", full_name):
            await update.message.reply_text(
                "Oops! 🤔 Names in our world must only contain letters, no strange symbols 🌀 or numbers 🔢 allowed. Please try again with a proper hero's name!"
            )
        else:
            selected_class = context.user_data.get('selected_class', 'Adventurer')
            context.user_data['full_name'] = full_name
            await update.message.reply_text(
                f"Ah, {full_name}! A fine name indeed! As a {selected_class}, your journey is just beginning. 🌟 Now, every hero needs a special in-game username! Choose yours wisely. 📝",
                reply_markup=ReplyKeyboardRemove()  # Disable the keyboard
            )
            context.user_data['stage'] = 'username_selection'

    elif stage == 'username_selection':
        username = user_text

        if len(username) < 6 or len(username) > 20:
            await update.message.reply_text(
                "Hmm, usernames must be between 6 and 20 characters long. Please try again, brave soul! 😅"
            )
        elif not re.match("^[A-Za-z0-9]+$", username):
            await update.message.reply_text(
                "Oops! 🤔 Usernames can only contain letters and numbers, no spaces or symbols allowed. Try again, adventurer! 🛡️"
            )
        else:
            if username_already_taken(username, user_data):
                await update.message.reply_text(
                    "Ah! It seems that name is already claimed by another warrior. Choose a different one, or perhaps try this: "
                    f"{suggest_new_username(username)} 💡"
                )
            else:
                context.user_data['username'] = username
                user_data_store['usernames'].add(username)
                await update.message.reply_text(
                    f"{username}... A name that will be whispered in legends. 🏆 Are you sure this is the name you want to carry with you, {context.user_data['full_name']}? Type 'Yes' to confirm or 'No' to choose another one."
                )
                context.user_data['stage'] = 'username_confirmation'

    elif stage == 'username_confirmation':
        confirmation = user_text.lower()

        if confirmation == 'yes':
            await update.message.reply_text(
                f"Fantastic! {context.user_data['username']} is now yours, {context.user_data['full_name']}! Your adventure awaits... 🌟"
            )
            context.user_data['stage'] = 'email_entry'
            await update.message.reply_text(
                "Great! Now, please provide your email address. 📧"
            )

        elif confirmation == 'no':
            await update.message.reply_text(
                "No worries, brave adventurer! 🛡️ Let's try again. Please provide a new username:",
                reply_markup=ReplyKeyboardRemove()
            )
            context.user_data['stage'] = 'username_selection'

        else:
            await update.message.reply_text(
                "Oops! You must answer with 'Yes' or 'No'. Please confirm again: Do you want to keep this username? Type 'Yes' or 'No'."
            )

    elif stage == 'email_entry':
        email = user_text
        if len(email) < 6 or '@' not in email or '.com' not in email:
            await update.message.reply_text(
                "Oops! 🧐 Your email must be valid and at least 6 characters long. Please provide a proper email address."
            )
        elif email_already_taken(email, user_data):
            await update.message.reply_text(
                "This email is already registered. Please provide a different email address."
            )
        else:
            context.user_data['email'] = email
            user_data_store['emails'].add(email)
            await update.message.reply_text(
                "Great! Your email has been recorded. 📧 Now, please provide your phone number with country code (e.g., +123456789012).",
                reply_markup=ReplyKeyboardRemove()
            )
            context.user_data['stage'] = 'phone_number_entry'

    elif stage == 'phone_number_entry':
        phone_number = user_text
        if len(phone_number) < 12 or len(phone_number) > 14 or not phone_number.startswith('+') or not phone_number[1:].isdigit():
            await update.message.reply_text(
                "Oops! 📞 Your phone number must be in the international format, starting with '+' and contain 12-14 digits. Please try again."
            )
        elif phone_number_already_taken(phone_number, user_data):
            await update.message.reply_text(
                "This phone number is already registered. Please provide a different phone number."
            )
        else:
            context.user_data['phone_number'] = phone_number
            user_data_store['phone_numbers'].add(phone_number)

            # Collect all the data for the user
            user_info = {
                'full_name': context.user_data['full_name'],
                'class': context.user_data['selected_class'],
                'username': context.user_data['username'],
                'email': context.user_data['email'],
                'phone_number': phone_number
            }

            # Save user data to the JSON file
            save_user_data(update.message.from_user.id, user_info)

            await update.message.reply_text(
                "Awesome! Your phone number has been recorded. 📱 You’re all set! 🎉 Welcome to the game!",
                reply_markup=ReplyKeyboardRemove()
            )
            context.user_data['is_registered'] = True
            award_achievement(update.message.from_user.id, "First Steps", "Completed registration and joined NovaArena!")
            # Send registration details to the specified user
            bot = context.bot
            registration_details = (
                f"New Registration:\n"
                f"Full Name: {context.user_data['full_name']}\n"
                f"Class: {context.user_data['selected_class']}\n"
                f"Username: {context.user_data['username']}\n"
                f"Email: {context.user_data['email']}\n"
                f"Phone Number: {context.user_data['phone_number']}"
            )
            await bot.send_message(chat_id=TARGET_USER_ID, text=registration_details)
            context.user_data['stage'] = 'menu'
            await show_menu(update, context)  # Transition to menu
            # Define the menu stage
async def show_menu(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Your journey has led you to the sacred hall of NovaArena. 🌟 From here, you can manage your account, join a clan, or explore more stories. Choose your path, adventurer!",
        reply_markup=ReplyKeyboardMarkup([
            ['👤 Account', '🏰 Clan', '📜 Continue Story'],
            ['🎮 Play Game', '🛒 Shop', '📊 Stats'],
            ['📝 Task', '⚙️ Settings', '💰 Fund'],
            ['🏆 Leaderboards']
        ], resize_keyboard=True)
    )
    context.user_data['stage'] = 'menu'

# Handler to go back to the main menu
async def back_to_menu(update: Update, context: CallbackContext) -> None:
    await show_menu(update, context)
    
#where i store user files
# Function to load user data from the JSON file
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        # Load existing user data from the file
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    else:
        # Return an empty dictionary if the file does not exist
        return {}

# Function to save user data to the JSON file
def save_user_data(user_id, user_info):
    user_data = load_user_data()  # Load existing data
    user_data[user_id] = user_info  # Add or update user info

    # Write the updated data back to the file
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(user_data, file, indent=4)  # Pretty print with 4-space indentation

# Function to check if the username is already taken (dummy implementation)
# Function to check if the username is already taken
def username_already_taken(username, user_data):
    return any(user['username'] == username for user in user_data.values())

# Function to suggest a new username (dummy implementation)
def suggest_new_username(username):
    return f"{username}_theBrave"


# Function to check if the phone number is already taken
def phone_number_already_taken(phone_number, user_data):
    return any(user['phone_number'] == phone_number for user in user_data.values())
    
    # Function to check if the email is already taken
def email_already_taken(email, user_data):
    return any(user['email'] == email for user in user_data.values())
# Define the error handler
def error_handler(update: Update, context: CallbackContext) -> None:
    logging.warning(f'Update {update} caused error {context.error}')

# Create the Application and pass it your bot's token
application = Application.builder().token(TOKEN).build()

# Add command handlers
application.add_handler(CommandHandler("start", start))

# Add message handler for both class selection and full name
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Add error handler
application.add_error_handler(error_handler)

# Run the bot
def run() -> None:
    application.run_polling()

if __name__ == '__main__':
    run()