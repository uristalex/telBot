import datetime as DT
import telebot
from config import TOKEN
# from youtube_d import Download_vid
from YouDDl import download_vid, download_serv

bot_p = telebot.TeleBot(TOKEN)
start_text = 'Тебя  приветствует бот для загрузки YouTube SHOTS. Для загрузки вставь ссылку на видео или поделись ею в бот из приложения YouTube'
CHAT_BY_DATETIME = dict()

@bot_p.message_handler(commands=['start'])
def start_mess(message):
    # bot_p.delete_message(message.chat.id, ) func to delet message
    bot_p.send_message(message.chat.id, f'{start_text}')


@bot_p.message_handler(commands=['error'])
def error_mes(message):
    error_text = ('YouTube имеет возможность ограничивать использования своего контента на других платформах'
                  'в связи с чем отдельные ролики не могут быть скачаны.')
    bot_p.send_message(message.chat.id, error_text)


@bot_p.message_handler(commands=['help'])
def help_mess(message):
    help_text: str = ('В настоящий момент бот поддерживает загрузку только коротких видео.\n'
                      'К сожалению некоторые видео не удается скачать'
                      'так как автор видео может поставить запрет')
    bot_p.send_message(message.chat.id, help_text)


@bot_p.message_handler(commands=['help_bot'])
def help_bot(message):
    bot_donate: str = ('Если хотите поддержать развитие БОТА приобретите'
                       'себе сервер по моей рефферальной ссылке: https://zomro.com/vds?from=4824')
    bot_p.send_message(message.chat.id, bot_donate)




# @bot_p.message_handler(content_types=['text'])
def ganre_repl(message):
    if message.text.startswith('s'):
        download_serv(message.text.lstrip('s'))
        bot_p.send_message(message.chat.id, 'загружено на сервер')
    elif message.text.startswith('http') and ('shorts' in message.text):
        bot_p.delete_message(message.chat.id, message.message_id)
        try:
            bot_p.send_message(message.chat.id,
                               f'Перед загрузкой проверим какого размера файл видео и нет ли ограничений {len(CHAT_BY_DATETIME)}')
            s = download_vid(message.text, False)
            if s == 'big':
                bot_p.send_message(message.chat.id, 'Размер файла превышает 50 MB')
            elif s == 'Er':
                bot_p.send_message(message.chat.id, 'Ошибка скачивания файла, возможен запрет автора')
            else:
                with open(s, 'rb') as file:
                    f = file.read()
                bot_p.send_document(message.chat.id, document=f, visible_file_name=s, caption=f'Предоставленно: https://t.me/YouShots_BOT')
                return True

        except:
            print('ERROR')
            bot_p.send_message(message.chat.id, 'Извините что-то пошло не так. Попробуйте другое видео :(')

    else:
        bot_p.send_message(message.chat.id, 'Вставьте корректную ссылку')


@bot_p.message_handler(func=lambda message: True)
def on_request(message: telebot.types.Message):
    text = ''
    need_seconds = 20
    current_time = DT.datetime.now()
    last_datetime = CHAT_BY_DATETIME.get(message.chat.id)
    if not last_datetime:
        CHAT_BY_DATETIME[message.chat.id] = current_time
        ganre_repl(message)
    else:
        delta_seconds = (current_time - last_datetime).total_seconds()
        seconds_left = int(need_seconds - delta_seconds)
        if seconds_left > 0:
            text = f'Подождите {seconds_left} секунд перед выполнение этой команды'
        else:
            CHAT_BY_DATETIME[message.chat.id] = current_time
            ganre_repl(message)

    if text:
        bot_p.send_message(message.chat.id, text)


if __name__ == "__main__":
    bot_p.polling(none_stop=True)
