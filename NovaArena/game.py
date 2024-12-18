from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext

async def show_game_menu(update, context):
    # Define a list of mini-games with emojis
    games = [
        '❌⭕ Tic Tac Toe', 
        '♟️ Chess Duel', 
        '🎯 Dart Master', 
        '🎲 Dice Roll Battle', 
        '⚽ Penalty Shootout',
        '🏎️ Racing Challenge', 
        '👾 Space Invaders', 
        '🧩 Puzzle Solver', 
        '🎳 Bowling Strike', 
        '🏹 Archery Championship',
        '🧠 Memory Challenge', 
        '🃏 Card Game Duel'
    ]
    
    # Create the game menu with a back option
    game_keyboard = [
        [games[0], games[1], games[2]],
        [games[3], games[4], games[5]],
        [games[6], games[7], games[8]],
        [games[9], games[10], games[11]],
        ['🔙 Back']
    ]
    
    # Send the game list as a message with a keyboard
    await update.message.reply_text(
        "🎮 *Choose a Game*:\nSelect a game to play:",
        reply_markup=ReplyKeyboardMarkup(game_keyboard, resize_keyboard=True)
    )

# Handler to go back to the main menu
async def back_to_menu(update: Update, context: CallbackContext) -> None:
    await show_game_menu(update, context)


async def handle_card_game_duel(update, context):
    story_text = (
        "🃏 Welcome to *Card Game Duel*! 🃏\n"
        "Play your cards in different modes:\n"
        "1️⃣ Play against the *AI* 🤖\n"
        "2️⃣ Challenge your *Online Friend* 🌐\n"
        "3️⃣ Challenge a *Friend* 🧑‍🤝‍🧑\n"
        "4️⃣ Practice in *Training Mode* 🏋️‍♂️"
    )
    
    card_game_keyboard = [
        ['🧿 AI', '😁 Online Friend'],  # 2 items
        ['🤗 Friend', '😏 Training'],  # 2 items
        ['Back 🔙']  # 1 item
    ]
    
    await update.message.reply_text(
        story_text,
        reply_markup=ReplyKeyboardMarkup(card_game_keyboard, resize_keyboard=True)
    )

async def handle_space_invaders(update, context):
    story_text = (
        "👾 Welcome to *Space Invaders*! 👾\n"
        "You can fight against:\n"
        "1️⃣ Play against the *AI* 🤖\n"
        "2️⃣ Fight with your *Online Friend* 🌐\n"
        "3️⃣ Fight alongside a *Friend* 🧑‍🤝‍🧑\n"
        "4️⃣ Practice in *Training Mode* 🏋️‍♂️"
    )
    
    space_invaders_keyboard = [
        ['🙄 AI', '🥴 Online Friend'],  # 2 items
        ['😎 Friend', '😟 Training'],  # 2 items
        ['Back 🔙']  # 1 item
    ]
    
    await update.message.reply_text(
        story_text,
        reply_markup=ReplyKeyboardMarkup(space_invaders_keyboard, resize_keyboard=True)
    )

async def handle_puzzle_solver(update, context):
    story_text = (
        "🧩 Welcome to *Puzzle Solver*! 🧩\n"
        "Challenge your brain in:\n"
        "1️⃣ Play against the *AI* 🤖\n"
        "2️⃣ Solve puzzles with your *Online Friend* 🌐\n"
        "3️⃣ Solve puzzles with a *Friend* 🧑‍🤝‍🧑\n"
        "4️⃣ Practice in *Puzzle Mode* 🧠"
    )
    
    puzzle_solver_keyboard = [
        ['🧠 Puzzle AI', '✈️ Online'],  # 2 items
        ['☹️ Friend', '🧠 Puzzle Mode'],  # 2 items
        ['Back 🔙']  # 1 item
    ]
    
    await update.message.reply_text(
        story_text,
        reply_markup=ReplyKeyboardMarkup(puzzle_solver_keyboard, resize_keyboard=True)
    )

