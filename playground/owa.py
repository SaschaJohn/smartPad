import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from pyexchange import Exchange2010Service, ExchangeNTLMAuthConnection
from pytz import timezone
from datetime import datetime

URL = u'https://owa.thyssenkrupp.info/EWS/Exchange.asmx'
USERNAME = u'tkagit\\10316197'
PASSWORD = u"17.anderes"

# Set up the connection to Exchange
connection = ExchangeNTLMAuthConnection(url=URL,username=USERNAME,password=PASSWORD)

service = Exchange2010Service(connection)
events = service.calendar().list_events(
    start=timezone("CET").localize(datetime(2015, 12, 11, 1, 0, 0)),
    end=timezone("CET").localize(datetime(2015, 12, 11, 23, 0, 0)),
    details=True
)
for event in events.events:
    print "{start} {stop} - {subject}".format(
        start=event.start,
        stop=event.end,
        subject=event.subject
    )
