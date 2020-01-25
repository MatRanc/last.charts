import requests
import json
import sys

# Insert an api key
api_key = "INSERT_KEY"
# Insert a username
username = "INSERT_USRNAME"

#-------------------------------------------------------------
# Top artists data

# Get url for browser
#print("http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user="+username+"&api_key="+api_key+"&format=json&limit=1000")

top_artists_raw = requests.get("http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user="+username+"&api_key="+api_key+"&format=json&limit=1000")
top_artists_json = json.loads(top_artists_raw.text)

for x in range(0, 1000):

	artist_name = top_artists_json["topartists"]["artist"][x]["name"]
	artist_playcount = top_artists_json["topartists"]["artist"][x]["playcount"]

	print(artist_name)
	print(artist_playcount)