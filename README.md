Телеграм Бот: Nearest Events Bot
 
Не знаете чем заняться сегодня вечером? Nearest Events Bot поможет вам найти ближайшие не только по времени, но и по месту мероприятия, которые вы сможете посетить! (пока только для Челябинска) 
 
Бот выполняет следующие команды:
/start - начало работы с ботом. Бот сообщает пользователю, что, поделившись геолокацией, он сможет увидеть список мероприятий близких не только по времени, но и по месту.

Кнопка "Поделиться геолокацией" - бот, получив геолокацию пользователя, выводит список мероприятий ближайших по месту и времени.

/events - бот выводит список мероприятий, ближайших по времени.

Скрапинг сайта: https://chel.guide/events
Мероприятия сохраняются в базу данных PostgreSQL. 

Структура: 
.env - настройка окружения. 
scraper.py - парсинг данных с сайта. 
models.py - определение таблицы Базы Данных. 
init.sql - создание таблицы Базы Данных. 
database.py - подключение к Базы Данных. 
docker-compose.yml - управление контейнерами docker. 
bot.py - Телеграм бот. 
Dockerfile - сборка образа. 
requirements.txt - зависимости python. 
build.sh - запуск проекта.

Установка и запуск: 
1. Клонируйте репозиторий. 
2. Установите Docker и docker-compose. 
3. Запустите сборку проекта командой - bash build.sh
