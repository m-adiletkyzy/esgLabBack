from types import SimpleNamespace
from unittest.mock import MagicMock, Mock, patch

from django.test import SimpleTestCase

from v1.parsers.ESGfilters import (
    filter_esg_items,
    is_esg_content,
    is_esg_content_for_genres,
    isESGRu,
)
from v1.parsers.NlpMethods import (
    EsgSubGenreClassifier,
    classify_esg_genres,
    classify_news,
    get_esg_genres,
    get_esg_subgenres,
    matches_esg_genres,
    should_notify_user,
)
from v1.parsers.EventParsers.AtamekenKzEventParser import Parse_AtamekenKzEnEvents, Parse_AtamekenKzRuEvents
from v1.parsers.NewsParsers.GovkznewsParser import Parse_GovkznewsKz, Parse_GovkznewsRu
from v1.parsers.NewsParsers.InformkzParser import Parse_informkzRuNews


class EsgFilterHelpersTests(SimpleTestCase):
    def test_is_esg_ru_detects_sustainable_development(self):
        self.assertTrue(isESGRu('Компания развивает устойчивое развитие'))
        self.assertFalse(isESGRu('Обычная новость о спорте'))

    def test_is_esg_content_russian_keywords(self):
        self.assertTrue(is_esg_content('Новая программа по экологии', 'ru'))
        self.assertFalse(is_esg_content('Результаты футбольного матча', 'ru'))

    def test_is_esg_content_kazakh_keywords(self):
        self.assertTrue(is_esg_content('тұрақты даму жобасы', 'kk'))
        self.assertFalse(is_esg_content('футбол чемпионаты', 'kk'))

    def test_is_esg_content_english_keywords(self):
        self.assertTrue(is_esg_content('New sustainability report published', 'en'))
        self.assertFalse(is_esg_content('Local sports league update', 'en'))

    def test_filter_esg_items_keeps_only_matching_objects(self):
        items = [
            SimpleNamespace(title='ESG Forum', digest='climate action'),
            SimpleNamespace(title='Tax update', digest='corporate reporting'),
        ]
        filtered = filter_esg_items(items, 'en')
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].title, 'ESG Forum')


class EsgSubGenreClassifierTests(SimpleTestCase):
    def test_get_esg_subgenres_returns_five_categories(self):
        genres = get_esg_subgenres()
        self.assertEqual(len(genres), 5)
        self.assertEqual(genres[0]['id'], 'climate')
        self.assertEqual(genres[0]['label']['ru'], 'Экология и Климат')
        self.assertEqual(get_esg_genres(), genres)

    def test_classifier_loads_txt_files_from_language_folder(self):
        classifier = EsgSubGenreClassifier('ru')
        self.assertEqual(
            set(classifier._keywords_by_genre.keys()),
            {'climate', 'waste', 'labor', 'ethics', 'finance'},
        )

    def test_classify_climate_ru(self):
        genres = classify_news('Запуск солнечной электростанции снижает выбросы', 'ru')
        self.assertIn('climate', genres)
        self.assertNotIn('labor', genres)

    def test_classify_waste_kk(self):
        genres = classify_news('Қалдықтарды өңдеу және су ресурстары', 'kk')
        self.assertIn('waste', genres)

    def test_classify_labor_ru(self):
        genres = classify_news('Забастовка из-за зарплаты и безопасности труда', 'ru')
        self.assertIn('labor', genres)

    def test_classify_ethics_ru(self):
        genres = classify_news('Расследование коррупции и взятки в совете директоров', 'ru')
        self.assertIn('ethics', genres)

    def test_classify_finance_ru(self):
        genres = classify_news('Выпуск зеленых облигаций и инвестиционный фонд', 'ru')
        self.assertIn('finance', genres)

    def test_classify_multiple_genres(self):
        genres = classify_news(
            'Грант на солнечную энергетику и переработку отходов',
            'ru',
        )
        self.assertIn('climate', genres)
        self.assertIn('waste', genres)
        self.assertIn('finance', genres)

    def test_whole_word_matching_avoids_partial_token_matches(self):
        genres = classify_news('Монтаж электрической проводки на заводе', 'ru')
        self.assertNotIn('waste', genres)

    def test_should_notify_user_requires_overlap(self):
        self.assertTrue(should_notify_user(['climate', 'waste'], ['climate']))
        self.assertTrue(should_notify_user(['climate', 'waste'], ['finance', 'waste']))
        self.assertFalse(should_notify_user(['climate'], ['finance']))
        self.assertFalse(should_notify_user([], ['climate']))
        self.assertFalse(should_notify_user(['climate'], []))

    def test_matches_esg_genres_with_selection(self):
        text = 'Новая программа субсидий для ветровой энергетики'
        self.assertTrue(matches_esg_genres(text, 'ru', ['climate']))
        self.assertTrue(matches_esg_genres(text, 'ru', ['climate', 'labor']))
        self.assertFalse(matches_esg_genres(text, 'ru', ['labor']))

    def test_classify_esg_genres_alias(self):
        self.assertEqual(
            classify_esg_genres('Солнечная электростанция снижает выбросы', 'ru'),
            classify_news('Солнечная электростанция снижает выбросы', 'ru'),
        )

    def test_is_esg_content_for_genres_uses_genre_keywords_when_selected(self):
        labor_text = 'Забастовка из-за зарплаты на заводе'
        climate_text = 'Солнечная электростанция снижает углеродный выброс'

        self.assertTrue(is_esg_content_for_genres(labor_text, 'ru', ['labor']))
        self.assertTrue(is_esg_content_for_genres(climate_text, 'ru', ['climate']))
        self.assertFalse(is_esg_content_for_genres(labor_text, 'ru', ['climate']))
        self.assertFalse(is_esg_content_for_genres(climate_text, 'ru', ['labor']))

    def test_filter_esg_items_by_genre(self):
        items = [
            SimpleNamespace(title='Солнечная станция', digest='снижение выбросов'),
            SimpleNamespace(title='Забастовка', digest='требования по зарплате'),
        ]
        climate_only = filter_esg_items(items, 'ru', ['climate'])
        labor_only = filter_esg_items(items, 'ru', ['labor'])

        self.assertEqual(len(climate_only), 1)
        self.assertEqual(climate_only[0].title, 'Солнечная станция')
        self.assertEqual(len(labor_only), 1)
        self.assertEqual(labor_only[0].title, 'Забастовка')


