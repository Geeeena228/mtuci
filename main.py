import telebot
from telebot import types

token = "2127285808:AAE5-RBAZXOhTrk72o4UXRJXfFAXvU-ucQo"

bot = telebot.TeleBot(token)

name = ''
surname = ''
age = 0

@bot.message_handler(commands=[ 'start', 'help' ])
def send_welcome(message):
    bot.reply_to(message, 'how are you doing')

@bot.message_handler(func=lambda m:True)
def echo_all(message):
    if message.text == 'Привет':
        bot.reply_to(message, 'Привет! Давай познакомимся! Как тебя зовут?')
    elif message.text == '/reg':
        bot.send_message(message.from_user.id, 'как тебя зовут')
        bot.register_next_step_handler(message, reg_name) # переходим к следующей функции

def reg_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Введите фамилию')
    bot.register_next_step_handler(message, reg_surname)

def reg_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Сколько лет')
    bot.register_next_step_handler(message, reg_age)

def reg_age(message):
    global age
    #age = message.text
    while age == 0:
        try:
            age = int(message.text)
        except Exception:
            bot.send_message(message.from_user.id, 'Вводите цифрами')
    keybord = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keybord.add(key_yes)#добавляем клавишу на экран да
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keybord.add(key_no)
    question = 'Тебе' + str(age) + "Зовут" + str(name) + ' ' + str(surname)
    bot.send_message(message.from_user.id, text = question, reply_markup=keybord)  # выводим все что получили через переменную. replay_keydoard передает ответ на клавиатуру

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, "Теперь запишу в БД!")
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Попробуем еще раз!")
        bot.send_message(call.message.chat.id, "Привет! Давай познакомимся! Как тебя зовут?")
        bot.register_next_step_handler(call.message, reg_name)


bot.polling()