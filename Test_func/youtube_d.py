from pytube import YouTube



def Download_vid(link):
    yt1 = YouTube(link)
    yt = yt1.streams.get_highest_resolution()
    title_vid = yt.title
    for c in '\/:*?"<>#|.,':
        title_vid = title_vid.replace(c, '')
    try:
        # print(title_vid)
        yt.download(filename=f'{title_vid}.mp4')
    except:
        print("An error has occurred")
    return f'{title_vid}.mp4'






