from telegram.ext import CommandHandler, MessageHandler, Filters
from middlewares.check_subscribe import subscription_required
from utils.users_servise import get_user_and_settings

@subscription_required
def games_home(update, context):
    user, user_settings = get_user_and_settings(update.effective_user.id)
    if user_settings.language == 'ru':
        text = "Добро пожаловать в раздел игр!"
    elif user_settings.language == 'en':
        text = "Welcome to the games section!"
    else:
        text = "O'yinlar bo'limiga xush kelibsiz!"

    update.message.reply_text(text)

def register_handlers(dp):
    dp.add_handler(CommandHandler("games", games_home))
    dp.add_handler(MessageHandler(Filters.text(["🎮 O'yinlar", "🎮 Игры", "🎮 Games"]), games_home))