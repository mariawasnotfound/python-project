import logging 
from aiogram import Bot, Dispatcher, executor, types 
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton 
import psycopg2 
from psycopg2.extras import RealDictCursor 
 
logging.basicConfig(level=logging.INFO) 
 
BOT_TOKEN = '8182443228:AAGznPxs3-VV3LpeAcwKSHXKc8HvvPOqcqU' 
 
DB_CONFIG = { 
    'dbname': 'database_name',  
    'user': 'username',  
    'password': 'password',  
    'host': 'localhost',  
    'port': 5432 
} 
 
try: 
    conn = psycopg2.connect(**DB_CONFIG) 
    cursor = conn.cursor(cursor_factory=RealDictCursor) 
    logging.info("Успешное подключение к базе данных") 
except Exception as e: 
    logging.error(f"Ошибка подключения к базе данных: {e}") 
    exit() 
 
bot = Bot(token=BOT_TOKEN) 
dp = Dispatcher(bot) 
 
# Запрос геолокации для определения ближайших по месту мероприятий 
location_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) 
location_button.add(KeyboardButton("🌐 Предоставить геолокацию", request_location=True)) 
 
@dp.message_handler(commands=['start']) 
async def start_command(message: types.Message): 
    """Обработка команды /start""" 
    await message.reply("Привет! Чтобы увидеть ближайшие мероприятия не только по времени, но и по месту, можете предоставить вашу геолокацию.",  
                        reply_markup=location_button) 
 
 
@dp.message_handler(content_types=['location']) 
async def handle_location(message: types.Message): 
    """Обработка отправки геолокации от пользователя""" 
    latitude = message.location.latitude 
    longitude = message.location.longitude 
    user_id = message.from_user.id

    # Сохранение/обновление местоположения пользователя в базе данных 
    try: 
        cursor.execute("""INSERT INTO user_locations (user_id, latitude, longitude)  
                        VALUES (%s, %s, %s)  
                        ON CONFLICT (user_id) DO UPDATE  
                        SET latitude = EXCLUDED.latitude, longitude = EXCLUDED.longitude""",  
                       (user_id, latitude, longitude)) 
        conn.commit() 
    except Exception as e: 
        logging.error(f"Ошибка при сохранении геолокации: {e}") 
     
    await message.reply("Спасибо! Теперь вы можете использовать команду /events для просмотра ближайших мероприятий.") 
 
@dp.message_handler(commands=['events']) 
async def show_events(message: types.Message): 
    """Обработка команды /events""" 
    user_id = message.from_user.id 
    try: 
        cursor.execute("SELECT latitude, longitude FROM user_locations WHERE user_id = %s", (user_id,)) 
        location = cursor.fetchone() 
    except Exception as e: 
        logging.error(f"Ошибка при получении геолокации пользователя: {e}") 
        location = None 
 
    try: 
        if location: 
            # Мероприятия ближайшие по месту 
            cursor.execute(""" 
                SELECT * FROM events  
                WHERE (earth_distance(ll_to_earth(latitude, longitude), ll_to_earth(%s, %s)) < 5000)  
                AND start_time >= NOW() AND start_time <= NOW() + interval '12 hours'  
                ORDER BY start_time ASC LIMIT 5 
            """, (location['latitude'], location['longitude'])) 
        else: 
            # Мероприятия ближайшие только по времени (отсутствие геолокации) 
            cursor.execute(""" 
                SELECT * FROM events  
                WHERE start_time >= NOW() AND start_time <= NOW() + interval '12 hours'  
                ORDER BY start_time ASC LIMIT 5 
            """) 
 
        events = cursor.fetchall()

        if events: 
            response = "Ближайшие мероприятия:\n" 
            for event in events: 
                status = event.get('availability_status', 'Нуждается в уточнении') 
                response += f"\n✨ {event['title']} \n⏰ Время: {event['start_time']} \n☞ Место: {event['location']} \n❓ Доступность мест: {status}\n" 
                response += f"Подробнее: {event['link']}\n" 
        else: 
            response = "К сожалению, ближайших мероприятий не найдено."

        await message.reply(response) 
    except Exception as e: 
        logging.error(f"Ошибка при получении мероприятий: {e}") 
        await message.reply("Произошла ошибка при получении мероприятий. Пожалуйста, попробуйте позже.")

@dp.message_handler(commands=['available']) 
async def check_availability(message: types.Message): 
    """Обработка команды для проверки доступности мест на мероприятии""" 
    event_id = message.get_args() 
     
    if not event_id: 
        await message.reply("Пожалуйста, укажите ID мероприятия. Например: /available 123") 
        return 
     
    try: 
        cursor.execute("SELECT available_status FROM events WHERE id = %s", (event_id,)) 
        event = cursor.fetchone() 
        if event: 
            status = event['available_status'] or 'Нуждается в уточнении' 
            await message.reply(f"Доступность мест на мероприятии: {status}") 
        else: 
            await message.reply("Мероприятие с таким ID не найдено.") 
    except Exception as e: 
        logging.error(f"Ошибка при проверке доступности мест: {e}") 
        await message.reply("Произошла ошибка при проверке доступности мест.") 
 
 
if name == '__main__': 
    logging.info("Бот запущен") 
    executor.start_polling(dp, skip_updates=True)
