from v1.parsers.NlpMethods import (
    KeywordsFiltration,
    classify_news,
    lemmatizateText,
    should_notify_user,
)

ru_keywords = ['esg', 'устойчивое развитие']
ru_keywords = [lemmatizateText(w, 'ru') for w in ru_keywords]

_EN_ESG_TERMS = (
    'esg',
    'sustainability',
    'climate',
    'carbon',
    'renewable',
    'green',
    'environment',
)

_kw_filters = {}


def _get_kw_filter(lang: str) -> KeywordsFiltration:
    if lang not in _kw_filters:
        _kw_filters[lang] = KeywordsFiltration(lang)
    return _kw_filters[lang]


def isESGRu(text: str) -> bool:
    text = lemmatizateText(text, 'ru')

    for w in ru_keywords:
        if w in text:
            return True

    return False


def is_esg_content(text: str, lang: str) -> bool:
    if lang in ('ru', 'kk'):
        return _get_kw_filter(lang).EsgKeyWordCheck(text, lang)

    normalized = lemmatizateText(text, lang)
    return any(term in normalized for term in _EN_ESG_TERMS)


def filter_esg_items(items, lang: str, genre_ids=None):
    return [
        item
        for item in items
        if is_esg_content_for_genres(
            f"{item.title} {getattr(item, 'digest', '') or ''}",
            lang,
            genre_ids,
        )
    ]


def is_esg_content_for_genres(text: str, lang: str, genre_ids=None) -> bool:
    if genre_ids:
        if lang in ('ru', 'kk'):
            return should_notify_user(genre_ids, classify_news(text, lang))
        return is_esg_content(text, lang)
    return is_esg_content(text, lang)
