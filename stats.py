import json
import os
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, filters

# Files where data is stored
BALANCE_FILE = 'balance_store.json'
BONUS_FILE = 'bonus_store.json'
ACHIEVEMENT_FILE = 'achievements.json'
STATS_FILE = 'stats_store.json'

# Balance (Nova) Functions
def load_balance_data():
    if os.path.exists(BALANCE_FILE):
        with open(BALANCE_FILE, 'r') as file:
            return json.load(file)
    return {}

def get_balance(user_id):
    balance_data = load_balance_data()
    return balance_data.get(str(user_id), 0)

# Daily Bonus Functions
def load_bonus_data():
    if os.path.exists(BONUS_FILE):
        with open(BONUS_FILE, 'r') as file:
            return json.load(file)
    return {}

def get_daily_bonus_count(user_id):
    bonus_data = load_bonus_data()
    return bonus_data.get(str(user_id), 0)

# Achievements Functions
def load_achievement_data():
    if os.path.exists(ACHIEVEMENT_FILE):
        with open(ACHIEVEMENT_FILE, 'r') as file:
            return json.load(file)
    return {}

def get_achievements_count(user_id):
    achievement_data = load_achievement_data()
    return len(achievement_data.get(str(user_id), []))

# Stats (Level, Victories, Defeats, Referrals) Functions
def load_stats_data():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r') as file:
            return json.load(file)
    return {}

def get_level(user_id):
    stats_data = load_stats_data()
    return stats_data.get(str(user_id), {}).get('level', 1)

def get_victories(user_id):
    stats_data = load_stats_data()
    return stats_data.get(str(user_id), {}).get('victories', 0)

def get_defeats(user_id):
    stats_data = load_stats_data()
    return stats_data.get(str(user_id), {}).get('defeats', 0)

def get_referrals(user_id):
    stats_data = load_stats_data()
    return len(stats_data.get(str(user_id), {}).get('referrals', []))

# Function to show user stats as options
async def show_stats_menu(update, context):
    stats_keyboard = [
        ['🧙‍♂️ Level', '🫂 Referrals'],
        ['⭐️ Nova', '🏆 Victories'],
        ['⚔️ Defeats', '📅 Daily Login Streak'],
        ['🎯 Achievements', '🔙 Go Back']
    ]
    stats_message = "📊 *Your Stats*:\nChoose an option to view details:"

    await update.message.reply_text(
        stats_message,
        reply_markup=ReplyKeyboardMarkup(stats_keyboard, resize_keyboard=True)
    )

# Handlers for each stat
async def show_level(update, context):
    user_id = update.message.from_user.id
    level = get_level(user_id)
    await update.message.reply_text(f"🧙‍♂️ *Your Level*: {level}\nKeep progressing to reach new heights!")

async def show_referrals(update, context):
    user_id = update.message.from_user.id
    referrals = get_referrals(user_id)
    await update.message.reply_text(f"🫂 *Referrals*: {referrals}\nInvite more friends to grow your clan!")

async def show_balance(update, context):
    user_id = update.message.from_user.id
    balance = get_balance(user_id)
    await update.message.reply_text(f"⭐️ *Nova*: {balance}\nKeep earning Novas for future rewards!")

async def show_victories(update, context):
    user_id = update.message.from_user.id
    victories = get_victories(user_id)
    await update.message.reply_text(f"🏆 *Victories*: {victories}\nGreat job! Keep winning!")

async def show_defeats(update, context):
    user_id = update.message.from_user.id
    defeats = get_defeats(user_id)
    await update.message.reply_text(f"⚔️ *Defeats*: {defeats}\nDon’t worry, every defeat is a lesson!")

async def show_daily_bonus(update, context):
    user_id = update.message.from_user.id
    daily_bonus_count = get_daily_bonus_count(user_id)
    await update.message.reply_text(f"📅 *Daily Login Streak*: {daily_bonus_count}\nLog in daily to claim more bonuses!")

async def show_achievement(update, context):
    user_id = update.message.from_user.id
    achievements_count = get_achievements_count(user_id)
    await update.message.reply_text(f"🎯 *Achievements*: {achievements_count}\nYou've unlocked some great achievements!")

# Handler for the back button
async def go_back(update, context):
    await update.message.reply_text("Returning to main menu...")