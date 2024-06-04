from yt_dlp import YoutubeDL
import os

limit_vid_size: float = 10
total_vid_size: float = 0

def split_name(title_n: str) -> str:
    """Функция удаления специальных символов
    принимает строку для преобразования

    """
    text_name = ''
    for i in title_n:
        if i in '\/:*?"<>#|@.,':
            continue
        text_name += i
    return text_name


# def sum_file_vid(folder: str):
#     size_folder: float = 0
#     for i in os.listdir(folder):
#         size_folder+=os.path.getsize(i)
#     return size_folder



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
    # print(sum_file_vid('videos'))
    ydl_opts = {
        'quiet': True,
        'format': 'mp4',
        'no_warnings': True
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        if sefe_server:
            ydl_opts['outtmpl']['default'] = f'server/videos/{split_name(info["title"])}.mp4'
            ydl.download([url])
            print(f"{ydl_opts['outtmpl']['default']} safe_server")
            return f'server'

        size_info = round((info['filesize_approx'] / 1024) / 1024, 2)
        if size_info:
            print(size_info)
        if size_info > 49:
            print(f'Fail to Big: {size_info}')
            return f'big'
        else:
            ydl_opts['outtmpl']['default'] = f'videos/{split_name(info["title"])}.mp4'
            ydl.download([url])
            total_vid_size += size_info
            print(f"{ydl_opts['outtmpl']['default']} size {size_info}")
            print(total_vid_size)

            return ydl_opts['outtmpl']['default']
    except Exception as err:
        print(err)
        return 'Er'

# download_vid('https://youtube.com/shorts/VNpFR1ow-3U?si=429A7X6-oCCI5-Wb')
