#!/usr/bin/env python
import os
import sys
import requests
import urllib

ASSETS_URL = 'http://assets.tape.ly/{0}'
SHOWTAPE_URL = 'http://tape.ly/showtape?id={0}'
YOUTUBE_DOWNLOAD_CMD = u'youtube-dl  --audio-format "mp3" -x "https://www.youtube.com/watch?v={0}"  -o "{1}" -q'
SC_DOWNLOAD_URL = 'http://api.soundcloud.com{0}/stream?client_id=f97207e1f10679ca18d43d544890ec34'


def download_s3(url, name, index, tape_name):
    urllib.urlretrieve(
        ASSETS_URL.format(url),
        u'downloads/{0}/{1} - {2}.mp3'.format(tape_name, '%02d' % index, name)
    )


def download_soundcloud(url, name, index, tape_name):
    url = SC_DOWNLOAD_URL.format(url)
    urllib.urlretrieve(
        url,
        u'downloads/{0}/{1} - {2}.mp3'.format(tape_name, '%02d' % index, name)
    )


def download_youtube(url, name, index, tape_name):
    youtube_id = url.rsplit('/', 1)[1]
    cmd = YOUTUBE_DOWNLOAD_CMD.format(
        youtube_id,
        u'downloads/{0}/{1} - {2}.mp3'.format(tape_name, '%02d' % index, name)
    ).encode('utf-8')
    os.system(cmd)

tape_slug = sys.argv[1]
headers = {
    'X-Requested-With': 'XMLHttpRequest',
    'Accept': 'application/json, text/javascript, */*; q=0.01'
}

song_list = requests.get(SHOWTAPE_URL.format(tape_slug), headers=headers)

tape = song_list.json()['tape']
song_list = tape['songs']

os.mkdir(u'downloads/{0}'.format(tape['name']))

for index, song in enumerate(song_list):
    song = song['song']
    print 'Downloading', index, song['title']

    song_title = song['title'].replace('"', "'")
    tape_name = tape['name'].replace('"', "'")
    if song['source'] == 'S3':
        download_s3(
            song['filename'],
            name=song_title,
            index=index,
            tape_name=tape_name,
        )
    elif song['source'] == 'YT':
        download_youtube(
            song['filename'],
            name=song_title,
            index=index,
            tape_name=tape_name,
        )
    elif song['source'] == 'SC':
        download_soundcloud(
            song['filename'],
            name=song_title,
            index=index,
            tape_name=tape_name,
        )

    else:
        print 'Skipping, unkown source', song['source']
        continue
        # raise Exception('unknown source %s' % song['source'])
