from telegram.ext import Updater
from loader import bot
import handlers
from utils import on_startup_notify
from utils.set_bot_commands import set_default_commands
from models.admins import Admins
from models.users import User
from models.settings import User_Settings
from models.dict import Dict, TOG
from data.database import Base, engine
from data import get_db

def main():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    try:
        db = next(get_db())
        existing_admin = db.query(Admins).filter(Admins.telegram_id == 6295573556).first()
        if not existing_admin:
            new_admin = Admins(
                name = "KhasanOFF",
                telegram_id = 6295573556,
                add_admin = True
            )
            db.add(new_admin)
            db.commit()
        db.close()
    except Exception as e:
        print(f"Admin qo'shishda xato: {e}")
    
    updater = Updater(bot.token, use_context=True)
    dp = updater.dispatcher

    set_default_commands(dp)
    on_startup_notify(dp)

    handlers.register_handlers(dp)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
