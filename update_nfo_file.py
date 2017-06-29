"""
This module contains two primary functions that can modify .nfo files
    using the DVD Netflix Scraper

These functions are intented to be called from the REPL, while in the
    folder DVDNetflixScraper.

The functions will display the scraped data to the console, ask the user
    to verify the data, then update the .nfo file accordingly.

"""

import urllib.request
from bs4 import BeautifulSoup
from DVDNetflixScraper import NetflixSession


def update_tvshow_nfo(tv_show_name,
                      tv_show_folder='/Volumes/Media/TV/',
                      data_selections={'landscape': True,
                                       'plot': True,
                                       'outline': True,
                                       'genre-moods': True,
                                       'best-guess-rating': False,
                                       'avg-rating': False,
                                       'netflix-tag': True}):
    """
    This function updates .nfo files for TV shows.

    tv_show_name: exact string of TV show name (case-insensitive)
    tv_show_folder: exact string to path of TV shows
    data_selections: dictionary of data in .nfo file to be updated
    """

    # get folder of TV show and .nfo file
    path_to_tv_show = tv_show_folder + tv_show_name + '/'
    path_to_tv_show_nfo = path_to_tv_show + 'tvshow.nfo'

    # open .nfo file and extract info using bs4
    with open(path_to_tv_show_nfo) as fp:
        soup = BeautifulSoup(fp, 'xml')

    # start session with scraper and search for TV show
    session = NetflixSession()

    # skip the search page if url tag is available
    if soup.find('dvd-netflix-url'):
        show_url = soup.find('dvd-netflix-url').get_text()
        session.load_movie_with_url(show_url)
    else:
        tv_show_year = int(soup.find('premiered').get_text()[0:4])
        session.load_movie(tv_show_name, tv_show_year)

    # scrape all of the data into variables
    movie_url = session.get_movie_url()
    synopsis = session.get_synopsis()
    genres = session.get_genres()
    moods = session.get_moods()
    guess_rating = session.get_guess_rating()
    avg_rating = session.get_avg_rating()
    img_url = session.get_image_link()

    # print the values for selected data
    print(' ')
    print(session.movie_name)
    print(session.movie_year)
    if data_selections['plot'] or data_selections['outline']:
        print(' ')
        print(synopsis)
    if data_selections['genre-moods']:
        print(' ')
        print(genres)
        print(moods)
    if data_selections['best-guess-rating']:
        print(' ')
        print(guess_rating)
    if data_selections['avg-rating']:
        print(' ')
        print(avg_rating)

    # ask for confirmations here
    #       (y)es to selection
    #       (n)o to all
    print(' ')
    answer = input('Save?    ')

    # update .nfo and save if 'y'
    if answer == 'y':
        if data_selections['plot']:
            update_plot(soup, synopsis)
        if data_selections['outline']:
            update_outline(soup, synopsis)
        if data_selections['genre-moods']:
            update_genre_moods(soup, genres, moods)
        if data_selections['best-guess-rating']:
            update_rating(soup, guess_rating)
        if data_selections['avg-rating']:
            update_rating(soup, avg_rating)
        if data_selections['landscape']:
            update_img(img_url)
        if data_selections['netflix-tag']:
            add_netflix_tag_tvshow(soup, movie_url)
        # save the xml file
        with open(path_to_tv_show_nfo, 'w') as f:
            f.write(str(soup))


def update_movie_nfo(movie_name_and_year,
                     movies_folder='/Volumes/Media/Movies/',
                     data_selections={'plot': True,
                                      'outline': True,
                                      'genre-moods': True,
                                      'best-guess-rating': False,
                                      'avg-rating': False,
                                      'netflix-tag': True}):
    """
    This function updates .nfo files for movies.

    movie_name_and_year: exact string of "movie name (year)" (case-insensitive)
    movies_folder: exact string to path of movies
    data_selections: dictionary of data in .nfo file to be updated
    """

    # recover name and year from input
    movie_name = movie_name_and_year[:-7]
    movie_year = int(movie_name_and_year[-5:-1])

    # get folder of movie and .nfo file
    path_to_movie = movies_folder + movie_name_and_year + '/'
    path_to_movie_nfo = path_to_movie + movie_name + '.nfo'

    # open .nfo file and extract info using bs4
    with open(path_to_movie_nfo) as fp:
        soup = BeautifulSoup(fp, 'xml')

    # start session with scraper and search for movie
    session = NetflixSession()

    # skip search page if url tag is found
    if soup.find('dvd-netflix-url'):
        movie_url = soup.find('dvd-netflix-url').get_text()
        session.load_movie_with_url(movie_url)
    else:
        session.load_movie(movie_name, movie_year)

    # scrape all of the data into variables
    movie_url = session.get_movie_url()
    synopsis = session.get_synopsis()
    genres = session.get_genres()
    moods = session.get_moods()
    guess_rating = session.get_guess_rating()
    avg_rating = session.get_avg_rating()

    # print the values for selected data
    print(' ')
    print(session.movie_name)
    print(session.movie_year)
    if data_selections['plot'] or data_selections['outline']:
        print(' ')
        print(synopsis)
    if data_selections['genre-moods']:
        print(' ')
        print(genres)
        print(moods)
    if data_selections['best-guess-rating']:
        print(' ')
        print(guess_rating)
    if data_selections['avg-rating']:
        print(' ')
        print(avg_rating)

    # ask for confirmations here
    #       (y)es to selection
    #       (n)o to all
    print(' ')
    answer = input('Save?    ')

    if answer == 'y':
        if data_selections['plot']:
            update_plot(soup, synopsis)
        if data_selections['outline']:
            update_outline(soup, synopsis)
        if data_selections['genre-moods']:
            update_genre_moods(soup, genres, moods)
        if data_selections['best-guess-rating']:
            update_rating(soup, guess_rating)
        if data_selections['avg-rating']:
            update_rating(soup, avg_rating)
        if data_selections['netflix-tag']:
            add_netflix_tag_movie(soup, movie_url)
        # save the xml file
        with open(path_to_movie_nfo, 'w') as f:
            f.write(str(soup))


def update_outline(soup, synopsis):
    soup.find('outline').string = synopsis


def update_plot(soup, synopsis):
    soup.find('plot').string = synopsis


def update_genre_moods(soup, genres, moods):
    try:
        genres.remove('TV Shows')
    except:
        pass
    if moods:
        new_string = str(' / ').join(genres) + ' / ' + str(' / ').join(moods)
    else:
        new_string = str(' / ').join(genres)
    soup.find_all('genre')[0].string = new_string
    for ext_count in range(1, len(soup.find_all('genre'))):
        soup.find_all('genre')[1].decompose()


def update_rating(soup, rating):
    soup.find('rating').string = str(2 * rating)
    soup.find('votes').string = str(0)


def add_netflix_tag_tvshow(soup, show_url):
    netflix_tag = soup.new_tag('dvd-netflix-url')
    netflix_tag.string = show_url
    soup.find('tvshow').append(netflix_tag)


def add_netflix_tag_movie(soup, movie_url):
    netflix_tag = soup.new_tag('dvd-netflix-url')
    netflix_tag.string = movie_url
    soup.find('movie').append(netflix_tag)


def update_img(img_url):
    urllib.request.urlretrieve(img_url, "./landscape.jpg")
