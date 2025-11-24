# pip imports
from telegram import ReplyKeyboardMarkup, KeyboardButton

def get_menu_keyboard(lang: str) -> ReplyKeyboardMarkup:
     if lang == "en":
         return ReplyKeyboardMarkup(
             [
                 [KeyboardButton("Dictionary 📚"), KeyboardButton("Search 🔎")],
                 [KeyboardButton("Translator 🌍")],
                 [KeyboardButton("Settings ⚙️"), KeyboardButton("Help ❓")],
             ],
             resize_keyboard=True
         )
     elif lang == "ru":
         return ReplyKeyboardMarkup(
             [
                 [KeyboardButton("Словарь 📚"), KeyboardButton("Поиск 🔎")],
                 [KeyboardButton("Переводчик 🌍")],
                 [KeyboardButton("Настройки ⚙️"), KeyboardButton("Помощь ❓")],
             ],
             resize_keyboard=True
         )
     else:  # default to Uzbek
         return ReplyKeyboardMarkup(
             [
                 [KeyboardButton("Lug'at 📚"), KeyboardButton("Qidirish 🔎")],
                 [KeyboardButton("Tarjimon 🌍")],
                 [KeyboardButton("Sozlamalar ⚙️"), KeyboardButton("Yordam ❓")],
             ],
             resize_keyboard=True
         )
