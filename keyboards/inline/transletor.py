# pip imports
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# local imports
from utils.misc.languages import languages

def get_transletor_keyborad(t_from, t_to, lang) -> InlineKeyboardMarkup:

    if t_from == 'auto':
        lang_button = 'Auto 🌐'
    else:
        lang_button = 'Unknown'
        for key, value in languages.items():
            if value == t_from:
                lang_button = key
                break
    
    to_lang_button = 'Unknown'
    for key, value in languages.items():
        if value == t_to:
            to_lang_button = key
            break

    if lang == 'en':
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{lang_button}", callback_data='change_from'), InlineKeyboardButton("< - >", callback_data='change_toto'), InlineKeyboardButton(f"{to_lang_button}", callback_data='change_to')],
            [InlineKeyboardButton("Close", callback_data='close_transletor')]
        ])
    elif lang == 'ru':
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{lang_button}", callback_data='change_from'), InlineKeyboardButton("< - >", callback_data='change_toto'), InlineKeyboardButton(f"{to_lang_button}", callback_data='change_to')],
            [InlineKeyboardButton("Закрыть", callback_data='close_transletor')]
        ])
    else:
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{lang_button}", callback_data='change_from'), InlineKeyboardButton("< - >", callback_data='change_toto'), InlineKeyboardButton(f"{to_lang_button}", callback_data='change_to')],
            [InlineKeyboardButton("Yopish", callback_data='close_transletor')]
        ])