
import requests
from bs4 import BeautifulSoup as bs
import random
import time


spisok_f = []
spisok_wait = []
spisok_horror = []
spisok_comedy = []
spisok_fantasy = []
spisok_mult = []
OOPsPoster = 'https://img.freepik.com/premium-vector/ooops-comic-book-explosion-icon-simple-illustration-ooops-comic-book-explosion-vector-icon-web_96318-26126.jpg?w=826'


spisok = {'comedy': (spisok_comedy, 'https://www.kinoafisha.info/rating/movies/comedy/', 'Комедии'),
          'mult': (spisok_mult, 'https://www.kinoafisha.info/rating/movies/animation/', 'Мультфильмы'),
          'horror': (spisok_horror, 'https://www.kinoafisha.info/rating/movies/horror/', 'Ужасы'),
          'fantasy': (spisok_fantasy, 'https://www.kinoafisha.info/rating/movies/sci-fi/', 'Фантастика')}

def time_covert(t):
    return time.strftime("%H:%M:%S %d.%m.%Y", time.localtime(t))


def spisok_500():
    global spisok_f
    if len(spisok_f) == 0:
        for i in (1, 2):
            response_get = requests.get(f'https://www.kinoafisha.info/rating/movies/?page={i}')
            soup = bs(response_get.text, features='html.parser')
            list_films = soup.find_all('a', class_='movieItem_title')
            for film in list_films:
                link_pic = soup.find(alt=f'{film.text}')
                spisok_f.append([film.text, str(link_pic.get('data-picture'))])
        return random.choice(spisok_f)
    else:
        return random.choice(spisok_f)


def rand_popular():
    global spisok_wait
    if len(spisok_wait) == 0:
        response_get = requests.get(f'https://www.kinoafisha.info/rating/releases/')
        soup = bs(response_get.text, features='html.parser')
        list_films = soup.find_all('a', class_='movieItem_title')
        for film in list_films:
            link_pic = soup.find(alt=f'{film.text}')
            if not link_pic:
                spisok_wait.append([film.text, 'https://img.freepik.com/premium-vector/ooops-comic-book-explosion-icon-simple-illustration-ooops-comic-book-explosion-vector-icon-web_96318-26126.jpg?w=826'])
            else:
                spisok_wait.append([film.text, str(link_pic.get('data-picture'))])
        return random.choice(spisok_wait)
    else:
        return random.choice(spisok_wait)


# def rand_mult(var_bot):
#     global spisok[var_bot][0]
#     if len(spisok_mult) == 0:
#         response_get = requests.get(f'https://www.kinoafisha.info/rating/movies/animation/')
#         soup = bs(response_get.text, features='html.parser')
#         list_films = soup.find_all('a', class_='movieItem_title')
#         for film in list_films:
#             link_pic = soup.find(alt=f'{film.text}')
#             if not link_pic:
#                 spisok_mult.append([film.text, 'https://img.freepik.com/premium-vector/ooops-comic-book-explosion-icon-simple-illustration-ooops-comic-book-explosion-vector-icon-web_96318-26126.jpg?w=826'])
#             else:
#                 spisok_mult.append([film.text, str(link_pic.get('data-picture'))])
#         return random.choice(spisok_mult)
#     else:
#         return random.choice(spisok_mult)
#

def rand_akt(var_bot):
    sp = spisok[var_bot]

    if len(sp[0]) == 0:
        response_get = requests.get(sp[1])
        soup = bs(response_get.text, features='html.parser')
        list_films = soup.find_all('a', class_='movieItem_title')
        for film in list_films:
            link_pic = soup.find(alt=f'{film.text}')
            if not link_pic:
                sp[0].append((sp[2], film.text, OOPsPoster))
            else:
                sp[0].append((sp[2], film.text, str(link_pic.get('data-picture'))))
        return random.choice(sp[0])
    else:
        return random.choice(sp[0])