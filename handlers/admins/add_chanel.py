from data import get_db
from models.admins import Chanels
from utils.admins import send_admin_message
from middlewares.for_admin import admin_only
from states.add_chanel import NAME, CHANNAL_ID, USERNAME
from telegram.ext import (
    CommandHandler, MessageHandler,
    ConversationHandler, Filters
)

@admin_only
def add_chanel(update, context):
    update.message.reply_text("Iltimos, kanal nomini kiriting:")
    return NAME

def get_chanel_name(update, context):
    context.user_data['chanel_name'] = update.message.text
    update.message.reply_text("Iltimos, kanal ID sini kiriting:")
    return CHANNAL_ID

def get_chanel_id(update, context):
    context.user_data['chanel_id'] = update.message.text
    update.message.reply_text("Iltimos, kanal username sini kiriting:")
    return USERNAME

def get_chanel_username(update, context):
    context.user_data['chanel_username'] = update.message.text

    db = next(get_db())
    new_chanel = Chanels(
        name=context.user_data['chanel_name'],
        channel_id=context.user_data['chanel_id'],
        username=context.user_data['chanel_username']
    )
    db.add(new_chanel)
    db.commit()

    update.message.reply_text("Kanal muvaffaqiyatli qo'shildi!")
    return ConversationHandler.END

def cancel(update, context):
    update.message.reply_text("Bekor qilindi.")
    return ConversationHandler.END

def register_handlers(dp):
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add_channel', add_chanel), MessageHandler(Filters.text('➕ add Channel'), add_chanel)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, get_chanel_name)],
            CHANNAL_ID: [MessageHandler(Filters.text & ~Filters.command, get_chanel_id)],
            USERNAME: [MessageHandler(Filters.text & ~Filters.command, get_chanel_username)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dp.add_handler(conv_handler)