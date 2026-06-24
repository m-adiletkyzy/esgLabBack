import json
from datetime import datetime

import requests
import lxml
from bs4 import BeautifulSoup
from v1.parsers.ESGfilters import filter_esg_items
from v1.parsers.ParsClasses import NewsClass

GovKzUrl = 'https://www.gov.kz/'
GovKzApiUrl = 'https://www.gov.kz/api/v1/public/content-manager/news?sort-by=created_date:DESC&page=1&size=5&directions=14993'


headersRu = {'User-Agent': 'My User Agent 1.0', 'Accept-Language':'ru'}
headersKz = {'User-Agent': 'My User Agent 1.0', 'Accept-Language':'kk'}

class GovkzNews(NewsClass):
    def __init__(self, a: json, lang, siteUrl):
        self.title = a['title']
        self.image_url = a.get('image') or a.get('preview_image') or ''
        if self.image_url and self.image_url.startswith('/'):
            self.image_url = f'{GovKzUrl.rstrip("/")}{self.image_url}'

        body_soup = BeautifulSoup(a.get('body') or '', 'lxml')
        body_paragraph = body_soup.find('p')
        self.digest = body_paragraph.text.strip() if body_paragraph else body_soup.get_text(" ", strip=True)
        url_base = 'https://www.gov.kz/memleket/entities/ardfm/press/news/details/'
        self.url = url_base + str(a['id']) + '?lang=' + lang
        self.date = datetime.fromisoformat(a['created_date'].replace('Z', '+00:00'))
        self.site_url = siteUrl
        self.lang = lang

def Parse_GovkznewsBase(header):
    raw = requests.get(GovKzApiUrl, headers=header)
    data = raw.json()
    article_json_list = data.get("content", [])

    return article_json_list

def Parse_GovkznewsRu():
    article_json_list = Parse_GovkznewsBase(headersRu)
    article_list = [GovkzNews(a, 'ru', GovKzUrl) for a in article_json_list]
    return filter_esg_items(article_list, 'ru')

def Parse_GovkznewsKz():
    article_json_list = Parse_GovkznewsBase(headersKz)
    article_list = [GovkzNews(a, 'kk', GovKzUrl) for a in article_json_list]
    return filter_esg_items(article_list, 'kk')
