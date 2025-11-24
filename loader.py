# pip imports
from telegram import Bot

# local imports
from data.config import config

bot = Bot(token=config.BOT_TOKEN)
