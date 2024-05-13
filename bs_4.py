import requests
from bs4 import BeautifulSoup as bs
import random

spisok_f = []
spisok_wait = []


def spisok_500():
    global spisok_f
    if len(spisok_f) == 0:
        for i in (1, 2):
            response_get = requests.get(f'https://www.kinoafisha.info/rating/movies/?page={i}')
            print(response_get.status_code)
            soup = bs(response_get.text, features='html.parser')
            list_films = soup.find('div', class_='movieList_item movieItem  movieItem-rating movieItem-position  ')
            # for film in list_films:
            #
            #     link_pic = soup.find(alt=f'{film.text}')
            #     spisok_f.append([film.text, str(link_pic.get('data-picture'))])
            print(list_films.text)

        # return random.choice(spisok_f)
    # else:
        # return random.choice(spisok_f)

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


rand_popular()
print(*spisok_wait, sep='\n')

# <a class="movieItem_title" href="https://www.kinoafisha.info/movies/8369274/">Майор Гром: Игра</a>
# spisok_500()
# print(spisok_f)




#<img class="picture_image" alt="Шрэк" title="Шрэк" src="https://static.kinoafisha.info/k/movie_posters/220/upload/movie_posters/5/2/6/5625/8971a949ea7f23e16f77f34c1d9403aa.jpeg">