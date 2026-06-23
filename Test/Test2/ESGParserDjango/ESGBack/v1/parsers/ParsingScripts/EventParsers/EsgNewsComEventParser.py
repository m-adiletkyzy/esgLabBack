import datetime

import pytz
import requests
import lxml
from bs4 import BeautifulSoup

from v1.parsers.ParsClasses import EventClass

url_esgnewscomRu = 'https://esgnews.com/ru/'
url_egsnewsRuEvents = 'https://esgnews.com/ru/%D0%A1%D0%BE%D0%B1%D1%8B%D1%82%D0%B8%D1%8F/'

class EsgnewscomRuEvent(EventClass):
    def __init__(self, e: BeautifulSoup, lang, siteUrl):
        date0 = e.find('time')['datetime']

        self.title = e.find('h3', {'class': 'tribe-events-calendar-list__event-title tribe-common-h6 tribe-common-h4--min-medium'}).text.strip()
        try:
            self.image_url = e.find('img', {'class': 'attachment-large size-large'})['src']
        except:
            self.image_url = None

        self.digest = e.find('div', {'class': 'tribe-events-calendar-list__event-description tribe-common-b2 tribe-common-a11y-hidden'}).text.strip()
        self.url = e.find('a', {'class': 'tribe-events-calendar-list__event-title-link tribe-common-anchor-thin'})['href']
        self.date = pytz.utc.localize(datetime.datetime.strptime(date0, '%Y-%m-%d'))
        self.site_url = siteUrl
        self.lang = lang

def Parse_EsgnewscomEventsBase(link):
    headers = {'User-Agent': 'My User Agent 1.0', }
    raw = requests.get(link, headers=headers)
    soup = BeautifulSoup(raw.text, 'lxml').find('div', {'class': 'tribe-events-calendar-list'})
    event_soup_list = soup.find_all('div', {'class': 'tribe-common-g-row tribe-events-calendar-list__event-row'})

    return event_soup_list

def Parse_EsgnewscomRuEvents():
    event_soup_list = Parse_EsgnewscomEventsBase(url_egsnewsRuEvents)
    event_list = [EsgnewscomRuEvent(e, 'ru', url_esgnewscomRu) for e in event_soup_list]

    return event_list

