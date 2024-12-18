import logging
import time
import asyncio  # Add asyncio for non-blocking sleep
from telegram import Update
from telegram.ext import CallbackContext, Application

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Store active games and users
active_games = {}
waiting_for_game = False  # Flag to indicate if waiting for a game

def notify_users(username, user_id, context: CallbackContext):
    for player_id, player_name in active_games.items():
        if player_id != user_id:
            player_message = f"{username} has joined the game! 🎉"
            asyncio.create_task(context.bot.send_message(chat_id=player_id, text=player_message))

async def countdown_timer(context: CallbackContext, time_limit: int):
    for remaining in range(time_limit, 0, -1):
        for player_id in active_games.keys():
            await context.bot.send_message(chat_id=player_id, text=f"⏳ Waiting for another player to join... {remaining} seconds remaining.")
        await asyncio.sleep(1)

async def waiting_for_players(context: CallbackContext):
    time_limit = 10  # seconds
    await countdown_timer(context, time_limit)

    # Check if two players have joined after the countdown
    return len(active_games) == 2

async def join_game(update: Update, context: CallbackContext) -> None:
    global waiting_for_game
    user_id = update.message.from_user.id
    username = update.message.from_user.username or "Player"

    if user_id in active_games:
        await update.message.reply_text("You are already in a game!")
        return

    active_games[user_id] = username
    await update.message.reply_text(f"{username}, waiting for another player to join... ⏳")

    if waiting_for_game:
        # If already waiting for players, notify them
        notify_users(username, user_id, context)
    else:
        waiting_for_game = True  # Set flag to indicate waiting for a game
        if await waiting_for_players(context):
            await start_game(context)
        else:
            del active_games[user_id]
            waiting_for_game = False  # Reset flag
            await update.message.reply_text("No players online. Game cancelled. ❌")

async def start_game(context: CallbackContext):
    global waiting_for_game
    waiting_for_game = False  # Reset the waiting flag
    player_list = list(active_games.items())
    player1_id, player1_name = player_list[0]
    player2_id, player2_name = player_list[1]

    # Notify both players that the game is starting
    await context.bot.send_message(chat_id=player1_id, text=f"The game has started! 🎮\nPlayers: {player1_name} vs {player2_name}")
    await context.bot.send_message(chat_id=player2_id, text=f"The game has started! 🎮\nPlayers: {player1_name} vs {player2_name}")

async def leave_game(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id in active_games:
        del active_games[user_id]
        await update.message.reply_text("You have left the game. 👋")
    else:
        await update.message.reply_text("You are not in any game.")