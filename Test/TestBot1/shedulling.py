import requests
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from configs import siteDomain
from handlers import bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

users = ['704838385']

# Функция для отправки рассылки
async def send_daily_message():
    report_info = requests.get(f'{siteDomain}/api/v1/Report/').json()
    message_text = f'''Уведомление по сегодняшнему парсингу:
    
Колличество ошибок: {report_info['ErrorNumber']}

Данные для фильтрации👇
Колличество статей: {report_info['ArtNumber']}
Колличество курсов: {report_info['CourseNumber']}
Количество мероприятий: {report_info['EventNumber']}
Количество проектов: {report_info['ProjectNumber']}'''

    for user_id in users:
        try:
            await bot.send_message(chat_id=user_id, text=message_text)
        except Exception as e:
            print(e)

# Настройка планировщика
scheduler = AsyncIOScheduler()
scheduler.add_job(
    send_daily_message,
    CronTrigger(hour=9, minute=0, second=0),  # Запуск ежедневно в 9:00:00

    id="daily_message",
    replace_existing=True
)

