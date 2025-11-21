from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from utils.misc.languages import languages
from models.settings import User_Settings

def get_settings_keyboard(user_settings: User_Settings) -> InlineKeyboardMarkup:
    
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
    
    if user_settings.use_TOG:
        tog_status = "✅"
        change_tog = "disable_tog"
    else:
        tog_status = "❌"
        change_tog = "enable_tog"
    
    if user_settings.ai_assistant:
        ai_status = "✅"
        change_ai = "disable_ai"
    else:
        ai_status = "❌"
        change_ai = "enable_ai"
    
    
    
    if user_settings.language == 'en':
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("Language:", callback_data='None'), InlineKeyboardButton("🇬🇧", callback_data='change_lang')],
            [InlineKeyboardButton(f"{lang_button}", callback_data='change_from'), InlineKeyboardButton("< - >", callback_data='change_toto'), InlineKeyboardButton(f"{to_lang_button}", callback_data='change_to')],
            [InlineKeyboardButton("TOG method:", callback_data='None'), InlineKeyboardButton(f"{tog_status}", callback_data=f'{change_tog}')],
            [InlineKeyboardButton("AI assistant:", callback_data='None'), InlineKeyboardButton(f"{ai_status}", callback_data=f'{change_ai}')],
            [InlineKeyboardButton("Close Settings", callback_data='close_settings')]
        ])
    elif user_settings.language == 'ru':
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("Язык:", callback_data='None'), InlineKeyboardButton("🇷🇺", callback_data='change_lang')],
            [InlineKeyboardButton(f"{lang_button}", callback_data='change_from'), InlineKeyboardButton("< - >", callback_data='change_toto'), InlineKeyboardButton(f"{to_lang_button}", callback_data='change_to')],
            [InlineKeyboardButton("Метод TOG", callback_data='None'), InlineKeyboardButton(f"{tog_status}", callback_data=f'{change_tog}')],
            [InlineKeyboardButton("ИИ-помощник", callback_data='None'), InlineKeyboardButton(f"{ai_status}", callback_data=f'{change_ai}')],
            [InlineKeyboardButton("Настройки закрыть", callback_data='close_settings')]
        ])
    else:  # Uzbek
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("Til:", callback_data='None'), InlineKeyboardButton("🇺🇿", callback_data='change_lang')],
            [InlineKeyboardButton(f"{lang_button}", callback_data='change_from'), InlineKeyboardButton("< - >", callback_data='change_toto'), InlineKeyboardButton(f"{to_lang_button}", callback_data='change_to')],
            [InlineKeyboardButton("TOG usuli:", callback_data='None'), InlineKeyboardButton(f"{tog_status}", callback_data=f'{change_tog}')],
            [InlineKeyboardButton("Ai yordamchi:", callback_data='None'), InlineKeyboardButton(f"{ai_status}", callback_data=f'{change_ai}')],
            [InlineKeyboardButton("Sozlamalarni yopish", callback_data='close_settings')]
        ])