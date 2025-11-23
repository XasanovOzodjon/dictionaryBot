from telegram.ext import MessageHandler, Filters, CommandHandler
from middlewares.check_subscribe import subscription_required
from keyboards.default.dict import get_dict_keyboard, get_add_dict_keyboard
from utils.users_servise import get_user_and_settings

@subscription_required
def dict_menu(update, context):
    user, user_settings = get_user_and_settings(update.effective_user.id)
    
    if not user:
        update.message.reply_text("Please start the bot using /start command.")
        return
    
    if user_settings.language == "en":
        text = "Dictionary Menu📚"
    elif user_settings.language == "ru":
        text = "Меню словаря📚"
    else:  # default to Uzbek
        text = "Lug'at menu📚"
        
    update.message.reply_text(text, reply_markup=get_dict_keyboard(user_settings.language))

def add_dict_handler(update, context):
    user, user_settings = get_user_and_settings(update.effective_user.id)
    
    if not user:
        update.message.reply_text("Please start the bot using /start command.")
        return
    
    if user_settings.language == "en":
        text = "➕ Add dictionary"
    elif user_settings.language == "ru":
        text = "➕ Добавить словарь"
    else:  # default to Uzbek
        text = "➕ Lug'at qo'shish"
        
    update.message.reply_text(text, reply_markup=get_add_dict_keyboard(user_settings.language))
    
def register_handlers(dp):
    dp.add_handler(MessageHandler(Filters.text(['Dictionary 📚', 'Словарь 📚', "Lug'at 📚"]), dict_menu))
    dp.add_handler(CommandHandler('dictionary', dict_menu))
    dp.add_handler(MessageHandler(Filters.text(['🔙 Back to Dictionary', '🔙 Назад к словарю', "🔙 Orqaga lug'atga"]), dict_menu))

    dp.add_handler(MessageHandler(Filters.text(['➕ Add dictionary', '➕ Добавить словарь', "➕ Lug'at qo'shish"]), add_dict_handler))