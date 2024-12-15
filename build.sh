#!/bin/bash

echo "Создаем и запускаем контейнеры..."
docker-compose up -d --build

echo "Ожидание запуска контейнеров..."
sleep 10

echo "Создание таблиц в базе данных..."
docker exec telegram_bot python -c "from db import create_tables; create_tables()"

echo "Готово! Сервис работает."
