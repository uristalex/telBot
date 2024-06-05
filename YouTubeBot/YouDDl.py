import os
import shutil
from pathlib import Path
from yt_dlp import YoutubeDL


limit_vid_size: float = 100
total_vid_size: float = 0


def split_name(title_n: str) -> str:
    """Функция удаления специальных символов\n принимает строку для преобразования
    """
    return ''.join([i for i in title_n if i not in '\/:*?"<>#|@.,;' ])


def folder_size(path: str)-> float:
    """Функция подсчета размера папки для временного хранения файлов\n
    необходима для контроля объема загружаемых данных\n
    Параметры:\n
    path: str - принимает имя папки(путь) где хранятся файлы для подсчета"""
    return round((sum([os.path.getsize(i) for i in Path(path).rglob('*')])/1024)/1024, 2)

def delete_everything_in_folder(folder_path):
    shutil.rmtree(folder_path)
    os.mkdir(folder_path)


def download_vid(url: str, sefe_server: bool = False) -> str:
    """
    Функция загрузки видео
    Принимает ссылку на видео и параметр для сохранения на сервере без загрузки в Теллеграм

    Параметры:

    url: ссылка на видео\n
    sefe_server: принимает False/True

    Результат:

    Строка с именем файла для дальнейшей обработки в боте.
    """
    global total_vid_size
    flag: str = ''
    ydl_opts = dict(quiet=True, format='mp4', no_warnings=True)
    if total_vid_size == 0:
        total_vid_size = folder_size('videos')
    if total_vid_size > limit_vid_size:
        delete_everything_in_folder('videos')
        total_vid_size = 0
        print('deleted')
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        if sefe_server:
            ydl_opts['outtmpl']['default'] = f'server/videos/{split_name(info["title"])}.mp4'
            ydl.download([url])
            print(f"{ydl_opts['outtmpl']['default']} safe_server")
            flag = f'server'
        size_info = round((info['filesize_approx'] / 1024) / 1024, 2)
        if size_info > 49:
            print(f'Fail to Big: {size_info}')
            flag = f'big'
        else:
            ydl_opts['outtmpl']['default'] = f'videos/{split_name(info["title"])}.mp4'
            ydl.download([url])
            total_vid_size += size_info
            print(f"{ydl_opts['outtmpl']['default']} size {size_info}")
            flag = ydl_opts['outtmpl']['default']
    except Exception as err:
        print(err)
        flag = 'Er'

    print(total_vid_size)
    return flag

# download_vid('https://youtube.com/shorts/VNpFR1ow-3U?si=429A7X6-oCCI5-Wb')
