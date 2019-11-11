import sys
import spotipy
import spotipy.util as util
import requests
from config.config import *
from bs4 import BeautifulSoup

def getCurrentSong(token):
    # Create a Spotify() instance with the obtained token
    sp = spotipy.Spotify(auth=token)

    current_song = sp.currently_playing()
    # check if none
    if current_song is not None:
        artist = current_song['item']['artists'][0]['name']
        song_name = current_song['item']['name']
        return artist, song_name
    else:
        print("There is no song currently playing")
        sys.exit()

def getSpotifyToken():
    token = util.prompt_for_user_token(
        USERNAME, SCOPE, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)

    try:
        return token
    except:
        print("Can't get token for user: {}".format(USERNAME))
        sys.exit()

def removeParentheses(dataString):
    pos1 = dataString.find('(')

    if pos1 != -1:
        pos2 = dataString.find(')')
        dataString = dataString[:pos1] + dataString[pos2+1:]

    return dataString

def cleanParentheses(dataString):
    dataString = dataString.replace('(','').replace(')','')
    return dataString

def cleanSongInfo(artist, song_name):
    charsToRemove = ['\'', ',', ' -']

    clean_artist = str(artist).strip().lower()
    clean_song = str(song_name).strip().lower()

    for x in charsToRemove:
        clean_artist = clean_artist.replace(x,'')
        clean_song = clean_song.replace(x,'')

    clean_artist = removeParentheses(clean_artist)
    clean_song = cleanParentheses(clean_song)
    
    return clean_artist, clean_song

def createSongUrl(artist, song_name, showUrl=False):
    # create a valid url for web scrapping using song name and artist
    clean_artist, clean_song = cleanSongInfo(artist, song_name)
    artist2url = clean_artist.replace(" ", "-")
    song2url = clean_song.replace(" ", "-")
    song_url = '{}-{}-lyrics'.format(artist2url, song2url)

    print('\nSong: {}\nArtist: {}'.format(song_name, artist))

    if showUrl:
        print(song_url)
    
    return song_url

def getLyrics(song_url):
    # New request using song_url created before
    request = requests.get("https://genius.com/{}".format(song_url))

    # Verify status_code of request
    if request.status_code == 200:
        # BeautifulSoup library return an html code
        html_code = BeautifulSoup(request.text, features="html.parser")
        # Extract lyrics from beautifulsoup response using the correct prefix {"class": "lyrics"}
        lyrics = html_code.find("div", {"class": "lyrics"}).get_text()
        return lyrics

    else:
        print("Sorry, I can't find the actual song")
        sys.exit()

def main():
    token = getSpotifyToken()
    artist, song_name = getCurrentSong(token)
    song_url = createSongUrl(artist, song_name, showUrl=True)
    lyrics = getLyrics(song_url)
    print(lyrics)

if __name__ == "__main__":
    main()