# pip imports
from telegram.ext import Updater

# local imports
import handlers
from loader import bot
from data import get_db
from models.users import User
from models.admins import Admins
from models.dict import Dict, TOG
from utils import on_startup_notify
from data.database import Base, engine
from models.settings import User_Settings
from utils.set_bot_commands import set_default_commands

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
