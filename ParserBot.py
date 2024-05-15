import telebot
from config import TOKEN
from Pars_for_Bot import spisok_500, rand_popular


bot_p = telebot.TeleBot(TOKEN)
name = ''


@bot_p.message_handler(commands=['start'])
def start_mess(message):
    poem = f'Тебя приветствует бот помощник.\n Введи свое имя и начнем'
    bot_p.send_message(message.chat.id, f'{poem}')
    bot_p.register_next_step_handler(message, reg_name)


    # with open('text.txt', 'a', encoding='utf-8') as f:
    #     print(f'Время: {time_covert(message.date)} {message.from_user.username} написал: {message.text}', file=f)
    #     # print(message)


@bot_p.message_handler(commands=['help'])
def help_mess(message):
    help_text = """
    "Для того чтобы начать введите команду /pusk"\
    "Для получения помощи введите команду /help"\
    "Для того чтобы заново запустить бота введите /start"\
    "При работе с ботом используйте клавиатуру, которая появиться после отправки команды /pusk"
    """
    bot_p.send_message(message.chat.id, help_text)


def key_pusk():
    keyb_markup = telebot.types.ReplyKeyboardMarkup()
    button_genre = telebot.types.KeyboardButton("Жанры фильмов")
    button_rand_popular = telebot.types.KeyboardButton("Случайный фильм из ожидаемых")
    button_rand_500 = telebot.types.KeyboardButton("Случайный фильм из 500 лучших")
    keyb_markup.row(button_genre, button_rand_popular)
    # keyb_markup.row(button_rand_popular)
    keyb_markup.row(button_rand_500)
    return keyb_markup


def key_gener():
    key_g_replay = telebot.types.InlineKeyboardMarkup()
    key_comedy = telebot.types.InlineKeyboardButton(text='Комедии', callback_data='comedy')
    key_fantasy = telebot.types.InlineKeyboardButton(text='Фантастика', callback_data='fantasy')
    key_mult = telebot.types.InlineKeyboardButton(text='Мультфильмы', callback_data='mult')
    key_horror = telebot.types.InlineKeyboardButton(text='Ужасы', callback_data='horror')
    key_g_replay.add(key_comedy, key_fantasy, key_mult, key_horror)
    return key_g_replay


@bot_p.message_handler(commands=['pusk'])
def help_pusk(message):
    bot_p.send_message(message.chat.id,'Поехали!!!', reply_markup=key_pusk())


def reg_name(message):
    global name
    name = message.text
    bot_p.send_message(message.chat.id, f'Hi {name}\nЧтобы начать отправь /pusk\n'
                                            f'Если тебе нужна помощь, то отправь /help')


@bot_p.message_handler(content_types=['text'])
def ganre_repl(message):
    if message.text == "Жанры фильмов":
        bot_p.send_message(message.chat.id, 'Выберите один из жанров: ', reply_markup=key_gener())
    if message.text == "Случайный фильм из ожидаемых":
        n_film, pic_film = rand_popular()
        bot_p.send_photo(message.chat.id, caption=n_film, photo=pic_film)
    if message.text == "Случайный фильм из 500 лучших":
        n_film, pic_film = spisok_500()
        bot_p.send_photo(message.chat.id, photo=pic_film, caption=n_film)





@bot_p.callback_query_handler(func=lambda call: True)
def genre_reply_but(call):
    if call.data == 'comedy':
        bot_p.send_message(call.message.chat.id, 'Вы выбрали случайный фильм из жанра Комедии')
    if call.data == 'fantasy':
        bot_p.send_message(call.message.chat.id, 'Вы выбрали случайный фильм из жанра Фантастика')
    if call.data == 'mult':
        bot_p.send_message(call.message.chat.id, 'Вы выбрали случайный фильм из жанра Мультфильмы')
    if call.data == 'horror':
        bot_p.send_message(call.message.chat.id, 'Вы выбрали случайный фильм из жанра Ужасы')






bot_p.polling()