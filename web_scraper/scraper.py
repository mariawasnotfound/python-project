import requests 
from bs4 import BeautifulSoup 
from db import save_event 
 
URL = 'https://afisha.timepad.ru/chelyabinsk/' 
 
def get_event_data(): 
    response = requests.get(URL) 
    soup = BeautifulSoup(response.content, 'html.parser') 
    events = [] 
 
    for event in soup.select('.event-card'):
        name = event.select_one('.event-title').get_text(strip=True) 
        date = event.select_one('.event-date').get_text(strip=True) 
        location = event.select_one('.event-location').get_text(strip=True) 
        contact_info = event.select_one('.contact-info').get_text(strip=True) if event.select_one('.contact-info') else 'Информация недоступна'
        events.append({ 
            'name': name, 
            'date': date, 
            'location': location, 
            'contact_info': contact_info, 
            'free_spaces': None
        })
    return events 
 
def save_events_to_db(events): 
    for event in events: 
        save_event(event['name'], event['date'], event['location'], event['free_spaces'], event['contact_info']) 
 
if name == "__main__": 
    event_data = get_event_data() 
    save_events_to_db(event_data)
