import urllib2
from bs4 import BeautifulSoup
import string

url_stem = 'http://www.darklyrics.com/'
ignore_links = ['', 'SUBMIT LYRICS', 'LINKS', 'Privacy Policy',
                'Disclaimer', 'Contact Us']
ignore_links += [e for e in string.ascii_uppercase]

all_lyrics = ''


# Get the list of bands that start with each letter
# for letter in string.ascii_lowercase:
for letter in ['a']:
    letter_url = url_stem + letter + '.html'
    letter_page = urllib2.urlopen(letter_url)
    letter_soup = BeautifulSoup(letter_page)
    band_list = letter_soup.find_all('a')
    band_list = [e.attrs['href'] for e in band_list \
                    if e.text not in ignore_links]
    band_list = [e for e in band_list if not e.startswith('http')]

    for band_name in band_list:  # Get a list of all albums by this band
        print band_name
        band_url = url_stem + band_name
        try:
            band_page = urllib2.urlopen(band_url)
        except:
            print "I didn't like %s anyway." % band_name
            # continue
        band_soup = BeautifulSoup(band_page)
        song_list = band_soup.find_all('a')
        # Get the name of the first song on each album
        song_titles = [e.attrs['href'] for e in song_list]
        first_songs = [e for e in song_titles if e.endswith('#1')]

        for album in first_songs: # Get all the lyrics in this album
            album_url = url_stem + album[3:-2]
            album_page = urllib2.urlopen(album_url)
            album_soup = BeautifulSoup(album_page)
            if album_soup.body is None:
                print "No data returned."
                continue
            lyrics = album_soup.body.find('div', attrs={'class' : 'lyrics'})
            lyrics = lyrics.getText()
            all_lyrics += lyrics
            # print "+1"

f = open('metal_corpus.txt', 'w')
f.write(all_lyrics)
f.close()
