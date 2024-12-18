from telegram import ReplyKeyboardMarkup

async def show_task_menu(update, context):
    # Define the task menu with a back option
    task_keyboard = [
        ['📝 Create Task', '✅ Complete Task'],
        ['📅 View Tasks', '🔄 Edit Task'],
        ['🔙 Back']
    ]
    
    # Send the task list as a message with a keyboard
    await update.message.reply_text(
        "🛠️ *Task Menu*:\nChoose an action to manage your tasks:",
        reply_markup=ReplyKeyboardMarkup(task_keyboard, resize_keyboard=True)
    )