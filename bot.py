from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, Location
from database import SessionLocal, Event
import asyncio
import os
from geopy.distance import geodesic

TOKEN = os.getenv("8182443228:AAGznPxs3-VV3LpeAcwKSHXKc8HvvPOqcqU")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def welcome(message: Message):
    await message.answer(
        "Добро пожаловать! Поделитесь геолокацией, чтобы мы могли найти ближайшие не только по времени, но и месту мероприятия.", 
        reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
            types.KeyboardButton("📍 Отправить геолокацию", request_location=True)
        )
    )

@dp.message_handler(content_types=["location"])
async def send_nearby_events(message: Message):
    user_lat = message.location.latitude
    user_lon = message.location.longitude

    session = SessionLocal()
    events = session.query(Event).all()

    response = "🎉 Ближайшие мероприятия:\n\n"
    count = 0
    for event in events:
        if event.latitude and event.longitude:
            event_coords = (event.latitude, event.longitude)
            user_coords = (user_lat, user_lon)
            distance = geodesic(user_coords, event_coords).kilometers
            if distance <= 10:
                response += f"📍 {event.title} ({event.location}) - {event.time}\n"
                count += 1

    if count == 0:
        response += "😔 Мероприятий поблизости не найдено."

    await message.answer(response)

@dp.message_handler(commands=["events"])
async def send_upcoming_events(message: Message):
    """ Показываем ближайшие мероприятия по времени (если геолокация недоступна). """
    session = SessionLocal()
    events = session.query(Event).order_by(Event.time).limit(5).all()
    response = "🎉 Ближайшие мероприятия:\n\n"
    for event in events:
        response += f"📍 {event.title} ({event.location}) - {event.time}\n"

    await message.answer(response)

async def main():
    await dp.start_polling(skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())

