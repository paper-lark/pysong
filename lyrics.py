#!/usr/bin/env python3

import requests
import json
import urllib.parse
import sys
import bs4


def createLyricsUrl(artist, song):
    '''
    Create a URL to the song lyrics page

    :param artist: string representing artist name
    :param song: string representing song
    :return: URL to the song lyrics page
    '''
    domain_name = 'http://www.metrolyrics.com'

    def translate(alpha):
        if alpha.isalnum():
            return alpha.lower()
        elif alpha.isspace():
            return '-'
        else:
            return ''

    artist = ''.join(map(translate, artist))
    song = ''.join(map(translate, song))

    return '{}/{}-lyrics-{}.html'.format(domain_name, song, artist)


def getSearchUrl(query):
    '''
    Create URL to the API given a query string.

    :param url: URL for the request
    :return: parsed response
    '''
    queryObject = {
        'per_page': 5,
        'q': query
    }
    url = 'https://genius.com/api/search/multi?{}'.format(
        urllib.parse.urlencode(queryObject))
    return url


def fetchJSON(url):
    '''
    Fetch JSON from the API.

    :param url: URL for the request
    :return: parsed response
    '''
    res = requests.get(url)
    if res.status_code != 200:
        raise Exception(
            'Requests failed with status: {}'.format(res.status_code))
    return res.json()


def fetchLyrics(url):
    '''
    Fetch lyrics from the website.
    :param url: URL to the webpage with lyrics
    :return: lyrics
    '''

    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    elements = soup.select('#lyrics-body-text > *')

    result = ''
    for block in elements:
        if 'class' in block.attrs and ('verse' in block['class'] or 'chorus' in block['class']):
            result += flatten(block.contents) + '\n\n'
    return result


def getTopHits(res):
    '''
    Get an array of top matches off the response object.

    :param res: API response
    :return: array of matches
    '''
    if(len(res['response']['sections']) == 0):
        raise Exception('No songs found')

    section = res['response']['sections'][0]['hits']
    songs = []
    for song in section:
        songs.append({
            'artist': song['result']['primary_artist']['name'],
            'title': song['result']['title']
        })
    return songs


def flatten(block):
    '''
    Flatten a list of BS4 elements to text.

    :param block: list of BS4 elements
    :return: text inside bs4.element.NavigableString elements
    '''

    if isinstance(block, bs4.element.NavigableString):
        return str(block)
    else:
        result = ''
        for line in block:
            if isinstance(line, bs4.element.NavigableString):
                result += line
        return result


if __name__ == '__main__':
    query = input('Enter a piece of the song that you know:\n').strip()
    print('Don\'t worry, we are working to get the title of your song now...')

    # Fetch hit matching API
    try:
        res = fetchJSON(
            getSearchUrl(query))
        print('Halfway there...')
    except:
        print('Failed to connect to the server')
        print("Unexpected error:", sys.exc_info()[0])
        sys.exit(1)

    # Get matching songs
    try:
        songs = getTopHits(res)
        song = songs[0]
    except:
        print('Could not find any matching songs')
        print("Unexpected error:", sys.exc_info()[0])
        sys.exit(1)

    # Hit lyrics API
    try:
        url = createLyricsUrl(song['artist'], song['title'])
        lyrics = fetchLyrics(url)
    except:
        print('Could not fetch lyrics')
        print("Unexpected error:", sys.exc_info()[0])
        sys.exit(1)

    # Print the result
    print('Here is the result:\n\n')
    print('Lyrics for {} by {}:\n'.format(song['title'], song['artist']))
    print(lyrics)
    print('Link to lyrics: {}'.format(url))
    print('\nSongs found:\n')
    for index, song in enumerate(songs):
        print('{}) {} by {}'.format(
            index + 1, song['title'], song['artist']))
