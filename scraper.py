import logging
import requests
from bs4 import BeautifulSoup
from models import Event
from database import get_session

def get_coordinates(location):
    location += ", Челябинск"
    api_key = 'e3b1003031fa4e7cb32b832e08c2eda8'
    url = f'https://api.opencagedata.com/geocode/v1/json?q={location}&key={api_key}'
    response_ = requests.get(url)
    data = response_.json()
    results = data['results']
    if results:
        latitude = results[0]['geometry']['lat']
        longitude = results[0]['geometry']['lng']
        return latitude, longitude
    return None, None

# парсинг событий с сайта
def fetch_events():
    url = 'https://chel.guide/events'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    events = []

    for event in soup.find_all('div', class_='teaser_info'):
        name = event.find('span', class_='event__field-title-h1').get_text(strip=True) if event.find('span', class_='event__field-title-h1') else 'Название не указано'
        details = event.find('div', class_='teaser_info__where_when').get_text(strip=True) if event.find('div', class_='teaser_info__where_when') else 'Детали не указаны'

        details_parts = details.split(',')
        date = details_parts[0].strip() if len(details_parts) > 0 else 'Дата не указана'
        time = details_parts[1].strip() if len(details_parts) > 1 else 'Время не указано'
        location = details_parts[2].strip() if len(details_parts) > 2 else 'Место не указано'

        latitude, longitude = get_coordinates(location)

        logging.info(f"Событие: {name}, Дата: {date}, Время: {time}, Место: {location}, Координаты: ({latitude}, {longitude})")

        events.append({
            'name': name,
            'date': date,
            'time': time,
            'location': location,
            'lat': latitude,
            'lng': longitude
        })
    return events

# saving the event in db
def save_event(name, date, time, location, latitude, longitude):
    db_session = get_session()
    db_event = Event(name=name, date=date, time=time, location=location, latitude=latitude, longitude=longitude)
    db_session.add(db_event)
    db_session.commit()
    db_session.close()

# saving a list of events
def save_events_to_db(events):
    for event in events:
        save_event(event['name'], event['date'], event['time'], event['location'], event['lat'], event['lng'])

if __name__ == "__main__":
    # getting and saving
    events = fetch_events()
    save_events_to_db(events)
    print("События успешно сохранены в базу данных.")

