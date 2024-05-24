import telebot
from config import TOKEN
# from youtube_d import Download_vid
from YouDDl import Download_vid


bot_p = telebot.TeleBot(TOKEN)

start_text = 'Тебя приветствует бот для загрузки Шотсов из YouTube\n Для загрузки вставь ссылку на видео \n или поделись ею в бот из приложения YouTube'

@bot_p.message_handler(commands=['start'])
def start_mess(message):
    bot_p.send_message(message.chat.id, f'{start_text}')


@bot_p.message_handler(commands=['help'])
def help_mess(message):
    help_text = """
    В настоящий момент бот поддерживает загрузку только коротких видео\n
    К сожалению некоторые видео не удается скачать так как автор видео может поставить запрет\n
    Т
    """
    bot_p.send_message(message.chat.id, help_text)


@bot_p.message_handler(content_types=['text'])
def ganre_repl(message):
    if message.text.startswith('http'):
        try:
            bot_p.send_message(message.chat.id, 'Перед загрузкой проверим какого размера файл видео и нет ли ограничений')
            s = Download_vid(message.text)
            if s == 'big':
                bot_p.send_message(message.chat.id, 'Размер файла превышает 50 MB')
            elif s == 'Er':
                bot_p.send_message(message.chat.id, 'Ошибка скачивания файла, возможен запрет автора')
            else:
                with open(s, 'rb') as file:
                    f = file.read()
                bot_p.send_document(message.chat.id, document=f, visible_file_name=s)
        except:
            sorry_text = 'К сожалению видео видео большого размера я на могу скачать'
            print('ERROR')
            bot_p.send_message(message.chat.id, 'Извините что-то пошло не так. Попробуйте другое видео :(')


bot_p.polling()