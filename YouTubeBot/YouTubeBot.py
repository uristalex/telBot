from telebot import TeleBot
from config import TOKEN
# from youtube_d import Download_vid
from YouDDl import download_vid

bot_p = TeleBot(TOKEN)
start_text = 'Тебя  приветствует бот для загрузки Шотсов из YouTube\nДля загрузки вставь ссылку на видео \nили поделись ею в бот из приложения YouTube'


@bot_p.message_handler(commands=['start'])
def start_mess(message):
    bot_p.send_message(message.chat.id, f'{start_text}')


@bot_p.message_handler(commands=['error'])
def error_mes(message):
    error_text = ('YouTube имеет возможность ограничивать использования своего контента на других платформах'
                  'в связи с чем отдельные ролики не могут быть скачаны.')
    bot_p.send_message(message.chat.id, error_text)


@bot_p.message_handler(commands=['help'])
def help_mess(message):
    help_text: str = ('В настоящий момент бот поддерживает загрузку только коротких видео\n'
                      'К сожалению некоторые видео не удается скачать так как автор видео может поставить запрет\n')
    bot_p.send_message(message.chat.id, help_text)


@bot_p.message_handler(commands=['help_bot'])
def help_bot(message):
    bot_donate: str = 'Если хотите поддержать развитие БОТА приобретите себе сервер по моей рефферальной ссылке: https://zomro.com/vds?from=4824 '
    bot_p.send_message(message.chat.id, bot_donate)


@bot_p.message_handler(content_types=['text'])
def ganre_repl(message):
    if message.text.startswith('s'):
        download_vid(message.text.lstrip('s'), True)
        bot_p.send_message(message.chat.id, 'загружено на сервер')
    elif message.text.startswith('http') and ('shorts' in message.text):
        try:
            bot_p.send_message(message.chat.id,
                               'Перед загрузкой проверим какого размера файл видео и нет ли ограничений')
            s = download_vid(message.text, False)
            if s == 'big':
                bot_p.send_message(message.chat.id, 'Размер файла превышает 50 MB')
            elif s == 'Er':
                bot_p.send_message(message.chat.id, 'Ошибка скачивания файла, возможен запрет автора')
            else:
                with open(s, 'rb') as file:
                    f = file.read()
                bot_p.send_document(message.chat.id, document=f, visible_file_name=s)
        except:
            print('ERROR')
            bot_p.send_message(message.chat.id, 'Извините что-то пошло не так. Попробуйте другое видео :(')
    else:
        bot_p.send_message(message.chat.id, 'Вставьте корректную ссылку')

bot_p.polling()
