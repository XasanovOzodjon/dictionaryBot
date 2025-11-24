# standard imports
from functools import wraps

# local imports
from data import get_db
from models.admins import Admins

def admin_only(func):
    @wraps(func)
    def wrapper(update, context, *args, **kwargs):
        db = next(get_db())
        telegram_id = update.effective_user.id
        admin = db.query(Admins).filter(Admins.telegram_id == telegram_id).first()
        if admin is None:
            update.message.reply_text("Siz admin emassiz.")
            return
        return func(update, context, *args, **kwargs)
    return wrapper
