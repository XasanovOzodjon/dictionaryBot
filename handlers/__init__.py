from . import errors
from .users import start, help, echo, settings
from . import groups
from .admins import add_chanel
from .errors.error_handler import error_handler

def register_handlers(dp):
    # Error handler qo'shish
    dp.add_error_handler(error_handler)
    
    add_chanel.register_handlers(dp)
    start.register_handlers(dp)
    help.register_handlers(dp)
    settings.register_handlers(dp)
    # echo.register_handlers(dp)
