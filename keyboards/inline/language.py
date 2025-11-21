from telegram import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

language_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("English 🇬🇧", callback_data='en')],
    [InlineKeyboardButton("Русский 🇷🇺", callback_data='ru')],
    [InlineKeyboardButton("O'zbekcha 🇺🇿", callback_data='uz')]
])

language_keyboard_s = InlineKeyboardMarkup([
    [InlineKeyboardButton("English 🇬🇧", callback_data='eng')],
    [InlineKeyboardButton("Русский 🇷🇺", callback_data='rus')],
    [InlineKeyboardButton("O'zbekcha 🇺🇿", callback_data='uzb')]
])