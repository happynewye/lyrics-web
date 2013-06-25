from scraper import Scraper

s = Scraper()

lyrics = s.get_lyrics('The Parlotones', 'Push Me To The Floor')
print(lyrics)