async def handle_bowling_strike(update, context):
    story_text = (
        "🎳 Welcome to *Bowling Strike*! 🎳\n"
        "Choose how you'd like to play:\n"
        "1️⃣ Bowl against the *Champion AI* 🎯\n"
        "2️⃣ Challenge your *Online Rival* 🌍\n"
        "3️⃣ Bowl with a *Local Friend* 👫\n"
        "4️⃣ Practice your skills in *Bowling Drills* 🎳"
    )
    
    bowling_keyboard = [
        ['🎯 Champion AI', '🌍 Online Rival'],  # Updated labels and emojis
        ['🥳 Friend', '🎳 Bowling Drills'],  # Updated labels and emojis
        ['Back 🔙']  # "Back" button remains unchanged
    ]
    
    await update.message.reply_text(
        story_text,
        reply_markup=ReplyKeyboardMarkup(bowling_keyboard, resize_keyboard=True)
    )

async def handle_memory_challenge(update, context):
    story_text = (
        "🧠 Welcome to *Memory Challenge*! 🧠\n"
        "Train your memory in different modes:\n"
        "1️⃣ Test your skills against the *Memory Master AI* 🧠\n"
        "2️⃣ Play with your *Online Challenger* 🌍\n"
        "3️⃣ Challenge a *Local Friend* 👫\n"
        "4️⃣ Hone your skills in *Memory Training* 📚"
    )
    
    memory_challenge_keyboard = [
        ['🧠 Memory Master AI', '🌍 Online Challenger'],  # Updated labels and emojis
        ['🛴 Bot', '📚 Memory Training'],  # Updated labels and emojis
        ['Back 🔙']  # "Back" button remains unchanged
    ]
    
    await update.message.reply_text(
        story_text,
        reply_markup=ReplyKeyboardMarkup(memory_challenge_keyboard, resize_keyboard=True)
    )
    
async def handle_archery_championship(update, context):
    story_text = (
        "🏹 Welcome to *Archery Championship*! 🏹\n"
        "Choose how to compete:\n"
        "1️⃣ Compete against the *Sharpshooter AI* 🎯\n"
        "2️⃣ Challenge your *Online Rival* 🌍\n"
        "3️⃣ Compete with a *Local Friend* 👫\n"
        "4️⃣ Practice your aim in *Skill Development* 🏹"
    )
    
    archery_keyboard = [
        ['🎯 Sharpshooter AI', '🌍 Online Rival'],  # Updated labels and emojis
        ['👫 Local Friend', '🏹 Skill Development'],  # Updated labels and emojis
        ['Back 🔙']  # "Back" button remains unchanged
    ]
    
    await update.message.reply_text(
        story_text,
        reply_markup=ReplyKeyboardMarkup(archery_keyboard, resize_keyboard=True)
    )
async def handle_racing_challenge(update, context):
    story_text = (
        "🏎️ Welcome to *Racing Challenge*! 🏎️\n"
        "Choose your race mode:\n"
        "1️⃣ Race against the *AI* 🤖\n"
        "2️⃣ Challenge your *Online Friend* 🌐\n"
        "3️⃣ Race with a *Friend* 🧑‍🤝‍🧑\n"
        "4️⃣ Practice in *Training Mode* 🏋️‍♂️"
    )
    
    racing_keyboard = [
        ['🏎️ Computer', '🌐 Online'],  # 2 items
        ['🫂 Friend', '🏋️‍♂️ Tutorial'],  # 2 items
        ['Back 🔙']  # 1 item
    ]
    
    await update.message.reply_text(
        story_text,
        reply_markup=ReplyKeyboardMarkup(racing_keyboard, resize_keyboard=True)
    )

async def handle_chess_duel(update, context):
    story_text = (
        "♟️ Welcome to *Chess Duel*! ♟️\n"
        "Sharpen your mind with these game modes:\n"
        "1️⃣ Play against the *AI* 🎓\n"
        "2️⃣ Challenge your *Online Friend* 🌍\n"
        "3️⃣ Challenge a *Local Friend* 👤\n"
        "4️⃣ Practice your moves in *Strategy Session* 📚"
    )
    
    chess_keyboard = [
        ['🎓 AI', '🌍 Online Friends'],  # Updated emojis
        ['👤 Local Friends', '📚 Strategy Session'],  # Updated labels and emojis
        ['Back 🔙']  # "Back" button remains unchanged
    ]
    
    await update.message.reply_text(
        story_text,
        reply_markup=ReplyKeyboardMarkup(chess_keyboard, resize_keyboard=True)
    )

