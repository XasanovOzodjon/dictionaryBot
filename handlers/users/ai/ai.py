# pip imports
from telegram.ext import MessageHandler, Filters

# local imports
from middlewares.check_subscribe import subscription_required

@subscription_required
def bot_ai(update, context):
    update.message.reply_text("ai not working...")

def register_handlers(dp):
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, bot_ai))