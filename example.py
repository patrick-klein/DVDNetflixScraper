from DVDNetflixScraper import NetflixSession

session = NetflixSession()

session.load_movie('alice in wonderland', 1950)

print(session.get_synopsis())
print(session.get_genres())
print(session.get_moods())
print(session.get_guess_rating())
print(session.get_avg_rating())
