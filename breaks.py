import simplematrixbotlib as botlib
import threading
import asyncio
import sys

creds = botlib.Creds(sys.argv[1], sys.argv[2], sys.argv[3])
DEFAULT_WORK_DURATION = "50"
DEFAULT_BREAK_DURATION = "10"
bot = botlib.Bot(creds)
PREFIX = '!'
tasks = {}

async def thread_function(work_duration, break_duration, room):
    while True:
        await asyncio.sleep(60 * work_duration)
        await bot.api.send_text_message(
                room.room_id, "take a break."
                )
        await asyncio.sleep(60 * break_duration)
        await bot.api.send_text_message(
                room.room_id, "break over."
                )

@bot.listener.on_message_event
async def echo(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)

    if match.is_not_from_this_bot() and match.prefix() and match.command("echo"):
        await bot.api.send_text_message(
                room.room_id, " ".join(arg for arg in match.args())
                )

    if match.is_not_from_this_bot() and match.prefix() and match.command("start"):
        work_duration = match.args()[0] if match.args() and str.isdigit(match.args()[0]) else DEFAULT_WORK_DURATION    
        break_duration = match.args()[1] if match.args() and str.isdigit(match.args()[1]) else DEFAULT_BREAK_DURATION
        if room in tasks and not tasks[room].cancelled():
            await bot.api.send_text_message(
                    room.room_id, "timer already running. cancelling "
                    )
            tasks[room].cancel()
            await asyncio.sleep(0.5)
        await bot.api.send_text_message(
                room.room_id, "starting timer for " + work_duration + " minutes with " + break_duration + " minutes break."
                )
        tasks[room] = asyncio.create_task(thread_function(int(work_duration), int(break_duration), room))

    if match.is_not_from_this_bot() and match.prefix() and match.command("stop"):
        if room in tasks and not tasks[room].cancelled():
            tasks[room].cancel()
            await bot.api.send_text_message(
                    room.room_id, "stopped timer"
                    )
        else:
            await bot.api.send_text_message(
                    room.room_id, "no timer running"
                    )

bot.run()
