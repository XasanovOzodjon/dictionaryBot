# pip imports
from telegram import Update

# local imports
from data import get_db
from models.users import User
from models.settings import User_Settings

def get_user_and_settings(user_id):
    with next(get_db()) as db:
        user = db.query(User).filter(User.telegram_id == user_id).first()
        user_settings = db.query(User_Settings).filter(User_Settings.from_user == user.telegram_id).first() if user else None
    return user, user_settings

def get_settings(user_id):
    with next(get_db()) as db:
        user_settings = db.query(User_Settings).filter(User_Settings.from_user == user_id).first()
    return user_settings

def UserUpdate(update: Update, context):
    with next(get_db()) as db:
        user = db.query(User).filter(User.telegram_id == update.effective_user.id).first()
        user_settings = db.query(User_Settings).filter(User_Settings.from_user == update.effective_user.id).first()
        if user:
            context.user_data['first_name'] = user.first_name
            context.user_data['last_name'] = user.last_name
            context.user_data['telegram_id'] = user.telegram_id
            if user_settings:
                context.user_data['language'] = user_settings.language
                context.user_data['settings_id'] = user_settings.id
                context.user_data['use_tog'] = user_settings.use_TOG
                context.user_data['translate_from'] = user_settings.translate_from
                context.user_data['translate_to'] = user_settings.translate_to
                context.user_data['ai_assistant'] = user_settings.ai_assistant
            