"""This module contains the NetflixSession class."""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from fuzzywuzzy import fuzz
import re
import pickle
import logging


class NetflixSession:
    """This is a class capable of scraping DVD Netflix pages."""

    # Configure logfile for debugging
    logging.basicConfig(filename='session.log',
                        filemode='w', level=logging.DEBUG)
    logging.info('Re-opening log file')

    def __init__(self, cookies_file='./cookie.pkl'):
        """
        Create instance of class for scraping movie.  Tries to load a
            set of cookies with this instance, which are required to view
            unavailable movies/shows, and are needed to get ratings.

        cookies_file: string of path to pickle file containing cookies
                        (if cookies aren't loaded, script will continue
                        without them)
        """
        try:
            self.cookies = pickle.load(open(cookies_file, "rb"))
            logging.info('Cookies loaded from ' + cookies_file)
        except:
            self.cookies = None
            logging.info('No cookies were loaded on init')

    def load_movie(self, search_name, search_year=None):
        """
        This method loads the Netflix page for the movie/show.  Must be called
            before requesting scraped data for movie

        search_name: string of the the name of the movie/show being searched
        search_year: if available, only a movie/show within 2 years of specified
                        year will be loaded
        """

        # create a driver using chromedriver
        driver = webdriver.Chrome(executable_path='./chromedriver')

        # need to load some netflix domain before adding cookies
        if self.cookies:
            driver.get('https://dvd.netflix.com/404')
            for i in range(len(self.cookies)):
                driver.add_cookie(self.cookies[i])

        # insert search string into url (effectively searching for 'search_name search_year')
        search_url = 'https://dvd.netflix.com/Search?oq=&ac_posn=&search_submit=&v1=' + \
            search_name.replace(' ', '+')
        if search_year:
            search_url = search_url + '+' + str(search_year)
        logging.info('search url: ' + search_url)

        # retrieve search page, and wait for results to load
        driver.get(search_url)
        delay = 3  # seconds
        try:
            WebDriverWait(driver, delay).until(
                EC.presence_of_element_located((By.ID, 'searchResultsItems')))
        except TimeoutException:
            logging.error("Search results did not load.")
            driver.quit()
            raise Exception('Search results did not load.')

        # parse html using BeautifulSoup to find search results
        html = driver.page_source
        results_page = BeautifulSoup(html, "html.parser")
        search_content = results_page.find(id="search-body")
        result_list = search_content.find(id='SliderContainer').find_all(
            attrs={"class": "movieSearchDetails"})

        # loop through results to find text and year(optional) match
        link_to_movie_page = None
        for result in result_list:
            result_name = result.find('a').get_text()
            if fuzz.ratio(search_name.lower(), result_name.lower()) < 80:  # value open to tweaking
                continue
            if search_year:
                result_year = int(result.find(
                    attrs={"class": "year"}).get_text())
                if abs(result_year - search_year) < 2:
                    link_to_movie_page = result.find('a').get('href')
                    break
            else:
                link_to_movie_page = result.find('a').get('href')
                break
        if link_to_movie_page == None:
            logging.error('No matching movies were found')
            driver.quit()
            raise Exception('No matching movies were found')
        else:
            logging.info('movie url: ' + link_to_movie_page)
        self.movie_url = link_to_movie_page

        # load movie/show page, and save parsed html for further use
        driver.get(self.movie_url)
        html = driver.page_source
        self.movie_page = BeautifulSoup(html, "html.parser")
        driver.quit()

    def print_movie_url(self):
        """This methods prints the url of the loaded movie."""
        print(self.movie_url)

    def get_synopsis(self):
        """This methods parses movie page and returns the synopsis."""
        synopsis = self.movie_page.find(
            'p', attrs={"class": "synopsis"}).get_text()
        return(synopsis)

    def get_genres(self):
        """This methods parses movie page and returns list of genres."""
        movie_details = self.movie_page.find(id='mdp-details')
        genres = movie_details.find(
            'dt', string="Genres").parent.dd.get_text().split(',')
        genres = [i.strip() for i in genres]
        return genres

    def get_moods(self):
        """This methods parses movie page and returns list of moods (if present)."""
        movie_details = self.movie_page.find(id='mdp-details')
        moods = movie_details.find('dt', string=re.compile("^T"))
        try:
            moods = moods.parent.dd.get_text().split(',')
            moods = [i.strip() for i in moods]
        except:
            logging.info('No moods found for this movie/show.')
        return moods

    def get_guess_rating(self):
        """
        This methods parses movie page and returns best guess rating
            or None if no cookies were provided
        """
        if self.cookies == None:
            return None
        rating_info = self.movie_page.find('div', id='ratingInfo')
        guess_rating = rating_info.find_all(
            'div')[0].find('span').get_text().split(' ')[0]
        return float(guess_rating)

    def get_avg_rating(self):
        """
        This methods parses movie page and returns avg rating
            or None if no cookies were provided
        """
        if self.cookies == None:
            return None
        rating_info = self.movie_page.find('div', id='ratingInfo')
        avg_rating = rating_info.find_all('div')[1].find(
            'span').get_text().split(' ')[0]
        return float(avg_rating)
