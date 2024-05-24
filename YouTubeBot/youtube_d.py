from pytube import YouTube

def split_name(title_n: str):
    text_name = ''
    for i in title_n:
        if i in '\/:*?"<>#|.,':
            continue
        text_name += i
    return text_name


def Download_vid(link):
    yt1 = YouTube(link)
    yt = yt1.streams.get_highest_resolution()
    print(yt)
    title_vid = split_name(yt.title)
    print(yt.filesize_mb)


    try:
        if yt.filesize_mb > 49:
            text_mess = 'big'
        else:
            yt.download(filename=f'{title_vid}.mp4')
            text_mess = f'{title_vid}.mp4'
    except Exception as err:
        print(err)

        text_mess = 'Er'
    return text_mess


Download_vid('https://youtu.be/Dtr-B_bzQi0?si=d9WDwnIP63zGhqNU')





