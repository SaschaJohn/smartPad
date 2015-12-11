import re
import urllib2
import string
url1 = raw_input("Please enter a URL from Tunein Radio: ");
open_file = urllib2.urlopen(url1);
raw_file = open_file.read();
API_key = re.findall(r"StreamUrl\":\"(.*?),",raw_file);
#print API_key;
#print "The API key is: " + API_key[0];
use_key = urllib2.urlopen(str(API_key[0]));
key_content = use_key.read();
raw_stream_url = re.findall(r"Url\": \"(.*?)\"",key_content);
bandwidth = re.findall(r"Bandwidth\":(.*?),", key_content);
reliability = re.findall(r"lity\":(.*?),", key_content);
isPlaylist = re.findall(r"HasPlaylist\":(.*?),",key_content);
codec = re.findall(r"MediaType\": \"(.*?)\",", key_content);
tipe = re.findall(r"Type\": \"(.*?)\"", key_content);
total = 0
for element in raw_stream_url:
    total = total + 1
i = 0
print "I found " + str(total) + " streams.";
for element in raw_stream_url:
    print "Stream #" + str(i + 1);
    print "Stream stats:";
    print "Bandwidth: " + str(bandwidth[i]) + " kilobytes per second."
    print "Reliability: " + str(reliability[i]) + "%"
    print "HasPlaylist: " + str(isPlaylist[i]) + "."
    print "Stream codec: " + str(codec[i]) + "."
    print "This audio stream is " + tipe[i].lower() + "."
    print "Pure streaming URL: " + str(raw_stream_url[i]) + ".";
    i = i + 1
raw_input("Press enter to close TMUS.")