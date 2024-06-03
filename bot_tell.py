# Библиотеки
import time
import telebot
from AioTest.config import TOKEN
import sqlite3 as sl
from datetime import datetime, timezone

bot_tell = telebot.TeleBot(TOKEN)
name = ''

con = sl.connect('reports.db')

with con:
    # получаем количество таблиц с нужным нам именем
    data = con.execute("select count(*) from sqlite_master where type='table' and name='reports'")
    for row in data:
        # если таких таблиц нет
        if row[0] == 0:
            # создаём таблицу для отчётов
            with con:
                con.execute("""
                    CREATE TABLE reports (
                        datetime VARCHAR(40) PRIMARY KEY,
                        date VARCHAR(20),
                        id VARCHAR(200),
                        name VARCHAR(200),
                        text VARCHAR(500)
                    );
                """)


# func for message time formated
def time_covert(t):
    return time.strftime("%H:%M:%S %d.%m.%Y", time.localtime(t))


@bot_tell.message_handler(commands=['start'])
def start_mess(message):
    bot_tell.send_message(message.chat.id, f'Hi my dear friends!')
    markup = telebot.types.ReplyKeyboardMarkup()
    btn1 = telebot.types.KeyboardButton('Hi')
    btn2 = telebot.types.KeyboardButton('11')
    btn3 = telebot.types.KeyboardButton('aiwiwiwa')
    markup.row(btn1, btn2, btn3)

    bot_tell.send_message(message.chat.id, 'hi', reply_markup=markup)






@bot_tell.message_handler(content_types=['text'])
def hello_mess(message):
    con = sl.connect('reports.db')
    # подготавливаем запрос
    sql = 'INSERT INTO reports (datetime, date, id, name, text) values(?, ?, ?, ?, ?)'
    # получаем дату и время
    now = datetime.now(timezone.utc)
    # и просто дату
    date = now.date()
    # формируем данные для запроса
    data = [
        (str(now), str(date), str(message.from_user.id), str(message.from_user.username), str(message.text[:500]))
    ]
    # добавляем с помощью запроса данные
    with con:
        con.executemany(sql, data)
    # отправляем пользователю сообщение о том, что отчёт принят
    bot_tell.send_message(message.from_user.id, 'Принято, спасибо!', parse_mode='Markdown')
    if message.text == 'Hi':
        bot_tell.send_message(
            message.chat.id,
            f'Hi my friends {message.chat.first_name.capitalize()}',
            reply_to_message_id=message.id
            )
        bot_tell.send_message(message.chat.id, f'Hay you name')
        bot_tell.register_next_step_handler(message, reg_name)



def reg_name(message):
    global name
    name = message.text
    bot_tell.send_message(message.chat.id, f'Hi {name}')
    my_keyb = telebot.types.InlineKeyboardMarkup()
    key_1 = telebot.types.InlineKeyboardButton(text='>18', callback_data='1')
    key_2 = telebot.types.InlineKeyboardButton(text='<18', callback_data='2')
    my_keyb.add(key_1)
    my_keyb.add(key_2)
    bot_tell.send_message(
        message.chat.id,
        'hayare you',
        reply_markup=my_keyb
    )


@bot_tell.callback_query_handler(func=lambda call: True)
def call_keyb(call):
    if call.data == '1':
        bot_tell.send_message(call.message.chat.id, f'{name} you old')
    else:
        bot_tell.send_message(call.message.chat.id, f'{name} you soy yang')


@bot_tell.message_handler(commands=['help'])
def help_mess(message):
    bot_tell.send_message(message.chat.id, f'Oooppps {message.chat.first_name} ')





bot_tell.infinity_polling()
