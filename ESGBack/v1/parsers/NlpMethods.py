import os
import string
from pymorphy3 import MorphAnalyzer
from .kaznlp.morphology.analyzers import AnalyzerDD


morph = MorphAnalyzer()
analyzer = AnalyzerDD()
analyzer.load_model(os.path.join(os.path.dirname(__file__), 'kaznlp', 'morphology', 'mdl'))

KEYWORD_FILES_DIR = os.path.join(os.path.dirname(__file__), 'KeyWordFiles')
SUPPORTED_KEYWORD_LANGS = ('ru', 'kk')
ESG_SUBGENRES = ('climate', 'waste', 'labor', 'ethics', 'finance')

ESG_SUBGENRE_LABELS = {
    'climate': {
        'ru': 'Экология и Климат',
        'kk': 'Экология және Климат',
        'en': 'Renewable Energy & Climate Action',
    },
    'waste': {
        'ru': 'Отходы и Ресурсы',
        'kk': 'Қалдықтар мен Ресурстар',
        'en': 'Waste Management, Nature & Resources',
    },
    'labor': {
        'ru': 'Труд и Общество',
        'kk': 'Еңбек және Қоғам',
        'en': 'Labor Rights, DEI & Workforce',
    },
    'ethics': {
        'ru': 'Управление и Этика',
        'kk': 'Басқару және Этика',
        'en': 'Corporate Governance & Ethics',
    },
    'finance': {
        'ru': 'Устойчивое Финансирование',
        'kk': 'Тұрақты Қаржыландыру',
        'en': 'Sustainable Finance & Investing',
    },
}


def default_genre_preferences():
    return list(ESG_SUBGENRES)


def lemmatizateRuWord(word: str):
    if word.isascii():
        return word.lower()
    return morph.parse(word)[0].normal_form


def lemmatizateKzWord(word: str):
    if word.isascii():
        return word.lower()
    [iscovered, alist] = analyzer.analyze(word)
    lword = alist[0]
    return lword[:lword.find('_')].lower()


def lemmatizateText(text: str, lang: str):
    table = str.maketrans(dict.fromkeys(string.punctuation))
    text = text.translate(table)

    if lang == 'ru':
        return ' '.join([lemmatizateRuWord(w) for w in text.split()])
    if lang == 'kk':
        return ' '.join([lemmatizateKzWord(w) for w in text.split()])
    return ' '.join([w.lower() for w in text.split()])


def txt_to_list(text):
    return [line.strip() for line in text.strip().splitlines() if line.strip()]


def _keyword_dir(lang: str) -> str:
    return os.path.join(KEYWORD_FILES_DIR, lang)


def _lemmatize_keywords(keywords, lang: str):
    return [lemmatizateText(keyword, lang) for keyword in keywords]


def _text_tokens(text: str, lang: str):
    return lemmatizateText(text, lang).split()


def _keyword_matches_tokens(tokens, keyword: str) -> bool:
    keyword_tokens = keyword.split()
    if len(keyword_tokens) == 1:
        return keyword_tokens[0] in tokens

    for index in range(len(tokens) - len(keyword_tokens) + 1):
        if tokens[index:index + len(keyword_tokens)] == keyword_tokens:
            return True
    return False


def _load_genre_keywords(lang: str):
    genre_dir = _keyword_dir(lang)
    if not os.path.isdir(genre_dir):
        raise ValueError(f"Keyword directory not found for language: {lang}")

    keywords_by_genre = {}
    for filename in sorted(os.listdir(genre_dir)):
        if not filename.endswith('.txt'):
            continue
        genre = filename[:-4]
        path = os.path.join(genre_dir, filename)
        with open(path, 'r', encoding='utf-8') as keyword_file:
            raw_keywords = txt_to_list(keyword_file.read())
        keywords_by_genre[genre] = _lemmatize_keywords(raw_keywords, lang)
    return keywords_by_genre


class EsgSubGenreClassifier:
    def __init__(self, lang: str):
        if lang not in SUPPORTED_KEYWORD_LANGS:
            raise ValueError(f"Unsupported language for sub-genre classification: {lang}")
        self.lang = lang
        self._keywords_by_genre = _load_genre_keywords(lang)

    def classify_news(self, text: str, lang: str):
        if lang != self.lang:
            raise ValueError(
                f"Classifier language '{self.lang}' does not match requested language '{lang}'"
            )

        tokens = _text_tokens(text, lang)
        return [
            genre
            for genre, keywords in self._keywords_by_genre.items()
            if any(_keyword_matches_tokens(tokens, keyword) for keyword in keywords)
        ]


_classifiers = {}


def get_subgenre_classifier(lang: str) -> EsgSubGenreClassifier:
    if lang not in _classifiers:
        _classifiers[lang] = EsgSubGenreClassifier(lang)
    return _classifiers[lang]


def classify_news(text: str, lang: str):
    if lang not in SUPPORTED_KEYWORD_LANGS:
        return []
    return get_subgenre_classifier(lang).classify_news(text, lang)


def should_notify_user(user_preferences, matched_genres) -> bool:
    if not user_preferences or not matched_genres:
        return False
    return bool(set(user_preferences) & set(matched_genres))


def get_esg_subgenres():
    return [
        {
            'id': genre_id,
            'label': ESG_SUBGENRE_LABELS[genre_id],
        }
        for genre_id in ESG_SUBGENRES
        if genre_id in ESG_SUBGENRE_LABELS
    ]


def get_esg_genres():
    return get_esg_subgenres()


def classify_esg_genres(text: str, lang: str):
    return classify_news(text, lang)


def matches_esg_genres(text: str, lang: str, genre_ids=None) -> bool:
    matched = classify_news(text, lang)
    if not genre_ids:
        return bool(matched)
    return should_notify_user(genre_ids, matched)


class KeywordsFiltration:
    def __init__(self, lang: str):
        if lang not in SUPPORTED_KEYWORD_LANGS:
            raise ValueError(f"Unsupported language for keyword filtration: {lang}")
        self.lang = lang
        self._classifier = get_subgenre_classifier(lang)

    def EsgKeyWordCheck(self, text, lang):
        if lang not in SUPPORTED_KEYWORD_LANGS:
            return False
        return bool(get_subgenre_classifier(lang).classify_news(text, lang))
