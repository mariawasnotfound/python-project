#!/bin/bash

echo "Создаем и запускаем контейнеры..."
docker-compose down
docker-compose up --build -d

echo "Ожидание запуска контейнеров..."
sleep 10

echo "Создание таблиц в базе данных..."
docker-compose exec web python app/database.py

echo "Готово! Сервис работает."
