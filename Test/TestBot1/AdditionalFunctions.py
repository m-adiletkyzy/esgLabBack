from urllib.parse import urlparse

def ProperErrorName(Error):
    parsed_url = urlparse(Error['ParsedSite'])
    domain = parsed_url.netloc
    date0 = Error["ErrorDate"][:16]
    return f'Сайт: {domain} \nДата: {date0}'