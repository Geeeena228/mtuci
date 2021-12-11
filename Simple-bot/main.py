import telebot
from telebot import types

token = "2139215221:AAHeLDpkg5Mc9XeEAipAtjDsXSsl9v5lnpU"

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    #keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("МТУСИ полезные группы", "/help", "Немного для будущего программиста")
    bot.send_message(message.chat.id, 'Привет! Тут немного полезной информации для учащегося на IT в МТУСИ', reply_markup = keyboard)

@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Я умею....пока ничего')

@bot.message_handler(content_types=['text'])
def MTUCI(message):
    if message.text.lower() == "мтуси полезные группы":
       bot.send_message(message.chat.id, 'Официальная группа в вк https://vk.com/mtuci\nЗа полезной инфой сюда https://vk.com/aktivist_mtuci\nРасслабить мозг https://vk.com/memmtuci')
    if message.text.lower() == "немного для будущего программиста":
        bot.send_message(message.chat.id, 'Книжка по питону  https://codernet.ru/books/python/izuchaem_python_4-e_izdanie_mark_lutc/\nОП  https://python-scripts.com/object-oriented-programming-in-python\nТут можно отработать знания https://www.codewars.com/')

bot.polling()