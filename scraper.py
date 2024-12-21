import requests
from bs4 import BeautifulSoup

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

    events.append({
        'name': name,
        'date': date,
        'time': time,
        'location': location
    })

for event in events:
    print(f"Название: {event['name']}, Дата: {event['date']}, Время: {event['time']}, Место: {event['location']}")

