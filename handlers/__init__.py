from . import errors
from .users import start, help, echo
from . import groups
from .admins import add_chanel

def register_handlers(dp):
    
    add_chanel.register_handlers(dp)
    start.register_handlers(dp)
    help.register_handlers(dp)
    echo.register_handlers(dp)
