from datetime import datetime
import re
from html import unescape

import requests

from v1.parsers.ESGfilters import filter_esg_items
from v1.parsers.ParsClasses import EventClass

url_atamekenKzRu = 'https://atameken.kz/ru/'
url_atamekenKzKk = 'https://atameken.kz/kk/'
url_atamekenKzEn = 'https://atameken.kz/en/'
api_atamekenKzRu_Events = 'https://atameken.kz/api/content/events/'

def strip_html(value: str) -> str:
    if not value:
        return ''
    text = re.sub(r'<[^>]+>', ' ', value)
    return ' '.join(unescape(text).split())


class AtamekenKzEvent(EventClass):
    def __init__(self, event_data: dict, lang: str, site_url: str):
        title_map = event_data.get('title') or {}
        content_map = event_data.get('content') or {}
        image_map = event_data.get('image') or {}
        selected_image = image_map.get(lang) or image_map.get('ru') or {}

        self.title = title_map.get(lang) or title_map.get('ru') or ''
        self.digest = strip_html(content_map.get(lang) or content_map.get('ru') or '')
        self.url = f"https://atameken.kz/ru/events?slug={event_data.get('slug', '')}"
        self.date = datetime.fromisoformat(event_data['display_date'])
        self.site_url = site_url
        self.lang = lang

        self.image_url = selected_image.get('original', '')
        if self.image_url and self.image_url.startswith('/'):
            self.image_url = f'https://atameken.kz{self.image_url}'


def Parse_AtamekenKzRuEvents():
    raw = requests.get(api_atamekenKzRu_Events, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
    raw.raise_for_status()

    payload = raw.json()
    events_data = payload.get('results', [])
    events = [AtamekenKzEvent(event_data, 'ru', url_atamekenKzRu) for event_data in events_data]
    return filter_esg_items(events, 'ru')


def Parse_AtamekenKzKkEvents():
    raw = requests.get(api_atamekenKzRu_Events, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
    raw.raise_for_status()

    payload = raw.json()
    events_data = payload.get('results', [])
    events = [AtamekenKzEvent(event_data, 'kk', url_atamekenKzKk) for event_data in events_data]
    return filter_esg_items(events, 'kk')


def Parse_AtamekenKzEnEvents():
    raw = requests.get(api_atamekenKzRu_Events, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
    raw.raise_for_status()

    payload = raw.json()
    events_data = payload.get('results', [])
    events = [AtamekenKzEvent(event_data, 'en', url_atamekenKzEn) for event_data in events_data]
    return filter_esg_items(events, 'en')
