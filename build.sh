#!/bin/bash

export $(grep -v '^#' .env | xargs)

echo "Собираем и запускаем проект через Docker Compose..."
docker-compose down --volumes
docker-compose up --build -d

echo "Запускаем PostgreSQL..."
until docker exec afisha_db pg_isready -U mariawasnotfound > /dev/null 2>&1; do
  echo "Еще пара секунд..."
  sleep 8
done

echo "PostgreSQL готов! Скрапим данные..."
docker exec -it nearby_events_bot python3 /app/scraper.py

echo "Ура! Проект запущен и все работает!"
