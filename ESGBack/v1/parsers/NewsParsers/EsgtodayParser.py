import time
from datetime import datetime
from urllib.parse import urlparse

import pytz
import requests
from bs4 import BeautifulSoup

from v1.parsers.ParsClasses import NewsClass


Esgtoday_link = 'https://www.esgtoday.com/'


class EsgtodayArticle(NewsClass):
	def __init__(self, elem: BeautifulSoup, lang, siteUrl):
		"""Parse a single article element from Esgtoday"""
		self.site_url = siteUrl
		self.lang = lang

		# title and url
		a = elem.find('a', href=True)
		self.url = a['href'] if a else None

		# try extract title from a link text first
		self.title = None
		if a:
			self.title = a.get_text().strip().replace('\n', ' ')

		# if no title, try typical heading selectors
		if not self.title:
			candidates = [
				lambda e: e.find(class_='entry-title'),
				lambda e: e.find(class_='td-module-title'),
				lambda e: e.find(class_='jeg_post_title'),
				lambda e: e.find('h1'),
				lambda e: e.find('h2'),
				lambda e: e.find('h3'),
			]
			for cand in candidates:
				try:
					node = cand(elem)
					if node:
						text = node.get_text().strip()
						if text:
							self.title = text
							break
				except Exception:
					continue

		# fallback: use element text or URL slug
		if not self.title:
			if self.url:
				try:
					parsed = urlparse(self.url)
					slug = parsed.path.rstrip('/').split('/')[-1]
					if slug:
						self.title = slug.replace('-', ' ').replace('_', ' ').strip().title()
					else:
						self.title = elem.get_text().strip()
				except Exception:
					self.title = elem.get_text().strip()
			else:
				self.title = elem.get_text().strip()

		# date: try time tag or meta
		self.date = None
		try:
			time_tag = elem.find('time')
			if time_tag and time_tag.has_attr('datetime'):
				# ISO-ish datetime
				try:
					self.date = pytz.utc.localize(datetime.fromisoformat(time_tag['datetime']))
				except Exception:
					self.date = time_tag['datetime']
			elif time_tag:
				# textual date like 'March 2, 2026'
				try:
					self.date = datetime.strptime(time_tag.get_text().strip(), '%B %d, %Y')
				except Exception:
					self.date = time_tag.get_text().strip()
		except Exception:
			self.date = None

		# digest/image filled later
		self.digest = None
		self.image_url = None

	def getExtra(self, s: requests.Session):
		"""Fetch article page to get image and digest"""
		if not self.url:
			return

		if urlparse(Esgtoday_link).netloc != urlparse(self.url).netloc:
			return

		time.sleep(0.1)
		print(f"Загрузка {self.url}")
		headers = {'User-Agent': 'My User Agent 1.0'}
		try:
			raw = s.get(self.url, headers=headers, timeout=10)
		except Exception:
			return

		soup = BeautifulSoup(raw.text, 'lxml')

		# image: prefer og:image
		try:
			og = soup.find('meta', property='og:image')
			if og and og.get('content'):
				self.image_url = og['content']
			else:
				fig = soup.find('figure')
				if fig and fig.find('img') and fig.find('img').get('src'):
					self.image_url = fig.find('img')['src']
		except Exception:
			print('Esgtoday image error')

		# digest: first meaningful paragraph
		try:
			article = soup.find('article') or soup.find('div', class_='post') or soup
			p = None
			for candidate in article.find_all('p'):
				text = candidate.get_text().strip()
				if text:
					p = text
					break
			if p:
				self.digest = p
		except Exception:
			print('Esgtoday digest error')


def Parse_EsgtodayBase(link: str = Esgtoday_link):
	"""Fetch the main page and return list of article elements"""
	headers = {'User-Agent': 'My User Agent 1.0'}
	session = requests.Session()

	raw = session.get(link, headers=headers, timeout=15)
	soup = BeautifulSoup(raw.text, 'lxml')

	# try several strategies to find article items
	list0 = soup.find_all('article')
	if not list0:
		# common theme blocks
		list0 = soup.find_all('div', class_=lambda x: x and ('post' in x or 'td_module' in x or 'jeg' in x))

	return list0


# helper to sort by date if available
def myFunc(l: EsgtodayArticle):
	"""Extract datetime for sorting, fallback to datetime.min if not available or parseable"""
	try:
		if isinstance(l.date, datetime):
			return l.date
		# try parse string
		if isinstance(l.date, str):
			try:
				return datetime.fromisoformat(l.date)
			except Exception:
				return datetime.min
	except Exception:
		pass
	return datetime.min


def MakeUniq(list2: list):
	"""Remove duplicates by title, keeping the most recent one based on date"""
	list2.sort(key=myFunc, reverse=True)

	i = 0
	while i + 1 < len(list2):
		try:
			if list2[i].title == list2[i + 1].title:
				list2.pop(i)
			else:
				i += 1
		except Exception:
			i += 1

	return list2


def Parse_EsgtodayNews(max_items: int = 30):
	"""Main function to parse Esgtoday news, returning list of EsgtodayArticle"""
	elems = Parse_EsgtodayBase(Esgtoday_link)
	session = requests.Session()
	result = []

	for e in elems:
		art = EsgtodayArticle(e, 'en', Esgtoday_link)
		art.getExtra(session)
		result.append(art)
		if len(result) >= max_items:
			break

	result = MakeUniq(result)
	return result


def Parse_EsgtodayEnNews(max_items: int = 30):
	"""Backward-compatible alias used by grouped parser launcher."""
	return Parse_EsgtodayNews(max_items=max_items)