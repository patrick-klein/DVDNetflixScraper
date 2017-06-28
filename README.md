# DVD Netflix Scraper
A Python class that scrapes information for movies and TV shows from dvd.netflix.com pages. No account/cookies required, unless attempting to scrape ratings or titles not available on DVD.

## Requirements
* Python 3
* Modules:
  * Selenium
  * Beautiful Soup
  * Fuzzywuzzy
* Chromedriver

## Installation

Git clone the project onto your computer 

A requirements file is included for convencience when installing the modules, 
so you only need to run the following command:

```$ pip3 install -r requirements.txt```

Selenium also requires a driver to load the webpages, so simply download the latest version of [Chromedriver](http://chromedriver.storage.googleapis.com/index.html) and place it in your project folder.

## Setting Up Cookies (Optional)

Cookies of a valid Netflix session can be used to enable scraping unavailable titles and ratings. Using the provided helper script, it's easy to make these cookies available to the webdriver.

1. First, you need to sign into [DVD Netflix](https://dvd.netflix.com/MemberHome) on Google Chrome.
2. Using the extension [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg?hl=en), export the cookies for this domain, which will be copied to the clipboard.
3. Paste these into save_cookies_to_pickle.py, replacing the example.
4. Edit the boolean values so they have the correct case, i.e. "True" and "False" instead of "true" and "false".
5. Save and run save_cookies_to_pickle.py to generate the pickle file.

# Instructions

Start by importing the module so that the class is available.

```>>> from DVDNetflixScraper import NetflixSession```

Create a new instance of the class.  It will search for 'cookie.pkl' in the current directory and associate the cookies with the session.  If it's unable to find or load the file, the session will still initialize without cookies.

```>>> session = NetflixSession()```

Alternatively, you can pass in an argument that specifies a pickle file containing the cookies.

```>>> session = NetflixSession(cookies_file='~/some/other/file.pkl')```

Load a movie by specifying a search string.  During this call, the webdriver will open a Chrome window to search for the movie.  Once it navigates to the correct page, it will store the parsed html into a variable and close the window.

```>>> session.load_movie('Deliverance')```

The first result that is a close text match will be selected.  The exact url is saved in the log, but you can also view it using the "print_movie_url()" method.

```
>>> session.print_movie_url()
https://dvd.netflix.com/Movie/Deliverance/433193?strackid=1a3cb801d6f27aff_1_srl&trkid=201891639
```

Because there is ambiguity with some searches, you can also specify the year of the movie/show.  This will only load a result if it matches +/- 1 year.

```
>>> session.load_movie('Alice in Wonderland',2010)
>>> session.print_movie_url()
https://dvd.netflix.com/Movie/Alice-in-Wonderland/70113536?strackid=e90ad5b09382b08_1_srl&trkid=201891639
>>> session.load_movie('Alice in Wonderland',1950)
>>> session.print_movie_url()
https://dvd.netflix.com/Movie/Alice-in-Wonderland/60031746?strackid=3a75bc6e9f9fa30c_2_srl&trkid=201891639
```

Now that the correct movie has loaded, you can start pulling data from the saved html.  Currently, you can pull the synopsis, genres, and moods, as well as the ratings if you are signed in.

```
>>> session.get_synopsis()
"Disney's animated, musical retelling of Lewis Carroll's whimsical tale follows young Alice as she falls down a rabbit hole and enters a strange and wonderful world that is home to the Mad Hatter, the Cheshire Cat and the terrifying Queen of Hearts."
>>> session.get_genres()
['Children & Family', 'Family Animation', 'Family Classics', 'Family Sci-Fi & Fantasy', 'Family Adventures', 'Book Characters', 'Disney', "Kids' Music", 'Ages 5-7', 'Ages 8-10', 'Ages 11-12']
>>> session.get_moods()
['Imaginative']
>>> session.get_guess_rating()
3.6
>>> session.get_avg_rating()
4
```

## Planned Features

* Add a method to check the sign-in status of the session

## Notes

If you're experiencing an error where chromedriver is not correctly quitting everytime, you can kill all of these instances using the following command on macOS:

```$ pkill -f chromedriver```
