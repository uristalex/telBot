import requests
from bs4 import BeautifulSoup as bs
import random

spisok_horror = []
spisok_comedy = []
spisok_fantasy = []
spisok_mult = []
OOPsPoster = 'https://img.freepik.com/premium-vector/ooops-comic-book-explosion-icon-simple-illustration-ooops-comic-book-explosion-vector-icon-web_96318-26126.jpg?w=826'


spisok = {'comedy': (spisok_comedy, 'https://www.kinoafisha.info/rating/movies/comedy/', 'Комедии'),
          'mult': (spisok_mult, 'https://www.kinoafisha.info/rating/movies/animation/', 'Мультфильмы'),
          'horror': (spisok_horror, 'https://www.kinoafisha.info/rating/movies/horror/', 'Ужасы'),
          'fantasy': (spisok_fantasy, 'https://www.kinoafisha.info/rating/movies/sci-fi/', 'Фантастика')}


# def test_s(var_bot):
#     sp = spisok[var_bot][0]
#     sp.append([var_bot])
#
#     print(sp)
#
#
# test_s('mult')


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


# print(rand_akt('mult'))
# print(rand_akt('mult'))
# print(rand_akt('mult'))

c = 30
while c > 1:
    # for i in spisok:
    print(rand_akt(random.choice([i for i in spisok])))
    c -=1

# print(random.choice(*[spisok.keys()]))
print([i for i in spisok])