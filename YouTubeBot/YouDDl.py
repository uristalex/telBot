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
            'quiet': True,
            'format': '[filesize<100M]',
            'no_warnings': True
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            ydl_opts['outtmpl']['default'] = f'videos/{split_name(info["title"])}.mp4'
        ydl.download([url])
        return ydl_opts['outtmpl']['default']
    except Exception as err:
        print(err)
        return 'Er'

Download_vid('https://youtu.be/kLtodiGQpuY?si=uEfFU-2OvnnMZWUe')
