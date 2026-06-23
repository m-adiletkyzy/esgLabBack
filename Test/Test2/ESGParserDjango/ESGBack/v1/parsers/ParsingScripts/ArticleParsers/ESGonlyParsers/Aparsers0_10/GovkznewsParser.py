import json

import requests
import lxml
from bs4 import BeautifulSoup
from v1.parsers.ParsClasses import ArticleClass

GovKzUrl = 'https://www.gov.kz/'
GovKzApiUrl = 'https://www.gov.kz/api/v1/public/content-manager/news?sort-by=created_date:DESC&page=1&size=5&directions=14993'


headersRu = {'User-Agent': 'My User Agent 1.0', 'Accept-Language':'ru'}
headersKz = {'User-Agent': 'My User Agent 1.0', 'Accept-Language':'kk'}

class GovkzArticle(ArticleClass):
    def __init__(self, a: json, lang, siteUrl):
        self.title = a['title']
        self.image_url = 'https://www.gov.kz'+ a['heropic']
        self.digest = BeautifulSoup(a['body'], 'lxml').find('p').text.strip()
        url_base = 'https://www.gov.kz/memleket/entities/ardfm/press/news/details/'
        self.url = url_base + str(a['id']) + '?lang=' + lang
        self.date = a['created_date']
        self.site_url = siteUrl
        self.lang = lang




def Parse_GovkznewsBase(header):
    raw = requests.get(GovKzApiUrl, headers=header)
    article_json_list = raw.json()

    return article_json_list

def Parse_GovkznewsRu():
    article_json_list = Parse_GovkznewsBase(headersRu)
    article_list = [GovkzArticle(a, 'ru', GovKzUrl) for a in article_json_list]

    return article_list

def Parse_GovkznewsKz():
    article_json_list = Parse_GovkznewsBase(headersKz)
    article_list = [GovkzArticle(a, 'kk', GovKzUrl) for a in article_json_list]

    return article_list

