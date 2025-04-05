import os
import shutil
from pathlib import Path
from yt_dlp import YoutubeDL


LIMIT_VID_SIZE: float = 100
TOTAL_VID_SIZE: float = 0


def split_name(title_n: str) -> str:
    """
    Функция удаления специальных символов принимает строку для преобразования
    :param title_n: Строка для преобразования
    :return: Строка преобразованная функцией
    """
    return ''.join([i for i in title_n if i not in '\/:*?"<>#|@.,;' ])


def folder_size(path: str)-> float:
    """
    Функция подсчета размера папки для временного хранения файлов
    необходима для контроля объема загружаемых данных.
    :param path: Название папки(путь) где хранятся файлы для подсчета
    :return: Округленное значение размера папки на момент вызова функции
    """
    return round((sum([os.path.getsize(i) for i in Path(path).rglob('*')])/1024)/1024, 2)


def delete_everything_in_folder(folder_path: str)-> None:
    """
    Функция очистки папки для загрузки видео. Нужна для предотвращения выхода за лимиты дискового пространства
    :param folder_path: Папка для загрузки видео и последующей передачи в Бот
    :return: Очистка содержимого папки загрузки видео
    """
    shutil.rmtree(folder_path)
    os.mkdir(folder_path)


def chek_size_total()-> None:
    """
    Функция контроля размера загруженных файлов
    :return:
    """
    global TOTAL_VID_SIZE
    if TOTAL_VID_SIZE == 0:
        TOTAL_VID_SIZE = folder_size('videos')
    if TOTAL_VID_SIZE > LIMIT_VID_SIZE:
        delete_everything_in_folder('videos')
        TOTAL_VID_SIZE = 0
        print('deleted')


def download_serv(url: str) -> str:
    """
    Функция для загрузки видео на сервер
    :param url: адрес видео
    :return: информация о результате работы функции
    """
    flag: str = ''
    ydl_opts = dict(quiet=True, format='mp4', no_warnings=True)
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            ydl_opts['outtmpl']['default'] = f'server/videos/{split_name(info["title"])}.mp4'
            ydl.download([url])
            flag = f'Загружено на сервер'
    except:
        flag = f'Ошибка'
    return flag


def download_vid(url: str) -> str:
    """
    Функция загрузки видео
    Принимает ссылку на видео 
    :param url: ссылка на видео
    :return: Строка с именем файла для дальнейшей обработки в боте.
    """
    global TOTAL_VID_SIZE
    flag: str = ''
    ydl_opts = dict(quiet=True, format='mp4', no_warnings=True)
    chek_size_total()
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        size_info = round((info['filesize_approx'] / 1024) / 1024, 2)
        if size_info > 49:
            print(f'Fail to Big: {size_info}')
            flag = f'big'
        else:
            ydl_opts['outtmpl']['default'] = f'videos/{split_name(info["title"])}.mp4'
            ydl.download([url])
            TOTAL_VID_SIZE += size_info
            print(f"{ydl_opts['outtmpl']['default']} size {size_info}")
            flag = ydl_opts['outtmpl']['default']
    except Exception as err:
        print(err)
        flag = 'Er'
    print(total_vid_size)
    return flag
