from telegram import ReplyKeyboardMarkup, KeyboardButton

def get_dict_keyboard(lang: str) -> ReplyKeyboardMarkup:
     if lang == "en":
         return ReplyKeyboardMarkup(
             [
                 [KeyboardButton("📚 My Dicts"), KeyboardButton("➕ Add dict")],
                 [KeyboardButton("🎮 Games")],
                 [KeyboardButton("🔙 Back")],
             ],
             resize_keyboard=True
         )
     elif lang == "ru":
         return ReplyKeyboardMarkup(
             [
                 [KeyboardButton("📚 Мои словари"), KeyboardButton("➕ Добавить словарь")],
                 [KeyboardButton("🎮 Игры")],
                 [KeyboardButton("🔙 Назад")],
             ],
             resize_keyboard=True
         )
     else:  # default to Uzbek
         return ReplyKeyboardMarkup(
             [
                 [KeyboardButton("📚 Mening lug'atlarim"), KeyboardButton("➕ Lug'at qo'shish")],
                 [KeyboardButton("🎮 O'yinlar")],
                 [KeyboardButton("🔙 Orqaga")],
             ],
             resize_keyboard=True
         )

def get_add_dict_keyboard(lang: str) -> ReplyKeyboardMarkup:
    if lang == "en":
        return ReplyKeyboardMarkup(
            [
                [KeyboardButton("➕ Add One Dict"), KeyboardButton("➕ Add Multiple Dicts")],
                [KeyboardButton("🔙 Back to Dictionary")],
            ],
            resize_keyboard=True
        )
    elif lang == "ru":
        return ReplyKeyboardMarkup(
            [
                [KeyboardButton("➕ Добавить один словарь"), KeyboardButton("➕ Добавить несколько словарей")],
                [KeyboardButton("🔙 Назад к словарю")],
            ],
            resize_keyboard=True
        )
    else:  # default to Uzbek
        return ReplyKeyboardMarkup(
            [
                [KeyboardButton("➕ Bitta lug'at qo'shish"), KeyboardButton("➕ Bir nechta lug'at qo'shish")],
                [KeyboardButton("🔙 Orqaga lug'atga")],
            ],
            resize_keyboard=True
        )