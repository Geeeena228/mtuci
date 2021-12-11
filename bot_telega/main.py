import psycopg2
import telebot
from telebot import types
import datetime

token = "2127285808:AAE5-RBAZXOhTrk72o4UXRJXfFAXvU-ucQo"
bot = telebot.TeleBot(token)

chet = 0
chet_week = 1

connection = psycopg2.connect(user="postgres",
                              # пароль, который указали при установке PostgreSQL
                              password="qweasd",
                              host="127.0.0.1",
                              port="5432",
                              database="qwe")
cursor = connection.cursor()


@bot.message_handler(commands=['start'])
def start(message):
    # keyboard = types.ReplyKeyboardMarkup()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Расписание')
    bot.send_message(message.chat.id, 'Тут Вы сможете найти расписание для БФИ2102\n'
                                      'Для ознакомления с полным функционалом нажмите /help', reply_markup=keyboard)
    # bot.register_next_step_handler(message, lesson_schedule)  # переходим к следующей функции


@bot.message_handler(content_types=['text'])
def world(message):
    if message.text.lower() == "/mtuci":
        bot.send_message(message.chat.id, 'https://mtuci.ru/')
    elif message.text.lower() == "/week":
        bot.register_next_step_handler(message, week_math)  # переходим к следующей функции
        # bot.send_message(message.chat.id, 'Пока не сделано')
    elif message.text.lower() == 'расписание':
        bot.register_next_step_handler(message, lesson_schedule)
        # bot
    elif message.text.lower() == "/help":
        bot.send_message(message.chat.id, 'Все возможные команды:\n'
                                          'Расписание - вызывает блок с расписанием\n'
                                          '/mtuci - Отравляет ссылку на официальный сайт МТУСИ\n'
                                          '/week - Показывает четность недели\n/start - Приветсвенное сообщение')
    else:
        bot.send_message(message.chat.id, 'Извините, я Вас не понял')


def week_math(message):
    nums = int(datetime.datetime.utcnow().isocalendar()[1])
    # x = datetime.datetime.now()
    if (nums % 2) == 0:
        chet = 0
        bot.send_message(message.chat.id, 'Сейчас: нечетная неделя')
    if (nums % 2) != 0:
        chet = 1
        bot.send_message(message.chat.id, 'Сейчас: четная неделя')


def lesson_schedule(message):
    keybord = types.InlineKeyboardMarkup()
    key_monday = types.InlineKeyboardButton(text='Понедельник', callback_data='monday')
    keybord.add(key_monday)  # добавляем клавишу на экран понедельник
    key_tuesday = types.InlineKeyboardButton(text='Вторник', callback_data='tuesday')
    keybord.add(key_tuesday)  # добавляем клавишу на экран вторник
    key_wednesday = types.InlineKeyboardButton(text='Среда', callback_data='wednesday')
    keybord.add(key_wednesday)  # добавляем клавишу на экран среда
    key_thursday = types.InlineKeyboardButton(text='Четверг', callback_data='thursday')
    keybord.add(key_thursday)  # добавляем клавишу на экран четверг
    key_friday = types.InlineKeyboardButton(text='Пятница', callback_data='friday')
    keybord.add(key_friday)  # добавляем клавишу на экран пятница
    key_current_week = types.InlineKeyboardButton(text='Расписание на текущую неделю', callback_data='current_week')
    keybord.add(key_current_week)  # добавляем клавишу на экран расписание на текущую неделю
    key_next_weeks = types.InlineKeyboardButton(text='Расписание на следующую неделю', callback_data='next_weeks')
    keybord.add(key_next_weeks)  # добавляем клавишу на экран расписание на следующую неделю
    day = 'Выберите день недели или неделю:'
    bot.send_message(message.from_user.id, text=day, reply_markup=keybord)


