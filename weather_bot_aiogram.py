from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import requests
import time

bot = Bot(token='token')   #ввести токен
dp = Dispatcher(bot, storage=MemoryStorage())


class state(StatesGroup):
    operation1 = State()


@dp.message_handler(commands=['start'])
async def hello(message):
    await message.answer(f'Привет {message.from_user.last_name} {message.from_user.first_name}')
    await message.answer('Я бот, который умеет показывать погоду')
    await message.answer('Введите город')
    await state.operation1.set()


@dp.message_handler(state=state.operation1)
async def operat1(message):
    global a
    a = message.text
    params = {'q': a, 'appid': 'appid',            #appid - ввести api key
              'units': 'metric', 'lang': 'ru'}
    res = requests.get('http://api.openweathermap.org/data/2.5/weather', params=params)
    res = res.json()

    if res['cod'] == '404':
        await message.answer('Пожалуйста введите город')

    elif res['cod'] == 200:
        temp = 'Сейчас : {}℃'.format(int(res['main']['temp']))
        feels_like = 'Ощущается как : {}℃'.format(int(res['main']['feels_like']))
        temp_min = 'Минимальная в городе : {}℃'.format(int(res['main']['temp_min']))
        temp_max = 'Максимальная в городе : {}℃'.format(int(res['main']['temp_max']))
        wind = 'Скорость ветра {}м/c'.format(round(float(res['wind']['speed'])), 1)
        weather = 'На улице - {}'.format(res['weather'][0]['description'])
        sunrise = 'Восход солнца - {}'.format(time.strftime('%X', time.localtime(res['sys']['sunrise'])))
        sunset = 'Заход солнца - {}'.format(time.strftime('%X', time.localtime(res['sys']['sunset'])))
        await message.answer(weather)
        await message.answer(temp)
        await message.answer(feels_like)
        await message.answer(temp_min)
        await message.answer(temp_max)
        await message.answer(wind)
        await message.answer(sunset)
        await message.answer(sunrise)


executor.start_polling(dp)
