# pip imports
from telegram.ext import MessageHandler, Filters, CommandHandler

# local imports
from utils.users_servise import UserUpdate
from middlewares.check_subscribe import subscription_required
from keyboards.default.dict import get_dict_keyboard, get_add_dict_keyboard


@subscription_required
def dict_menu(update, context):
    if not context.user_data:
        UserUpdate(update, context)
    if 'language' not in context.user_data:
        update.message.reply_text("Please start the bot using /start command.")
        return
    lang = context.user_data.get('language')

    if lang == "en":
        text = "Dictionary Menu📚"
    elif lang == "ru":
        text = "Меню словаря📚"
    else:  # default to Uzbek
        text = "Lug'at menu📚"

    update.message.reply_text(text, reply_markup=get_dict_keyboard(lang))

def add_dict_handler(update, context):
    if not context.user_data:
        UserUpdate(update, context)
    if 'language' not in context.user_data:
        update.message.reply_text("Please start the bot using /start command.")
        return
    lang = context.user_data.get('language')

    if lang == "en":
        text = "➕ Add dictionary"
    elif lang == "ru":
        text = "➕ Добавить словарь"
    else:  # default to Uzbek
        text = "➕ Lug'at qo'shish"

    update.message.reply_text(text, reply_markup=get_add_dict_keyboard(lang))

def register_handlers(dp):
    dp.add_handler(MessageHandler(Filters.text(['Dictionary 📚', 'Словарь 📚', "Lug'at 📚"]), dict_menu))
    dp.add_handler(CommandHandler('dictionary', dict_menu))
    dp.add_handler(MessageHandler(Filters.text(['🔙 Back to Dictionary', '🔙 Назад к словарю', "🔙 Orqaga lug'atga"]), dict_menu))

    dp.add_handler(MessageHandler(Filters.text(['➕ Add dictionary', '➕ Добавить словарь', "➕ Lug'at qo'shish"]), add_dict_handler))