from __future__ import print_function # In python 2.7
import time
import hashlib
import json
import requests
import os
import glob
import owa
import json
import babel.dates
import sqlite3
import sys
import logging
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from binascii import a2b_base64
from datetime import datetime, timedelta
from flask import Flask, render_template, url_for, request, send_file, Response, jsonify, g
from soco import SoCo
import flask

app = Flask(__name__)

app.config.from_pyfile('settings.py')

sonos = SoCo(app.config['SPEAKER_IP'])

fileCount = -1

#get gallery files, store in array
files = []
for (path, dirnames, filenames) in os.walk('gallery'):
	files.extend(os.path.join(path, name) for name in filenames)
#print(files[0])

DATABASE = 'messages.db'

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
	return db

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

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
	return json.dumps(track)


@app.route("/")
def index():
	return render_template('page.html')
	
@app.route("/page")
def page():
	return render_template('page.html')
	
@app.route("/pad")
def pad():
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

@app.route("/save", methods = ['POST'])
def save():
	data = request.form.get("dataUrl")
	filename = request.form.get("filename")
	db = get_db()
	cur = db.cursor()
	cur.execute("INSERT INTO message VALUES ('{file}', 0)".\
		format(file=filename))
	db.commit()
	binary_data = a2b_base64(data)
	fd = open(os.path.join('messages', filename), 'wb')
	fd.write(binary_data)
	fd.close()
	return 'Ok'

@app.route("/getMessages")
def getMessages():
	newest = max(glob.iglob('messages/*.png'), key=os.path.getctime)
	return send_file(newest , mimetype='image/png')

@app.route("/checkUnread")
def checkUnread():
	db = get_db()
	cur = db.cursor()
	cur.execute("SELECT * FROM message WHERE read=0")
	id_exists = cur.fetchall()
	if id_exists:
		return jsonify(True)
	else:
		return jsonify(False)

@app.route("/getUnread")
def getUnread():
	db = get_db()
	cur = db.cursor()
	cur.execute("SELECT file FROM message WHERE read=0 LIMIT 1")
	id_exists = cur.fetchone()
	newest = id_exists[0];
	cur.execute("UPDATE message set read=1 where file='{file}'".\
		format(file=newest))
	db.commit()
	return send_file('messages/'+newest , mimetype='image/png')

@app.route("/getAppointments")
def getAppointments():
	now = datetime.now()
	try:
		events = owa.getEvents(now)
		dat = json.dumps(events)
		resp = Response(response=dat,status=200,mimetype="application/json")
		return(resp)
	except:
		return jsonify("success=False"), 400

@app.route("/getImage")
def getImage():
	global fileCount
	fileCount+=1
	if fileCount > len(files)-1:
		fileCount=0
	return send_file(files[fileCount], mimetype='image/png')

@app.route("/getImageList")
def getImageList():
	global files
	return jsonify(files)

@app.route("/getDate")
def getDate():
	now=datetime.now()
	a = list()
	a.append(babel.dates.format_date(now, 'd. MMMM', locale='pl_PL'))
	a.append(babel.dates.format_date(now, 'd. MMMM yyyy', locale='de_DE'))	
	return jsonify(a)
	
@app.route("/stop")
def stop():
	target = request.args.get('target')
	sonos = SoCo(target)
	sonos.pause()    
	return 'Ok'

class MyHandler(PatternMatchingEventHandler):
	patterns=["*.jpg"]

	def process(self, event):
		"""
		event.event_type
			'modified' | 'created' | 'moved' | 'deleted'
		event.is_directory
			True | False
		event.src_path
			path/to/observed/file
		"""
		global files
		files = []
		for (path, dirnames, filenames) in os.walk('gallery'):
			files.extend(os.path.join(path, name) for name in filenames)
	
	def on_deleted(self, event):
		self.process(event)	

	def on_created(self, event):
		self.process(event)
	
if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO,
						format='%(asctime)s - %(message)s',
						datefmt='%Y-%m-%d %H:%M:%S')
	path = './gallery'
	event_handler = MyHandler()
	observer = Observer()
	observer.schedule(event_handler, path, recursive=True)
	observer.start()
	app.run(host= '0.0.0.0',debug=True)
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
	observer.join()
