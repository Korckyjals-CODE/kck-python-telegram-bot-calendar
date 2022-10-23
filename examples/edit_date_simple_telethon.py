"""
Example using telethon.
"""

from telethon import TelegramClient, events

from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

api_id =  123456 
api_hash =  'apihas'
bot_token = "token"

bot = TelegramClient("bot", api_id, api_hash)
valid_dates = ['2022-08-11', '2022-07-11', '2022-08-15', '2022-08-03'] #List containing the dates to be affected
edit_string = "(2){0} " #Format in which dates will be modified


@bot.on(events.NewMessage(pattern="/start"))
async def reply_handler(event):
    calendar, step = DetailedTelegramCalendar(telethon=True, valid_dates=valid_dates, edit_string=edit_string).build()
    await event.respond(f"Select {LSTEP[step]}", buttons=calendar)


@bot.on(events.CallbackQuery(pattern=DetailedTelegramCalendar.func(telethon=True)))
async def calendar_handler(event):
    result, key, step = DetailedTelegramCalendar(telethon=True, valid_dates=valid_dates, edit_string=edit_string).process(event.data.decode("utf-8"))

    if not result and key:
        await event.edit(f"Select {LSTEP[step]}", buttons=key)
    elif result:
        await event.edit(f"You selected {result}")


bot.start(bot_token=bot_token)
with bot:
    bot.run_until_disconnected()