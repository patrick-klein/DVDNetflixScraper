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

Create a new instance of the class.

```>>> session = NetflixSession()```

It will search for 'cookie.pkl' in the current directory and associate the cookies with the session.  If it's unable to find or load the file, the session will still initialize without cookies.  Alternatively, you can pass in an argument that specifies a pickle file containing the cookies.

```>>> session = NetflixSession('~/some/other/file.pkl')```

Load a movie by specifying a search string.  During this call, the webdriver will open a Chrome window to search for the movie.  Once it navigates to the correct page, it will store the parsed html into a variable and close the window.

```>>> session.load_movie('Deliverance')```

The first result that is a close text match will be selected.  After the movie is loaded, you can save the url by calling the "get_movie_url()".

```
>>> deliverance_movie_url = session.get_movie_url()
>>> deliverance_movie_url
'https://dvd.netflix.com/Movie/Deliverance/433193?strackid=13c7f06deb5662ef_1_srl&trkid=201891639'
```

Now if you need to load the movie again in the future, you can pass the url directly to skip the search page.  You can verify this works by checking the name and year of the loaded movie.

```
>>> session.load_movie_with_url(deliverance_movie_url)
>>> session.get_movie_name()
'Deliverance'
>>> session.get_movie_year()
1972
```

Because there is ambiguity with some movies/shows, you can also specify the year when loading from a search.  This will only load a result if it matches +/- 1 year.

```
>>> session.load_movie('Alice in Wonderland',2010)
>>> session.get_movie_url()
'https://dvd.netflix.com/Movie/Alice-in-Wonderland/70113536?strackid=206e723a68719b5d_1_srl&trkid=201891639'
>>> session.load_movie('Alice in Wonderland',1950)
>>> session.get_movie_url()
'https://dvd.netflix.com/Movie/Alice-in-Wonderland/60031746?strackid=d4341b42716abe_2_srl&trkid=201891639'
```

Now that the correct movie has loaded, you can start pulling data from the saved html.  Currently, you can pull the synopsis, image url, genres, and moods, as well as the ratings if you are signed in.

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
>>> session.get_image_link()
'http://secure.netflix.com/us/boxshots/ghd/60031746.jpg'
```

### Note

If you're experiencing an error where chromedriver is not correctly quitting every time, you can kill all of these instances using the following command on macOS:

```$ pkill -f chromedriver```

# NetflixSession Methods

<table class="tg">
  <tr>
    <th class="tg-s6z2">Method</th>
    <th class="tg-s6z2">Description</th>
  </tr>
  <tr>
    <td class="tg-s6z2">load_movie(search_name, search_year=None)</td>
    <td class="tg-s6z2">Loads the Netflix page for the movie/show by starting a search.  Must be called before requesting scraped data for movie.<br><br>
search_name: string of the the name of the movie/show being searched<br>
search_year: if available, only a movie/show within 2 years of specified year will be loaded</td>
  </tr>
  <tr>
    <td class="tg-s6z2">load_movie_with_url(movie_url):</td>
    <td class="tg-s6z2">Loads the Netflix page for the movie/show directly.  Must be called before requesting scraped data for movie.<br><br>
movie_url: a string of a direct link to the webpage</td>
  </tr>
  <tr>
    <td class="tg-s6z2">get_movie_url()</td>
    <td class="tg-s6z2">Returns the url of the loaded movie as a string</td>
  </tr>
  <tr>
    <td class="tg-s6z2">get_movie_name()</td>
    <td class="tg-s6z2">Returns the name of the loaded movie as a string</td>
  </tr>
  <tr>
    <td class="tg-s6z2">get_movie_year()</td>
    <td class="tg-s6z2">Returns the year of the loaded movie as a string</td>
  </tr>
  <tr>
    <td class="tg-s6z2">get_synopsis()</td>
    <td class="tg-s6z2">Returns the synopsis of the movie as a string</td>
  </tr>
  <tr>
    <td class="tg-s6z2">get_genres()</td>
    <td class="tg-s6z2">Returns the genres of the loaded movie as a list of strings</td>
  </tr>
  <tr>
    <td class="tg-s6z2">get_moods()</td>
    <td class="tg-s6z2">Returns the moods of the loaded movie as a list of strings if available, otherwise None</td>
  </tr>
  <tr>
    <td class="tg-s6z2">get_guess_rating()</td>
    <td class="tg-s6z2">Returns the best guess rating of the loaded movie as a float, or None if the session isn't signed in</td>
  </tr>
  <tr>
    <td class="tg-s6z2">get_avg_rating()</td>
    <td class="tg-s6z2">Returns the average rating of the loaded movie as a float, or None if the session isn't signed in</td>
  </tr>
  <tr>
    <td class="tg-s6z2">get_num_votes()</td>
    <td class="tg-s6z2">Returns the number of votes for average rating of the loaded movie as an int, or None if the session isn't signed in</td>
  </tr>
  <tr>
    <td class="tg-s6z2">get_image_link()</td>
    <td class="tg-s6z2">Returns the link to the image of the loaded movie</td>
  </tr>
