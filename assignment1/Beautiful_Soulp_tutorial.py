from requests import get
url = 'https://www.imdb.com/search/title?release_date=2017&sort=num_votes,desc&page=1'
response = get(url)
# print(response.text[:500])

from bs4 import BeautifulSoup
html_soup = BeautifulSoup(response.text, 'html.parser')
# print(type(html_soup))

movie_containers = html_soup.find_all('div', class_ = 'lister-item mode-advanced')
# print(type(movie_containers))
# print(len(movie_containers))

first_movie = movie_containers[0]
print(first_movie.h3.a)