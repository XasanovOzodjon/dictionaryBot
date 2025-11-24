# pip imports
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, MessageHandler, Filters

# local imports
from middlewares.check_subscribe import subscription_required

@subscription_required
def bot_help(update, context):
    text = (
        "Buyruqlar: ",
        "/start - Botni ishga tushirish",
        "/help - Yordam"
    )
    admin_keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Contact Admin", url="https://t.me/Xasanov_Ozodjon")]
        ]
    )
    update.message.reply_text(
        "\n".join(text),
        reply_markup=admin_keyboard

        )

def register_handlers(dp):
    dp.add_handler(CommandHandler("help", bot_help))
    dp.add_handler(MessageHandler(Filters.text(["Help ❓", "Помощь ❓", "Yordam ❓"]), bot_help))