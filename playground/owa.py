import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from pyexchange import Exchange2010Service, ExchangeNTLMAuthConnection
from pytz import timezone
from datetime import datetime, timedelta

from flask import Flask
app = Flask(__name__)

app.config.from_pyfile('../settings.py')


now = datetime.now()
DAY = timedelta(1)

tommorow = now + DAY;

URL = app.config['URL']
USERNAME = app.config['USER']
PASSWORD = app.config['PASS']

# Set up the connection to Exchange
connection = ExchangeNTLMAuthConnection(url=URL,username=USERNAME,password=PASSWORD)

service = Exchange2010Service(connection)
events = service.calendar().list_events(
    start=timezone("CET").localize(datetime(now.year, now.month, now.day, 1, 0, 0)),
    end=timezone("CET").localize(datetime(now.year, now.month, now.day, 23, 0, 0)),
    details=True
)
eventsTommorow = service.calendar().list_events(
    start=timezone("CET").localize(datetime(tommorow.year, tommorow.month, tommorow.day, 1, 0, 0)),
    end=timezone("CET").localize(datetime(tommorow.year, tommorow.month, tommorow.day, 23, 0, 0)),
    details=True
)
for event in events.events:
    print "{start} {stop} - {subject}".format(
        start=event.start,
        stop=event.end,
        subject=event.subject
    )
for event in eventsTommorow.events:
    print "{start} {stop} - {subject}".format(
        start=event.start,
        stop=event.end,
        subject=event.subject
    )
