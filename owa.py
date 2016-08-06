import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from pyexchange import Exchange2010Service, ExchangeNTLMAuthConnection
from pytz import timezone
from datetime import datetime, timedelta
from tzlocal import get_localzone

from flask import Flask

DAY = timedelta(1)

def getEvents(date):
	now = date
	tommorow = now + DAY
	returnValue = list()
	evt= service.calendar().list_events(
	start=timezone("CET").localize(datetime(date.year, date.month, date.day, 1, 0, 0)),
	end=timezone("CET").localize(datetime(tommorow.year, tommorow.month, tommorow.day, 23, 0, 0)),
	details=True
	)
	for event in evt.events:
		a = list()
		a.append((event.start.astimezone(get_localzone())).strftime("%Y-%m-%d %H:%M"))
		a.append((event.end.astimezone(get_localzone())).strftime("%Y-%m-%d %H:%M"))
		a.append(event.subject)
		returnValue.append(a)
	return returnValue

app = Flask(__name__)

app.config.from_pyfile('settings.py')
connection = ExchangeNTLMAuthConnection(url=app.config['URL'],username=app.config['USER'],password=app.config['PASS'])
service = Exchange2010Service(connection)