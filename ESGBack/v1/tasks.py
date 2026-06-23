from ESGBack.celery import app

from .models import News
from .parsers.GroupedParsers.AllCoursesParsers import Parse_Courses
from .parsers.GroupedParsers.AllEventParsers import Parse_Events
from .parsers.GroupedParsers.AllNewsParsers import Parse_News
from .parsers.GroupedParsers.AllProjectParsers import Parse_Projects
from .services import send_news_notification_email


def run_all_parsers():
    Parse_News()
    Parse_Courses()
    Parse_Projects()
    Parse_Events()


@app.task
def repeat_order_make():
    run_all_parsers()


@app.task
def send_news_email_task(news_id, recipients):
    news = News.objects.get(id=news_id)
    send_news_notification_email(news, recipients)
