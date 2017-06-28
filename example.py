from netflix import netflix

h = netflix()

h.load_movie('Deliverance')

print(h.get_genres())
print(h.get_moods())
print(h.get_guess_rating())
print(h.get_avg_rating())
