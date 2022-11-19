import os
import logging
import func

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

API_TOKEN = os.environ["API_TOKEN"]

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# Making keyboard
kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(KeyboardButton('/help'))


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """

    func.new_user(user_id=message.from_user.id)


    greeting = """
                Добрый день.\nЭтот бот предназначени для автоматизации процесса следования за выбранным \
                индесом или стратегей. Бот не использует ничего кроме открытых данных, передаваеммых \
                биражей.\nБот не знает ничего о новостях, экономической и/или политической \
                ситуации, волнах Эллиота и точках входа.\nВсё, что он может - это подсказать как \
                следовать Вашей стратегии, не обращая внимания на новостной фон."""
    greeting = greeting.replace(' '*8, '') # убираем лишние пробелы из-за отсутпов в коде
    await message.answer(greeting)

@dp.message_handler(commands=['help'])
async def show_help(message: types.Message):
    await message.answer(text='answer', reply_markup=kb)



@dp.message_handler(commands=['commands'])
async def show_commands(message: types.Message):
    answer = """/start - старт\n
                /help - хелп\n
                /commands - список комманд
             """
    await message.answer(answer)

@dp.message_handler(commands=['index'])
async def show_index(message: types.Message):
    answer = func.base_index() 
    await message.answer(answer, parse_mode='Markdown')



@dp.message_handler(commands=['price'])
async def show_price(message: types.Message):
    answer = func.shares_price() 
    await message.answer(answer, parse_mode='Markdown')

@dp.message_handler()
async def answ(message: types.Message):

    
    answer = func.message_parsing(message.text)

    #message.from_id - user ID

    # ответ туда откуда написали (из чата в чат, из лички в личку)
    answer = f'<s>{message.text}</s> -> {message.text.upper()}'
    await message.answer(answer, parse_mode='HTML')

    # ответ в личку. ответчать в личку можно только, если юзер сам запустил бота
    #await bot.send_message(message.from_user.id, message.text)


    # ответ на сообщение
    # await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=None, on_shutdown=None)

