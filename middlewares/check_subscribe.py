# standard imports
from functools import wraps

# pip imports
from telegram.error import TelegramError
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# local imports
from data import get_db
from models.admins import Chanels

def check_subscribe(update, context):
    user = update.effective_user
    msg = update.effective_message

    if not user:
        return False

    db = next(get_db())
    channels = db.query(Chanels).all()
    not_subscribed = []
    
    for channel in channels:
        try:
            member = context.bot.get_chat_member(channel.channel_id, user.id)
            status = member.status.lower()
            if status not in ("creator", "administrator", "member", "restricted"):
                not_subscribed.append(channel)
        except TelegramError:
            # send_admin_message(context, f"ERROR: Bot is not a member of the channel {channel.name} ({channel.channel_id}).")
            not_subscribed.append(channel)  # Agar bot kanalda a'zo bo'lmasa, foydalanuvchi ham a'zo emas deb hisoblaymiz
            
    if not_subscribed:
        buttons = []
        for channel in not_subscribed:
            # Agar username mavjud bo'lsa, link yaratamiz
            if hasattr(channel, 'username') and channel.username:
                url = f"https://t.me/{channel.username.lstrip('@')}"
                join_button = InlineKeyboardButton(
                    text=f"Obuna bo'ling: {channel.name}",
                    url=url
                )
                buttons.append([join_button])
        
        if buttons:
            keyboard = InlineKeyboardMarkup(buttons)
            msg.reply_text(
                "Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:\n",
                reply_markup=keyboard
            )
        else:
            msg.reply_text("Obuna bo'lish kerak bo'lgan kanallar mavjud, lekin havolalar topilmadi.")
        return False
    else:
        return True


def subscription_required(func):
    """Decorator to check subscription before executing handler"""
    @wraps(func)
    def wrapper(update, context, *args, **kwargs):
        if not check_subscribe(update, context):
            return 
        return func(update, context, *args, **kwargs)
    return wrapper
        
            
            
