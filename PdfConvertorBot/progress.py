from pyrogram.types import Message
from time import time
import math

def parse_time(time: int):
    days = math.floor(time/86400)
    remainder = time % 86400
    hours = math.floor(remainder/3600)
    _remainder_ = remainder % 3600
    min = math.floor(_remainder_/60)
    sec = _remainder_ % 60
    time = ""
    if days > 0:
        time += str(days)+"d, "
    if hours > 0:
        time += str(hours)+"h, "
    if min > 0:
        time += str(min)+"m, "
    time += str(sec)+"s"
    return time

def readable_bytes(bytes: float):
    if not bytes:
        return ""
    base = 1024
    type = ["", "K", "M", "G", "T"]
    count = 0
    while bytes > base:
        bytes /= base
        count += 1
    return str(round(bytes, 2)) + " " + type[count] + "B"



async def progress(current: int, total: int, type: str, message: Message, start: float):
    current_time = time()
    if (current_time - start)%4 == 0 or current == total:
        percentage = current*100/total
        speed = current/(current_time-start)
        time_to_complete = round((total-current)/speed)
        progress_message = ""
        if type == "d":
            progress_message += "Trying to download:\n\nDownloaded {}({}%) of {}\n".format(
                readable_bytes(current), round(percentage, 2), readable_bytes(total)
            )
        if type == "u":
            progress_message += "Trying to upload:\n\nUploaded {}({}%) of {}\n".format(
                readable_bytes(current), round(percentage, 2), readable_bytes(total)
            )
        progress_message += "Speed: {}\nETA: {}".format(
            readable_bytes(speed)+"/s",
            parse_time(time_to_complete)
        )
        try:
            await message.edit_text(
                progress_message
            )
        except:
            pass

        
            


