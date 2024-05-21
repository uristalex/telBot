import os
from yt_dlp import YoutubeDL

def split_name(title_n: str):
    text_name = ''
    for i in title_n:
        if i in '\/:*?"<>#|.,':
            continue
        text_name += i
    return text_name

def Download_vid(url: str):
    try:
        ydl_opts = {
            # 'outtmpl': f'%(title)s.%(ext)s',
            'outtmpl': f'%(id)s.%(ext)s',
            'quiet': True,
            'no_warnings': True
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            ydl.download([url])
        old_name = f'{info["id"]}.mp4'
        new_name = f'{split_name(info["title"])}.mp4'
        if os.path.exists(new_name):
            return f'{new_name}'
        else:
            os.renames(old_name, new_name)
            return f'{new_name}'

    except Exception as err:
        print(err)
        return 'error'

Download_vid('https://youtube.com/shorts/1avI5l__3HY?si=xMFg_GfWgX5GMDO6')
