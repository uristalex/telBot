#file to func
import  requests
from bs4 import BeautifulSoup as bs
import random

spisok_f = []


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
