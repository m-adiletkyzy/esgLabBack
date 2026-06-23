import datetime

import pytz
import requests
import lxml
from bs4 import BeautifulSoup

from v1.parsers.ParsClasses import EventClass

url_esgnewscomRu = 'https://esgnews.com/ru/'
url_esgnewscomEn = 'https://esgnews.com/'
url_esgnewsEvents = 'https://esgnews.com/esg-events/'

class EsgnewscomRuEvent(EventClass):
    def __init__(self, e: BeautifulSoup, lang, siteUrl):
        # 1. Дата события
        time_tag = e.find('time', class_='tribe-events-calendar-list__event-date-tag-datetime')
        date0 = time_tag['datetime'] if time_tag and time_tag.has_attr('datetime') else None
        self.date = pytz.utc.localize(datetime.datetime.strptime(date0, '%Y-%m-%d')) if date0 else None

        # 2. Заголовок
        title_tag = e.find('h3', class_='tribe-events-calendar-list__event-title')
        self.title = title_tag.get_text(strip=True) if title_tag else "Без названия"

        # 3. Изображение
        img_tag = e.find('img', class_='tribe-events-calendar-list__event-featured-image')
        self.image_url = img_tag['src'] if img_tag and img_tag.has_attr('src') else None

        # 4. Описание
        digest_tag = e.find('div', class_='tribe-events-calendar-list__event-description')
        self.digest = digest_tag.get_text(strip=True) if digest_tag else ""

        # 5. Ссылка
        a_tag = e.find('a', class_='tribe-events-calendar-list__event-title-link')
        self.url = a_tag['href'] if a_tag and a_tag.has_attr('href') else siteUrl

        # Дополнительное
        self.site_url = siteUrl
        self.lang = lang


def Parse_EsgnewscomEventsBase(link):
    headers = {'User-Agent': 'My User Agent 1.0', }
    raw = requests.get(link, headers=headers, timeout=30)
    raw.raise_for_status()
    soup = BeautifulSoup(raw.text, 'lxml')
    event_container = soup.find('div', {'class': 'tribe-events-calendar-list'})

    if not event_container:
        return []

    event_soup_list = event_container.find_all('div', {'class': 'tribe-common-g-row tribe-events-calendar-list__event-row'})

    return event_soup_list

def Parse_EsgnewscomRuEvents():
    event_soup_list = Parse_EsgnewscomEventsBase(url_esgnewsEvents)
    event_list = [EsgnewscomRuEvent(e, 'ru', url_esgnewscomRu) for e in event_soup_list]

    return event_list

def Parse_EsgnewscomEnEvents():
    event_soup_list = Parse_EsgnewscomEventsBase(url_esgnewsEvents)
    event_list = [EsgnewscomRuEvent(e, 'en', url_esgnewscomEn) for e in event_soup_list]

    return event_list
