import os
from dotenv import load_dotenv
from PdfConvertorBot.sample_config import Config
from PdfConvertorBot.convertor import PdfDoc
from pyrogram import Client

load_dotenv("config.env")

IS_ENV = bool(os.environ.get("ENV", True))


if IS_ENV:
    TOKEN = str(os.environ.get("TOKEN", None))
    APP_ID = int(os.environ.get("APP_ID", None))
    API_HASH = str(os.environ.get("API_HASH", None))
    BOT_USERNAME = str(os.environ.get("BOT_USERNAME", None))

else:
    TOKEN = Config.TOKEN
    APP_ID = Config.APP_ID
    API_HASH = Config.API_HASH
    BOT_USERNAME = Config.BOT_USERNAME

DOWNLOAD_PATH = "./PdfConvertorBot/convertor/files/"
THUMB_PATH = "./PdfConvertorBot/convertor/files/thumbs/"

client = Client("PdfConvertorBot", APP_ID, API_HASH, bot_token = TOKEN)
