import json
from telegram import Update
from telegram.ext import CallbackContext
from datetime import datetime, timedelta
from profile import load_user_achievements, award_achievement

# File paths for balance and bonus storage
BALANCE_FILE = "balance_store.json"
BONUS_FILE = "bonus_store.json"

# Function to load JSON data from a file
def load_json(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

# Function to save JSON data to a file
def save_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f)

# Load balance and bonus data from files
balance_store = load_json(BALANCE_FILE)
bonus_store = load_json(BONUS_FILE)

# Function to get user's balance
def get_balance(user_id):
    return balance_store.get(str(user_id), 0)  # Default to 0 Novas if not found

# Function to update user's balance and save to file
def update_balance(user_id, amount):
    user_id = str(user_id)  # Ensure the key is a string for JSON compatibility
    if user_id in balance_store:
        balance_store[user_id] += amount
    else:
        balance_store[user_id] = amount
    save_json(BALANCE_FILE, balance_store)

# Function to display balance with storytelling and emojis
async def show_balance(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    balance = get_balance(user_id)
    await update.message.reply_text(
        f"🏰 *Hero’s Treasury Report* 🏰\n\n"
        f"Brave adventurer, the keepers of the realm have tallied your fortune... 💰\n"
        f"You currently possess *{balance} Nova(s)* in your treasury.\n\n"
        f"May fortune favor you as your legend continues! 🌟"
    )

# Function to check and add a daily bonus (1 Nova per day, once every 24 hours)
async def give_bonus(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    now = datetime.now()

    # Load bonus store
    bonus_store = load_json(BONUS_FILE)

    # Check when the user last received a bonus
    last_bonus_time = bonus_store.get(str(user_id))

    # If user has claimed a bonus within the last 24 hours
    if last_bonus_time:
        last_bonus_time = datetime.fromisoformat(last_bonus_time)
        time_diff = now - last_bonus_time
        if time_diff < timedelta(hours=24):
            time_left = timedelta(hours=24) - time_diff
            hours_left = time_left.seconds // 3600
            minutes_left = (time_left.seconds % 3600) // 60
            await update.message.reply_text(
                f"⏳ *Bonus on Hold* ⏳\n\n"
                f"Adventurer, you have already claimed your reward for today! 🎁\n"
                f"You can return to claim more Novas in *{hours_left} hours and {minutes_left} minutes*.\n"
                f"Patience is a virtue, the stars will align again soon! 🌠"
            )
            return

    # If 24 hours have passed or it's the first bonus, give 1 Nova
    bonus_amount = 1
    update_balance(user_id, bonus_amount)

    # Update the bonus store with the current time and save it
    bonus_store[str(user_id)] = now.isoformat()
    save_json(BONUS_FILE, bonus_store)

    # Check for the first bonus achievement
    achievements = load_user_achievements()  # Load user achievements
    if "First Bonus" not in achievements.get(str(user_id), {}):
        award_achievement(user_id, "First Bonus", "Claimed your first daily bonus!")
    
    await update.message.reply_text(
        f"🎁 *Daily Bonus Received* 🎁\n\n"
        f"Congratulations, brave adventurer! 🌟\n"
        f"The gods of the realm have blessed you with *{bonus_amount} Nova*.\n"
        f"Return in 24 hours for another gift! 🕰️\n\n"
        f"Your current balance: 💰 *{get_balance(user_id)} Nova(s)*.\n"
        f"Continue your journey with fortune by your side! 🏆"
    )