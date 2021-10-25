import os
from time import time
from typing import Optional
from pyrogram import Client
from pyrogram.types import Message, Document
from PdfConvertorBot.progress import progress
from pyrogram.filters import command, private
from PdfConvertorBot.convertor import PdfDoc
from PdfConvertorBot import client, DOWNLOAD_PATH, BOT_USERNAME

@client.on_message(command(['tohtml', f'tohtml@{BOT_USERNAME}'], ['/', '!']) & private)
async def convert_to_html(client: Client, message: Message):
    reply: Optional[Message] = message.reply_to_message
    document: Optional[Document] = message.reply_to_message.document
    text = message.text.split(" ", 1)
    if not reply and not document:
        return await message.reply(
            text = "No PDF file mentioned. Please reply to a pdf document.",
            quote = True
        )
    if not document.file_name.lower().endswith(".pdf"):
        return await message.reply(
            text = "Please reply to a pdf document.",
            quote = True
        )
    if len(text) == 1:
        file_name = document.file_name
    elif len(text) == 2:
        if text[1].lower().endswith(".pdf"):
            file_name = text[1]
        if not text[1].lower().endswith(".pdf"):
            name_parts = text[1].split(".")
            if len(name_parts) > 1:
                file_name = ".".join(text[1].split(".")[:-1].append("pdf"))
            if len(name_parts) == 1:
                file_name = name_parts[0]+".pdf"
    msg = await message.reply_text(
        text = "Getting the file info...",
        quote = True
    )
    start_time = time()
    doc_location = await client.download_media(
        message = reply, 
        file_name = DOWNLOAD_PATH, 
        progress = progress,
        progress_args = ("d", msg, start_time)
    )
    if not doc_location or not os.path.exists(doc_location):
        return await msg.edit_text(
            "Download failed try again later!"
        )
    try:
        await msg.edit_text(
            "Downloaded Successfully and converting!"
        )
    except:
        pass
    os.rename(doc_location, DOWNLOAD_PATH+file_name)
    pdf_doc = PdfDoc(file_name)
    html_path = await pdf_doc.convert_to_html()
    if not html_path:
        return await msg.edit_text(
            "Not able to convert to html"
        )
    start_time = time()
    await message.reply_document(
        document = html_path,
        quote = True,
        caption = "Successfully Converted to HTML!",
        progress = progress,
        progress_args = ("u", msg, start_time)
    )
    try:
        os.remove(DOWNLOAD_PATH+file_name)
        os.remove(html_path)
    except:
        pass
    return await msg.delete()

