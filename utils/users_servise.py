from models.users import User
from models.settings import User_Settings
from data import get_db
def get_user_and_settings(user_id):
    db = next(get_db())
    user = db.query(User).filter(User.telegram_id == user_id).first()
    user_settings = db.query(User_Settings).filter(User_Settings.from_user == user.telegram_id).first() if user else None
    return user, user_settings