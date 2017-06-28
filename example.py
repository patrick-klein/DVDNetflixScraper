'''This is an example use of the scraper.  See the README for more'''

# import the class from the module
from DVDNetflixScraper import NetflixSession

# create a new session
session = NetflixSession()

# search for a movie, print the page that it found
session.load_movie('Deliverance')
session.print_movie_url()

# search for movies with the same name, but different years
session.load_movie('Alice in Wonderland', 2010)
session.print_movie_url()
session.load_movie('Alice in Wonderland', 1950)
session.print_movie_url()

# pull information from the web page.  ratings only show if signed in
print(session.get_synopsis())
print(session.get_genres())
print(session.get_moods())
print(session.get_guess_rating())
print(session.get_avg_rating())

# if signed in, this will load correctly
session_with_cookies = NetflixSession()
session_with_cookies.load_movie('blood drive')

# because this show doesn't have a public page, this will fail without cookies
session_without_cookies = NetflixSession(cookies_file='pickle.cki')
session_without_cookies.load_movie('blood drive')
