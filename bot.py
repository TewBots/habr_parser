import json
import time
from config import API
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from main import get_news, check_news_update
from dev import get_dev_news
from admin import get_admin_news


bot = Bot(token=API, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    start_buttons = ['Все', 'Последнии пять', 'Новые', 'Темы', 'Кар']
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.add(*start_buttons)
    await message.answer("Лента новостей", reply_markup=keyboard)


@dp.message_handler(Text(equals="Все"))
async def get_all_news(message: types.Message):
    await message.answer("Подождите идет обновление")
    get_news()
    get_admin_news()
    get_dev_news()
    with open("news_dict.json", encoding='utf8') as file:
        news_dict = json.load(file)

    for k, v in news_dict.items():
        news = f"<b>{v['articles_title']}</b>" \
               f"<u>\n{v['articles_url']}</u>"
        await message.answer(news)


@dp.message_handler(Text(equals="Последнии пять"))
async def get_last_five_news(message: types.Message):
    await message.answer("Подождите идет обновление")
    get_news()
    with open("news_dict.json", encoding='utf8') as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[-5:]:
        news = f"{v['articles_title']}" \
               f"\n{v['articles_url']}"
        await message.answer(news)

@dp.message_handler(Text(equals="Новые"))
async def get_fresh_news(message: types.Message):
    fresh_news = check_news_update()

    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items()):
            news = f"{v['articles_title']}" \
                   f"\n{v['articles_url']}"
            await message.answer(news)
    else:
        await message.answer("Нету свежих новостей")

@dp.message_handler(Text(equals="Темы"))
async def get_all_news(message: types.Message):
    button = ['Разработка', 'Администрирование', 'Дизайн', 'Манеджмент', 'Маркетинг', 'Ноучпоп', 'Назад']
    keyboards = types.ReplyKeyboardMarkup()
    keyboards.add(*button)
    await message.answer("Лента новостей", reply_markup=keyboards)

@dp.message_handler(Text(equals="Разработка"))
async def get_last_five_news(message: types.Message):
    with open("json/dev_ready.json", encoding='utf8') as file:
        news_dict = json.load(file)
    get_dev_news()

    for k, v in sorted(news_dict.items()):
        news = f"{v['articles_title']}" \
               f"\n{v['articles_url']}"
        await message.answer(news)

@dp.message_handler(Text(equals="Назад"))
async def send_welcome(message: types.Message):
    start_buttons = ['Все', 'Последнии пять', 'Новые', 'Темы', 'Кар']
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.add(*start_buttons)
    await message.answer("Лента новостей", reply_markup=keyboard)

@dp.message_handler(Text(equals="Администрирование"))
async def get_news_theme_admin(message: types.Message):
    get_admin_news()
    print(get_admin_news())
    with open("json/admin_ready.json", encoding='utf8') as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items()):
        news = f"{v['articles_title']}" \
               f"\n{v['articles_url']}"
        await message.answer(news)
        time.sleep(3)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)