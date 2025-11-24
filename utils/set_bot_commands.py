# pip imports
from telegram import BotCommand


def set_default_commands(dp):
    dp.bot.set_my_commands(
        [
            BotCommand("start", "Botni ishga tushurish"),
            BotCommand("help", "Yordam"),
            BotCommand("settings", "Sozlamalar"),
            BotCommand("translator", "Tarjimon"),
            BotCommand("dictionary", "Lug'at"),
        ]
    )
