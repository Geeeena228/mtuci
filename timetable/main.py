import psycopg2
import telebot
from telebot import types
import datetime

token = '2127285808:AAE5-RBAZXOhTrk72o4UXRJXfFAXvU-ucQo'
bot = telebot.TeleBot(token)


def week_math(message):
    nums = int(datetime.datetime.utcnow().isocalendar()[1])
    if (nums % 2) == 0:
        bot.send_message(message.chat.id,'Сейчас нечетная неделя')
    elif (nums % 2) != 0:
        bot.send_message(message.chat.id, 'Сейчас четная недееля')


@bot.message_handlers(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Расписание')
    bot.send_message(message.chat.id,'Тут Вы можете найти расписание для БФИ2102\nДля ознакомления с полным функционалом нажмите /help', reply_markup=keyboard)


@bot.message_handlers(content_types=['text'])
def mtuci(message):
    if message.text.lower() == '\mtuci':
        bot.send_message(message.chat.id, 'https://mtuci.ru/')