@bot.callback_query_handler(func=lambda call: True)
def monday(call):
    if call.data == "monday":
        try:
            cursor.execute("SELECT subject, room_numb, start_time FROM timetable WHERE day = 'Понедельник'")
            result = cursor.fetchall()
            print(result)
            to_print_monday = []
            for i in result:
                to_print_monday.append(', '.join(i) + '\n')
            bot.send_message(call.message.chat.id, ''.join(to_print_monday))
        except:
            bot.send_message(call.message.chat.id, 'Пар нет')

    elif call.data == "tuesday":
        try:
            cursor.execute("SELECT subject, room_numb, start_time FROM timetable WHERE day = 'Вторник'")
            result2 = cursor.fetchall()
            print(result2)
            to_print_tuesday = []
            for i in result2:
                to_print_tuesday.append(', '.join(i) + '\n')
            bot.send_message(call.message.chat.id, ''.join(to_print_tuesday))
        except:
            bot.send_message(call.message.chat.id, 'Пар нет')

    elif call.data == "wednesday":
        try:
            if chet == 0:
                cursor.execute("SELECT subject, room_numb, start_time FROM timetable WHERE day = 'среда'")
                result1 = cursor.fetchall()
                print(result1)
                to_print_wednesday = []
                for i in result1:
                    to_print_wednesday.append(', '.join(i) + '\n')
                bot.send_message(call.message.chat.id, ''.join(to_print_wednesday))
            elif chet == 1:
                cursor.execute("SELECT subject, room_numb, start_time FROM timetable WHERE day = 'среда_нижняя'")
                result1 = cursor.fetchall()
                print(result1)
                to_print_wednesday = []
                for i in result1:
                    to_print_wednesday.append(', '.join(i) + '\n')
                bot.send_message(call.message.chat.id, ''.join(to_print_wednesday))
        except:
            bot.send_message(call.message.chat.id, 'Пар нет')

    elif call.data == "thursday":
        try:
            cursor.execute("SELECT subject, room_numb, start_time FROM timetable WHERE day = 'Четверг'")
            result_thursday = cursor.fetchall()
            print(result_thursday)
            to_print_thursday = []
            for i in result_thursday:
                to_print_thursday.append(', '.join(i) + '\n')
            bot.send_message(call.message.chat.id, ''.join(to_print_thursday))
        except:
            bot.send_message(call.message.chat.id, 'Пар нет')

    elif call.data == "friday":
        try:
            cursor.execute("SELECT subject, room_numb, start_time FROM timetable WHERE day = 'Пятница'")
            result_friday = cursor.fetchall()
            print(result_friday)
            to_print_friday = []
            for i in result_friday:
                to_print_friday.append(', '.join(i) + '\n')
            bot.send_message(call.message.chat.id, ''.join(to_print_friday))
        except:
            bot.send_message(call.message.chat.id, 'Пар нет')

    elif call.data == "current_week":
        if chet_week == chet:
            cursor.execute("SELECT subject, room_numb, start_time FROM timetable WHERE room_numb = 'нижняя' ")
            result_current = cursor.fetchall()
            print(result_current)
            to_print_current = []
            for i in result_current:
                to_print_current.append(', '.join(i) + '\n')
            bot.send_message(call.message.chat.id, ''.join(to_print_current))
        elif chet_week != chet:
            cursor.execute("SELECT subject, room_numb, start_time FROM timetable WHERE week = 'верхняя' ")
            result_current = cursor.fetchall()
            print(result_current)
            to_print_current = []
            for i in result_current:
                to_print_current.append(', '.join(i) + '\n')
            bot.send_message(call.message.chat.id, ''.join(to_print_current))

    elif call.data == "next_weeks":
        if chet_week == chet:
            cursor.execute("SELECT subject, room_numb, start_time FROM timetable WHERE room_numb = 'дома' ")
            result_current = cursor.fetchall()
            print(result_current)
            to_print_current = []
            for i in result_current:
                to_print_current.append(', '.join(i) + '\n')
            bot.send_message(call.message.chat.id, ''.join(to_print_current))
        elif chet_week != chet:
            cursor.execute("SELECT subject, room_numb, start_time FROM timetable WHERE room_numb = 'дома' ")
            result_current = cursor.fetchall()
            print(result_current)
            to_print_current = []
            for i in result_current:
                to_print_current.append(', '.join(i) + '\n')
            bot.send_message(call.message.chat.id, ''.join(to_print_current))


bot.polling()
