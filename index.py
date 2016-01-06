import time
import hashlib
import json

import requests
from flask import Flask, render_template, url_for, request

from soco import SoCo

app = Flask(__name__)

app.config.from_pyfile('settings.py')

sonos = SoCo(app.config['SPEAKER_IP'])


def gen_sig():
    return hashlib.md5(
        app.config['ROVI_API_KEY'] +
        app.config['ROVI_SHARED_SECRET'] +
        repr(int(time.time()))).hexdigest()


def get_track_image(artist, album):
    blank_image = url_for('static', filename='img/blank.jpg')
    if 'ROVI_SHARED_SECRET' not in app.config:
        return blank_image
    elif 'ROVI_API_KEY' not in app.config:
        return blank_image

    headers = {
        "Accept-Encoding": "gzip"
    }
    req = requests.get(
        'http://api.rovicorp.com/recognition/v2.1/music/match/album?apikey=' +
        app.config['ROVI_API_KEY'] + '&sig=' + gen_sig() + '&name= ' +
        album + '&performername=' + artist + '&include=images&size=1',
        headers=headers)

    if req.status_code != requests.codes.ok:
        return blank_image

    result = json.loads(req.content)
    try:
        return result['matchResponse']['results'][0]['album']['images']\
            [0]['front'][3]['url']
    except (KeyError, IndexError):
        return blank_image


@app.route("/play")
def play():
    sonos.play()
    return 'Ok'


@app.route("/pause")
def pause():
    sonos.pause()
    return 'Ok'


@app.route("/next")
def next():
    sonos.next()
    return 'Ok'


@app.route("/previous")
def previous():
    sonos.previous()
    return 'Ok'


@app.route("/info-light")
def info_light():
    track = sonos.get_current_track_info()
    return json.dumps(track)


@app.route("/info")
def info():
    track = sonos.get_current_track_info()
    track['image'] = get_track_image(track['artist'], track['album'])
    return json.dumps(track)


@app.route("/")
def index():
    track = sonos.get_current_track_info()
    track['image'] = get_track_image(track['artist'], track['album'])
    return render_template('index.html', track=track)
	
@app.route("/page")
def page():
    return render_template('page.html')
    
@app.route("/pad")
def page():
    return render_template('pad.html')
	
@app.route("/tune")
def tune():
    station = request.args.get('station')
    target = request.args.get('target')
    sonos = SoCo(target)
    sonos.pause()
    if station == 'eldoradio':
        sonos.play_uri('x-rincon-mp3radio://sender.eldoradio.de:8000/high')
    elif station == 'xfm':
        sonos.play_uri('x-rincon-mp3radio://live64.917xfm.de')
    elif station == 'wdr5':
        sonos.play_uri('x-rincon-mp3radio://wdr-5.akacast.akamaistream.net/7/41/119439/v1/gnl.akacast.akamaistream.net/wdr-5')
    return 'Ok'
	
@app.route("/stop")
def stop():
    target = request.args.get('target')
    sonos = SoCo(target)
    sonos.pause()    
    return 'Ok'
	
if __name__ == '__main__':
    app.run(debug=True)
