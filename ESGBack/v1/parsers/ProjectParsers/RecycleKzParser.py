# from urllib.parse import urljoin, urlparse
# import requests
# import lxml
# from bs4 import BeautifulSoup
# from v1.parsers.ParsClasses import ProjectClass

# def is_absolute(url):
#     return bool(urlparse(url).netloc)

# ResycleKz = 'https://recycle.kz/'
# ResycleKzRu = 'https://recycle.kz/ru/'

# class ResycleKzClass(ProjectClass):
#     def __init__(self, p:BeautifulSoup, lang, siteUrl):
#         self.title = p.find('p', {'class':'proekties__title'}).text
#         self.lang = lang
#         self.site_url = siteUrl
#         self.image_url = urljoin(ResycleKz, p.find('img')['src'])

#         if not is_absolute(p['href']):
#             self.url = urljoin(ResycleKz,  lang + p['href'])
#         else:
#             self.url = p['href']


# def Parse_ResycleKzRuProject():
#     raw = requests.get(ResycleKzRu + 'proekty')
#     soup = BeautifulSoup(raw.text, 'lxml')

#     projectsoup = soup.find_all('a', {'class': 'proekties__wrap'})

#     projects = [ResycleKzClass(p, 'ru', ResycleKzRu) for p in projectsoup]

#     return projects