class AtamekenKzEventParserFilterTests(SimpleTestCase):
    def _mock_response(self, results):
        response = Mock()
        response.raise_for_status = Mock()
        response.json.return_value = {'results': results}
        return response

    @patch('v1.parsers.EventParsers.AtamekenKzEventParser.requests.get')
    def test_ru_events_filtered_by_esg_keywords(self, mock_get):
        mock_get.return_value = self._mock_response(
            [
                {
                    'title': {'ru': 'Форум устойчивого развития'},
                    'content': {'ru': '<p>Обсуждение ESG повестки</p>'},
                    'image': {},
                    'slug': 'esg-forum',
                    'display_date': '2025-06-01',
                },
                {
                    'title': {'ru': 'Налоговый семинар'},
                    'content': {'ru': '<p>Налоговое планирование для бизнеса</p>'},
                    'image': {},
                    'slug': 'tax-seminar',
                    'display_date': '2025-06-01',
                },
            ]
        )

        events = Parse_AtamekenKzRuEvents()

        self.assertEqual(len(events), 1)
        self.assertIn('устойчив', events[0].title.lower())

    @patch('v1.parsers.EventParsers.AtamekenKzEventParser.requests.get')
    def test_en_events_filtered_by_esg_keywords(self, mock_get):
        mock_get.return_value = self._mock_response(
            [
                {
                    'title': {'en': 'Sustainability business forum'},
                    'content': {'en': '<p>Climate and ESG topics</p>'},
                    'image': {},
                    'slug': 'sustainability-forum',
                    'display_date': '2025-06-01',
                },
                {
                    'title': {'en': 'Accounting workshop'},
                    'content': {'en': '<p>Tax reporting basics</p>'},
                    'image': {},
                    'slug': 'accounting-workshop',
                    'display_date': '2025-06-01',
                },
            ]
        )

        events = Parse_AtamekenKzEnEvents()

        self.assertEqual(len(events), 1)
        self.assertIn('Sustainability', events[0].title)


class GovkznewsParserFilterTests(SimpleTestCase):
    def _article(self, title, body):
        return {
            'title': title,
            'body': f'<p>{body}</p>',
            'id': 1,
            'created_date': '2025-06-01T12:00:00Z',
        }

    @patch('v1.parsers.NewsParsers.GovkznewsParser.requests.get')
    def test_ru_news_filtered_by_esg_keywords(self, mock_get):
        mock_get.return_value = Mock(
            json=Mock(
                return_value={
                    'content': [
                        self._article('Зеленая экономика', 'Развитие экологии в регионе'),
                        self._article('Спортивные соревнования', 'Итоги городского турнира'),
                    ]
                }
            )
        )

        articles = Parse_GovkznewsRu()

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, 'Зеленая экономика')

    @patch('v1.parsers.NewsParsers.GovkznewsParser.requests.get')
    def test_kz_news_filtered_by_esg_keywords(self, mock_get):
        mock_get.return_value = Mock(
            json=Mock(
                return_value={
                    'content': [
                        self._article('Тұрақты даму жобасы', 'Экология саласындағы жаңалықтар'),
                        self._article('Спорт жаңалықтары', 'Чемпионат нәтижелері'),
                    ]
                }
            )
        )

        articles = Parse_GovkznewsKz()

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, 'Тұрақты даму жобасы')


class InformkzParserFilterTests(SimpleTestCase):
    def _page_html(self, cards_html):
        return f'<html><body>{cards_html}</body></html>'

    def _card(self, title, href):
        return f'''
        <div class="catpageCard">
            <div class="catpageCard_title">{title}</div>
            <a href="{href}"></a>
            <div class="catpageCard_time">19:00, 05 Июнь 2025</div>
        </div>
        '''

    @patch('v1.parsers.NewsParsers.InformkzParser.requests.Session')
    def test_ru_news_filtered_by_esg_keywords(self, mock_session_cls):
        page_one = self._page_html(
            self._card('Устойчивое развитие в Казахстане', '/article/esg-news')
            + self._card('Футбольный матч', '/article/football')
        )
        page_two = self._page_html('')

        session = MagicMock()
        session.get.side_effect = [
            Mock(text=page_one),
            Mock(text=page_two),
        ]
        mock_session_cls.return_value = session

        articles = Parse_informkzRuNews(max_pages=5)

        self.assertEqual(len(articles), 1)
        self.assertIn('Устойчивое', articles[0].title)