async def handle_dice_roll(update, context):
    story_text = (
        "🎲 Welcome to *Dice Roll Battle*! 🎲\n"
        "You can play in three exciting modes:\n"
        "1️⃣ Play against the *Computer* 🎮\n"
        "2️⃣ Challenge an *Online Friend* 🌍\n"
        "3️⃣ Challenge a *Local Friend* 👤\n\n"
        "Roll the dice and test your luck! 🍀"
    )
    
    dice_roll_keyboard = [
        ['🎮 Computer', '🌍 Online Friend'],  # Updated emojis
        ['👤 Local Friend', '🔄 Roll Dice'],  # New button for rolling dice
        ['Back 🔙']  # "Back" button remains unchanged
    ]
    
    await update.message.reply_text(
        story_text,
        reply_markup=ReplyKeyboardMarkup(dice_roll_keyboard, resize_keyboard=True)
    )

async def handle_dart_master(update, context):
    story_text = (
        "🎯 Welcome to *Dart Master*! 🎯\n"
        "Choose your mode to play:\n"
        "1️⃣ Play against the *AI* 🤖\n"
        "2️⃣ Challenge your *Online Friend* 🌐\n"
        "3️⃣ Challenge a *Friend* 🧑‍🤝‍🧑\n"
        "4️⃣ Practice in *Training Mode* 🏋️‍♂️"
    )
    
    # Create a reply keyboard with updated emoji
    dart_master_keyboard = [
        ['🎮 AI', '🌍 Online Friend'],  # Updated emojis
        ['👥 Friend', '📚 Training'],  # Updated emojis
        ['Back 🔙 ']  # Updated emoji for 'Back'
    ]
    await update.message.reply_text(
        story_text,
        reply_markup=ReplyKeyboardMarkup(dart_master_keyboard, resize_keyboard=True)
    )

async def handle_tic_tac_toe(update, context):
    story_text = (
        "❌⭕ Welcome to *Tic Tac Toe*! ❌⭕\n"
        "Choose your opponent:\n"
        "1️⃣ Play against the *AI* 🤖\n"
        "2️⃣ Challenge your *Online Friend* 🌐\n"
        "3️⃣ Challenge a *Friend* 🧑‍🤝‍🧑\n"
        "4️⃣ Practice in *Training Mode* 🏋️‍♂️"
    )
    
    tic_tac_toe_keyboard = [
        ['🤖 AI', '🌐 Online Friend'],  # 2 items
        ['🧑‍🤝‍🧑 Friend', '🏋️‍♂️ Training'],  # 2 items
        ['Back 🔙']  # 1 item
    ]
    
    await update.message.reply_text(
        story_text,
        reply_markup=ReplyKeyboardMarkup(tic_tac_toe_keyboard, resize_keyboard=True)
    )

async def handle_penalty_shootout(update, context):
    story_text = (
        "⚽ Welcome to *Penalty Shootout*! ⚽\n"
        "Choose how you'd like to play:\n"
        "1️⃣ Play against the *AI Goalkeeper* 🤖\n"
        "2️⃣ Challenge your *Online Friend* 🌐\n"
        "3️⃣ Challenge a *Friend* 🧑‍🤝‍🧑\n"
        "4️⃣ Practice your shots in *Training Mode* 🏋️‍♂️"
    )
    
    penalty_shootout_keyboard = [
        ['🤖 AI Goalkeeper', '⚽ Online'],  # 2 items
        ['🏆 Friend', '🧑‍💻 Training'],  # 2 items
        ['Back 🔙']  # 1 item
    ]
    
    await update.message.reply_text(
        story_text,
        reply_markup=ReplyKeyboardMarkup(penalty_shootout_keyboard, resize_keyboard=True)
    )

