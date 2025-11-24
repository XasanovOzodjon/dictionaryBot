from . import errors
from . import groups
from .admins import add_chanel
from .errors.error_handler import error_handler
from .users import start, help, settings, transletor, dicts, add_one, add_multe, games_main, ai


def register_handlers(dp):
    dp.add_error_handler(error_handler)
    start.register_handlers(dp)  
    add_chanel.register_handlers(dp)
    help.register_handlers(dp)
    settings.register_handlers(dp)
    transletor.register_handlers(dp)
    dicts.register_handlers(dp)
    add_one.register_handlers(dp)
    add_multe.register_handlers(dp)
    games_main.register_handlers(dp)
    ai.register_handlers(dp)