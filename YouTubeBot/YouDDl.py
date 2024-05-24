from yt_dlp import YoutubeDL

def split_name(title_n: str):
    text_name = ''
    for i in title_n:
        if i in '\/:*?"<>#|@.,':
            continue
        text_name += i
    return text_name

def Download_vid(url: str):
    try:
        ydl_opts = {
            'quiet': True,
            'format': 'mp4',
            'no_warnings': True
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            size_info = round((info['filesize_approx']/1024)/1024, 2)
        if size_info > 49:
            print(f'Fail to Big: {size_info}')
            return f'big'
        else:
            ydl_opts['outtmpl']['default'] = f'videos/{split_name(info["title"])}.mp4'
            ydl.download([url])
            print(f"{ydl_opts['outtmpl']['default']} size {size_info}")
            return ydl_opts['outtmpl']['default']
    except Exception as err:
        print(err)
        return 'Er'

# Download_vid('https://youtube.com/shorts/VNpFR1ow-3U?si=429A7X6-oCCI5-Wb')
