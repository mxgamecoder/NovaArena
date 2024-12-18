import json
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

# JSON files to store profile and achievements data
USER_DATA_FILE = 'user_data.json'
ACHIEVEMENTS_FILE = 'achievements.json'

# Function to load user profile data
def load_profile_data(user_id):
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            user_data = json.load(file)
            return user_data.get(str(user_id), {})
    return {}

# Function to load user achievements
def load_achievements(user_id):
    achievements = load_user_achievements()
    return achievements.get(str(user_id), [])

# Function to award achievements
def award_achievement(user_id, title, description):
    achievements = load_user_achievements()
    if str(user_id) not in achievements:
        achievements[str(user_id)] = {}
    achievements[str(user_id)][title] = description
    save_user_achievements(user_id, achievements[str(user_id)])

# Function to load user achievements
def load_user_achievements():
    if os.path.exists(ACHIEVEMENTS_FILE):
        with open(ACHIEVEMENTS_FILE, 'r') as file:
            return json.load(file)
    return {}

# Function to save user achievements
def save_user_achievements(user_id, achievements):
    all_achievements = load_user_achievements()
    all_achievements[str(user_id)] = achievements
    with open(ACHIEVEMENTS_FILE, 'w') as file:
        json.dump(all_achievements, file, indent=4)

# Function to display the user's profile
async def show_profile(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    profile = load_profile_data(user_id)

    if profile:
        full_name = profile.get('full_name', 'Unknown Adventurer')
        selected_class = profile.get('class', 'No Class Selected')
        username = profile.get('username', 'Unknown Username')
        email = profile.get('email', 'Unknown Email')

        profile_message = (
            f"👤 *Profile Information*:\n"
            f"📛 *Full Name*: {full_name}\n"
            f"⚔️ *Class*: {selected_class}\n"
            f"🏷 *Username*: {username}\n"
            f"📧 *Email*: {email}\n"
        )
    else:
        profile_message = "🚫 No profile information found. Please complete your registration."

    await update.message.reply_text(profile_message)

# Function to display the user's achievements
async def show_achievements(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    achievements = load_achievements(user_id)

    if achievements:
        achievements_message = "🏆 *Your Achievements*:\n"
        for title, description in achievements.items():
            achievements_message += f"- {title}: {description}\n"
    else:
        achievements_message = "🎯 You have no achievements yet. Keep playing to earn some!"

    await update.message.reply_text(achievements_message)

# Add new achievements (example function)
async def add_achievement(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    achievement = "First Victory!"  # Example achievement

    achievements = load_achievements(user_id)
    if achievement not in achievements:
        achievements.append(achievement)
        save_user_achievements(user_id, achievements)
        await update.message.reply_text(f"🎉 *New Achievement Unlocked*: {achievement}")
    else:
        await update.message.reply_text("You already unlocked this achievement!")