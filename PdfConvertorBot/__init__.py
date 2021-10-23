from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update, Bot
import os
from dotenv import load_dotenv
from PdfConvertorBot.sample_config import Config
from PdfConvertorBot.convertor import PdfDoc

load_dotenv("config.env")

IS_ENV = bool(os.environ.get("ENV", False))

if IS_ENV:
    TOKEN = str(os.environ.get("TOKEN", None))
else:
    TOKEN = Config.TOKEN


new_pdf = PdfDoc("V17_Novel_Reincarnated_as_a_Slime")

print(new_pdf.get_details())