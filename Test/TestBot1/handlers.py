from AdditionalFunctions import ProperErrorName

from aiogram import types, Router
from aiogram.filters import Command
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from configs import TELEGRAM_BOT_TOKEN, siteDomain, OurSite
import requests


router1 = Router()
bot = Bot(token=TELEGRAM_BOT_TOKEN)

@router1.message(Command("do"))
async def do_command(message: types.Message):
    js = requests.get(f"{siteDomain}/api/v1/RecentArticles/").json()
    for a in js:
        text = a['title'] + '\n\n' + a['digest'] + '\n\n' + f'<a href="{OurSite}">Посетите наш сайт👈👈👈</a>'
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Читать", url=a['ar_site_url'])]
        ])
        if a['image_url']:
            await bot.send_photo('-1002584155352', photo=a['image_url'], caption=text, parse_mode='html', reply_markup=kb)
        else: await bot.send_message('-1002584155352', text, parse_mode='html', reply_markup=kb)

@router1.message(Command("start"))
async def start_command(message: types.Message):
    """Обработчик команды /start."""
    startText = f'''Привет. Это бот для доп работы с сайтом {siteDomain}
Каждый день будут отправляться уведомления о колличестве багов при парсинге, а так же объем для инспекции фильтрации данных.

Доступные команды:
/error - Список багов
/ArticlesToFilter - Список статей для фильтрации
/ProjectsToFilter - Список проектов для фильтрации
/EventsToFilter - Список событий для фильтрации
/CoursesToFilter - Список курсов для фильтрации'''

    await message.answer(startText)


def ErrorButtons(link):
    ErrorsJson = requests.get(f"{link}").json()
    ErrorsJson2 = ErrorsJson['results']

    ErrorList = [{'id': Error['id'], 'errorname': ProperErrorName(Error), 'errorText': Error['ErrorText']} for Error in
                 ErrorsJson2]

    buttons = [[InlineKeyboardButton(text=Error['errorname'], callback_data=f"err{Error['id']}")] for Error in
               ErrorList]

    BackForwardButtons = []
    if ErrorsJson['previous'] != None:
        BackForwardButtons.append(InlineKeyboardButton(text="Назад", callback_data=f"ErrPage{ErrorsJson['previous']}"))
    if ErrorsJson['next'] != None:
        BackForwardButtons.append(InlineKeyboardButton(text="Вперёд", callback_data=f"ErrPage{ErrorsJson['next']}"))

    buttons.append(BackForwardButtons)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router1.message(Command("error"))
async def ParsingErrors(message: types.Message):
    await message.answer("Выберите ошибку", reply_markup=ErrorButtons(f"{siteDomain}/api/v1/Errors/"))

@router1.callback_query(lambda c: c.data.startswith("ErrPage"))
async def process_callback_Errpage(callback_query: types.CallbackQuery):
    Page = callback_query.data[7:]
    await bot.send_message(callback_query.from_user.id, "Выберите ошибку", reply_markup=ErrorButtons(Page))


@router1.callback_query(lambda c: c.data.startswith("err"))
async def process_callback_err(callback_query: types.CallbackQuery):
    ErrorID = callback_query.data[3:]
    ErrorJson = requests.get(f"{siteDomain}/api/v1/Errors/{ErrorID}").json()
    ErrorInfo = (ProperErrorName({'ParsedSite': ErrorJson['ParsedSite'], 'ErrorDate': ErrorJson['ErrorDate']}) +
                 '\n\n' + ErrorJson['ErrorText'])
    await bot.send_message(callback_query.from_user.id, ErrorInfo)

def ArticleButtons(link):
    ArticlesJson = requests.get(f"{link}").json()
    Article = ArticlesJson['results']

    if len(Article) > 0:
        Article = Article[0]
        articleId = Article['id']
        messageText = f"{Article['esgScore']}/10 ESG очков\n\n{Article['title']}\n\n{Article['digest']}\n\n{Article['ar_site_url']}\n\nВсего на проверку осталось {ArticlesJson['count']} статей"

        Buttons = []
        if ArticlesJson['previous'] != None:
            Buttons.append(InlineKeyboardButton(text="Назад", callback_data=f"ArtPage{ArticlesJson['previous']}"))

        Buttons.append(InlineKeyboardButton(text="Одобрить", callback_data=f"ArtAct{siteDomain}/api/v1/Approve/Article/{articleId}/"))
        Buttons.append(InlineKeyboardButton(text="Отклонить", callback_data=f"ArtAct{siteDomain}/api/v1/Disapprove/Article/{articleId}/"))

        if ArticlesJson['next'] != None:
            Buttons.append(InlineKeyboardButton(text="Вперёд", callback_data=f"ArtPage{ArticlesJson['next']}"))

        return {'buttons': InlineKeyboardMarkup(inline_keyboard=[Buttons,]), 'message': messageText}
    return {'buttons': InlineKeyboardMarkup(inline_keyboard=[]), 'message': "Нет статей"}

@router1.message(Command("ArticlesToFilter"))
async def articles_command(message: types.Message):
    ab = ArticleButtons(f"{siteDomain}/api/v1/ArticlesToFilter/")
    await message.answer(ab['message'], reply_markup=ab['buttons'])

@router1.callback_query(lambda c: c.data.startswith("ArtPage"))
async def process_callback_Artpage(callback_query: types.CallbackQuery):
    Page = callback_query.data[7:]
    ab = ArticleButtons(f"{Page}")
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id

    await bot.delete_message(chat_id, message_id)
    await bot.send_message(callback_query.from_user.id, ab['message'], reply_markup=ab['buttons'])

@router1.callback_query(lambda c: c.data.startswith("ArtAct"))
async def process_callback_ArtAct(callback_query: types.CallbackQuery):
    link = callback_query.data[6:]
    result = ""
    print(link)
    if "Approve" in link:
        result = requests.post(link).json()['message']
    elif "Disapprove" in link:
        result = requests.delete(link).json()['message']

    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id

    await bot.delete_message(chat_id, message_id)
    await bot.send_message(callback_query.from_user.id, f"Статья обработана ({result})")

    ab = ArticleButtons(f"{siteDomain}/api/v1/ArticlesToFilter/")
    await bot.send_message(callback_query.from_user.id, ab['message'], reply_markup=ab['buttons'])

