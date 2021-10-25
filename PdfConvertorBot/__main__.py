from PdfConvertorBot import client, BOT_USERNAME
import PdfConvertorBot.modules
from pyrogram.filters import command
from pyrogram import Client
from pyrogram.types import Message


@client.on_message(command(['start', f"start@{BOT_USERNAME}"], prefixes=['/', '!']))
async def start_handler(client: Client, message: Message):
    chat = message.chat
    if chat.type == "private":
        return await message.reply_text("Heya Whats Up?")
    return await message.reply_text("Heya Whats Up?")



client.run()