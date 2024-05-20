from pytube import YouTube


def Download_vid(link):
    yt1 = YouTube(link)
    yt = yt1.streams.get_highest_resolution()
    title_vid = yt.title
    for c in '\/:*?"<>#|.,':
        title_vid = title_vid.replace(c, '')
    try:
        if yt.filesize_mb > 49:
            text_mess = 'big'
        else:
            yt.download(filename=f'{title_vid}.mp4')
            text_mess = f'{title_vid}.mp4'
    except:
        print("An error has occurred")
        text_mess = 'Er'
    return text_mess






