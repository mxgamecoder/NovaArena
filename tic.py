from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
import random
from game import handle_tic_tac_toe  # Assuming this imports the correct game menu handling

# Game state storage
games = {}

# Start the game
async def handle_tic_tac_toe_start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    # Initialize the game for the user if it does not exist
    if user_id not in games:
        games[user_id] = {
            'board': [' '] * 9,
            'current_turn': None,
            'symbol': None,
            'ai_symbol': None,
            'game_over': False
        }

    # Create a reply keyboard with symbols for the user to pick
    symbol_keyboard = [['❌', '⭕']]
    reply_markup = ReplyKeyboardMarkup(symbol_keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        "Welcome to Tic-Tac-Toe! Choose your symbol: ❌ or ⭕", 
        reply_markup=reply_markup
    )

# Handle symbol choice
async def handle_symbol_choice(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    
    # Check if the game has started
    if user_id not in games:
        await update.message.reply_text("Please start the game first.")
        return

    user_choice = update.message.text

    if user_choice not in ['❌', '⭕']:
        await update.message.reply_text("Please choose either ❌ or ⭕.")
        return

    games[user_id]['symbol'] = user_choice
    games[user_id]['ai_symbol'] = '❌' if user_choice == '⭕' else '⭕'
    games[user_id]['current_turn'] = 'player'

    await update.message.reply_text(f"You chose {user_choice}. Let’s start the game!")
    
    # Show the board and prompt for the player's move
    await display_board(update, context)

# Display the current board with numbers
async def display_board(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    board = games[user_id]['board']
    
    # Create a display with numbers for player reference
    board_display = f"{board[0] if board[0] != ' ' else 1} | {board[1] if board[1] != ' ' else 2} | {board[2] if board[2] != ' ' else 3}\n" \
                    f"--+---+--\n" \
                    f"{board[3] if board[3] != ' ' else 4} | {board[4] if board[4] != ' ' else 5} | {board[5] if board[5] != ' ' else 6}\n" \
                    f"--+---+--\n" \
                    f"{board[6] if board[6] != ' ' else 7} | {board[7] if board[7] != ' ' else 8} | {board[8] if board[8] != ' ' else 9}"
    
    # Create a keyboard for moves (1-9) and a Back option
    move_keyboard = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9'], ['↩️ Back']]
    reply_markup = ReplyKeyboardMarkup(move_keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(board_display, reply_markup=reply_markup)

# Handle user move
async def handle_tic_tac_toe_move(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    # Check if game has started and not over
    if user_id not in games or games[user_id]['game_over']:
        await update.message.reply_text("The game hasn't started or it's already over. Please start a new game.")
        return

    move = update.message.text

    # Check if the user pressed the back button
    if move == '↩️ Back':
        await update.message.reply_text("Game has not finished; please don't press back yet 😭.")
        return

    if move not in [str(i + 1) for i in range(9)]:
        await update.message.reply_text("Invalid input! Please enter a number between 1 and 9.")
        return

    move = int(move) - 1

    if games[user_id]['board'][move] != ' ':
        await update.message.reply_text("That spot is already taken. Please choose a different number.")
        return

    games[user_id]['board'][move] = games[user_id]['symbol']
    games[user_id]['current_turn'] = 'ai'

    await display_board(update, context)

    if check_winner(games[user_id]['board']):
        games[user_id]['game_over'] = True
        await update.message.reply_text("You win! 🎉")
        await ask_for_new_game(update, context)  # Ask if they want to start a new game
        return

    await ai_move(update, context)

# AI move logic
async def ai_move(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if games[user_id]['game_over']:
        return

    empty_cells = [i for i, cell in enumerate(games[user_id]['board']) if cell == ' ']
    move = random.choice(empty_cells)
    games[user_id]['board'][move] = games[user_id]['ai_symbol']
    games[user_id]['current_turn'] = 'player'

    await display_board(update, context)

    if check_winner(games[user_id]['board']):
        games[user_id]['game_over'] = True
        await update.message.reply_text("AI wins! 🤖")
        await ask_for_new_game(update, context)  # Ask if they want to start a new game
        return

# Check if there’s a winner
def check_winner(board):
    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)              # Diagonals
    ]
    for a, b, c in winning_combinations:
        if board[a] == board[b] == board[c] and board[a] != ' ':
            return True
    return False

# Reset the game state
def reset_game(user_id):
    games[user_id] = {
        'board': [' '] * 9,
        'current_turn': None,
        'symbol': None,
        'ai_symbol': None,
        'game_over': False
    }

# Ask user if they want to start a new game or go back to the main menu
async def ask_for_new_game(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    new_game_keyboard = [['Yes', 'No']]
    reply_markup = ReplyKeyboardMarkup(new_game_keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(
        "Do you want to start a new game? Yes or No.",
        reply_markup=reply_markup
    )

# Handle user's response to new game prompt
async def handle_new_game_response(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    response = update.message.text

    if response == 'Yes':
        await handle_tic_tac_toe_start(update, context)  # Start a new game
    elif response == 'No':
        await back_to_menu(update, context)  # Go back to main menu
    else:
        await update.message.reply_text("Invalid input! Please enter 'Yes' or 'No'.")
        await ask_for_new_game(update, context)  # Ask again if input is invalid


# Handler to go back to the main menu
async def back_to_menu(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    # Check if the game is still ongoing
    if user_id in games and not games[user_id]['game_over']:
        await update.message.reply_text("The game hasn't finished; please don't press back yet 😭.")
        return

    reset_game(user_id)  # Reset the game if over
    await handle_tic_tac_toe(update, context)  # Return to the main menue