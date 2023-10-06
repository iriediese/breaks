import simplematrixbotlib as botlib
import threading
import asyncio
import sys

creds = botlib.Creds(sys.argv[1], sys.argv[2], sys.argv[3])
bot = botlib.Bot(creds)
PREFIX = '!'
tasks = {}

async def thread_function(duration, room):
    while True:
        await asyncio.sleep(60 * duration)
        await bot.api.send_text_message(
                room.room_id, "take a break."
                )

@bot.listener.on_message_event
async def echo(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)

    if match.is_not_from_this_bot() and match.prefix() and match.command("echo"):
        await bot.api.send_text_message(
                room.room_id, " ".join(arg for arg in match.args())
                )

    if match.is_not_from_this_bot() and match.prefix() and match.command("start"):
        duration = match.args()[0] if match.args() and str.isdigit(match.args()[0]) else "60"
        if room in tasks and not tasks[room].cancelled():
            await bot.api.send_text_message(
                    room.room_id, "timer already running. cancelling "
                    )
            tasks[room].cancel()
            await asyncio.sleep(0.5)
        await bot.api.send_text_message(
                room.room_id, "starting timer for " + duration + " minutes"
                )
        tasks[room] = asyncio.create_task(thread_function(int(duration), room))

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
