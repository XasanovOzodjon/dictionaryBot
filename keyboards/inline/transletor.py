from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from utils.misc.languages import languages
from models.settings import User_Settings

def get_transletor_keyborad(user_settings: User_Settings) -> InlineKeyboardMarkup:
    
    if user_settings.translate_from == 'auto':
        lang_button = 'Auto 🌐'
    else:
        lang_button = 'Unknown'  # Default value
        for key, value in languages.items():
            if value == user_settings.translate_from:
                lang_button = key
                break
    
    to_lang_button = 'Unknown'  # Default value
    for key, value in languages.items():
        if value == user_settings.translate_to:
            to_lang_button = key
            break
        
    if user_settings.language == 'en':
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{lang_button}", callback_data='change_from'), InlineKeyboardButton("< - >", callback_data='change_toto'), InlineKeyboardButton(f"{to_lang_button}", callback_data='change_to')],
            [InlineKeyboardButton("Close", callback_data='close_transletor')]
        ])
    elif user_settings.language == 'ru':
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{lang_button}", callback_data='change_from'), InlineKeyboardButton("< - >", callback_data='change_toto'), InlineKeyboardButton(f"{to_lang_button}", callback_data='change_to')],
            [InlineKeyboardButton("Закрыть", callback_data='close_transletor')]
        ])
    else:  # Uzbek
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{lang_button}", callback_data='change_from'), InlineKeyboardButton("< - >", callback_data='change_toto'), InlineKeyboardButton(f"{to_lang_button}", callback_data='change_to')],
            [InlineKeyboardButton("Yopish", callback_data='close_transletor')]
        ])