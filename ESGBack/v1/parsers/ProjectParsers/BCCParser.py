from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
from v1.parsers.ParsClasses import ProjectClass

def is_absolute(url):
    return bool(urlparse(url).netloc)

linkRu = "https://www.bcc.kz/about/esg/"
linkKz = "https://www.bcc.kz/kz/about/esg/"
linkEn = "https://www.bcc.kz/en/about/esg/"

class BCClass(ProjectClass):
    def __init__(self, block, lang, siteUrl):
        self.lang = lang
        self.site_url = siteUrl

        # Название проекта
        title_div = block.find('div', class_='product-card-title')
        self.title = title_div.text.strip() if title_div else 'Без названия'

        # PDF-ссылка
        btn = block.find('a', class_='btn')
        href = btn['href'] if btn and btn.has_attr('href') else ''
        self.url = href if is_absolute(href) else urljoin(siteUrl, href)

        # Картинка (фон)
        img_div = block.find('div', class_='product-card-img')
        bg_style = img_div.get('style', '') if img_div else ''
        self.image_url = ''
        if 'url(' in bg_style:
            start = bg_style.find('url(') + 4
            end = bg_style.find(')', start)
            self.image_url = bg_style[start:end]

def parse_bcc_projects_by_lang(lang: str, url: str):
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    cards = soup.find_all('div', class_='product-card')
    return [BCClass(card, lang, url) for card in cards]

def Parse_BCCRuProject():
    return parse_bcc_projects_by_lang('ru', linkRu)

def Parse_BCCKzProject():
    return parse_bcc_projects_by_lang('kk', linkKz)

def Parse_BCCEnProject():
    return parse_bcc_projects_by_lang('en', linkEn)
