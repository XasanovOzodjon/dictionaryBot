# pip imports
from telegram.ext import CommandHandler, MessageHandler, Filters

# local imports
from utils.users_servise import UserUpdate
from middlewares.check_subscribe import subscription_required

@subscription_required
def games_home(update, context):
    if not context.user_data:
        UserUpdate(update, context)
    if 'language' not in context.user_data:
        update.message.reply_text("Please start the bot using /start command.")
        return

    lang = context.user_data['language']
    if lang == 'ru':
        text = "Добро пожаловать в раздел игр!"
    elif lang == 'en':
        text = "Welcome to the games section!"
    else:
        text = "O'yinlar bo'limiga xush kelibsiz!"

    update.message.reply_text(text)

def register_handlers(dp):
    dp.add_handler(CommandHandler("games", games_home))
    dp.add_handler(MessageHandler(Filters.text(["🎮 O'yinlar", "🎮 Игры", "🎮 Games"]), games_home))