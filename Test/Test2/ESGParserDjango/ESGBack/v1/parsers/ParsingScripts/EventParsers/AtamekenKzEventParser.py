import datetime
import json
from v1.parsers.NlpMethods import KeywordsFiltration
import pytz
import requests
import lxml
from bs4 import BeautifulSoup

from v1.parsers.ParsClasses import EventClass

url_atamekenKzRu = 'https://atameken.kz/ru/'
api_atamekenKzRu_Events = 'https://atameken.kz/ru/api/events_with_news?date='

today = datetime.date.today().strftime('%Y-%m-%d')

class AtamekenKzEvent(EventClass):
    def __init__(self, e: json, lang, siteUrl):
        self.title = e['title_ru']
        if e['image']: self.image_url = 'https://atameken.kz' + e['image']
        self.digest = BeautifulSoup(e['teaser_ru'], 'lxml').text
        self.url = 'https://atameken.kz/ru/events/' + str(e['id']) + '-' + e['alias']
        self.date = pytz.utc.localize(datetime.datetime.strptime(e['display_date'], '%Y-%m-%d %H:%M:%S'))
        self.site_url = siteUrl
        self.lang = lang


def Parse_AtamekenKzRuEvents():
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    raw = requests.get(api_atamekenKzRu_Events + today)
    eventsRu = raw.json()['events']
    event_list = [AtamekenKzEvent(e, 'ru', url_atamekenKzRu) for e in eventsRu]
    KWF = KeywordsFiltration('ru')
    event_list_filtered = [e for e in event_list if KWF.EsgKeyWordCheck(e.title + ' ' + e.digest, 'ru')]

    return event_list_filtered

