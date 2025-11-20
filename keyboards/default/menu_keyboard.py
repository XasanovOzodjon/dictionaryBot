from telegram import ReplyKeyboardMarkup, KeyboardButton

menu_keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton("Dictionary 📚"), KeyboardButton("Search 🔎")],
        [KeyboardButton("Translations 🌐")],
        [KeyboardButton("Settings ⚙️"), KeyboardButton("Help ❓")],
    ],
    resize_keyboard=True
)
