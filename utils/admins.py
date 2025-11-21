import logging
from data import get_db
from models.admins import Admins


def get_admins():
    db = next(get_db())
    return db.query(Admins).all()


def on_startup_notify(dp):
    admins = get_admins()
    for admin in admins:
        try:
            dp.bot.send_message(admin.telegram_id, "Bot ishga tushdi")
        except Exception as err:
            logging.exception(err)

def send_admin_message(dp, message):
    admins = get_admins()
    for admin in admins:
        try:
            dp.bot.send_message(admin.telegram_id, message)
        except Exception as err:
            logging.exception(err)