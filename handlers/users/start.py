from telegram.ext import CommandHandler
from middlewares.check_subscribe import subscription_required
from keyboards.default.menu_keyboard import menu_keyboard

@subscription_required
def bot_start(update, context):
    update.message.reply_text(f"Salom, {update.effective_user.full_name}!", reply_markup=menu_keyboard)

def register_handlers(dp):
    dp.add_handler(CommandHandler("start", bot_start))