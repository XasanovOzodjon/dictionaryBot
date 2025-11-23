from . import errors
from .users import start, help, echo, settings, transletor, dicts, add_one
from . import groups
from .admins import add_chanel
from .errors.error_handler import error_handler

def register_handlers(dp):
    # Error handler qo'shish
    dp.add_error_handler(error_handler)
    
    # Register start first to ensure it has priority
    start.register_handlers(dp)
    
    add_chanel.register_handlers(dp)
    help.register_handlers(dp)
    settings.register_handlers(dp)
    transletor.register_handlers(dp)
    dicts.register_handlers(dp)
    add_one.register_handlers(dp)
