# https://www.last.fm/api/show/user.getTopAlbums

import requests
import json

# Insert an api key
api_key = "INSERT_KEY"
# Insert a username
username = "INSERT_USRNAME"

# Get data with api, save it and load it as json
top_albums_raw = requests.get("http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user="+username+"&api_key="+api_key+"&format=json")
top_albums_json = json.loads(top_albums_raw.text)

for album_number in range(0,100):

	# Get album artist
	top_album_artist = top_albums_json["topalbums"]["album"][album_number]["artist"]["name"]
	# Get album name
	top_album_name = top_albums_json["topalbums"]["album"][album_number]["name"]

	# Displays full list
	print(top_album_name+" - "+top_album_artist)


#print("https://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user="+username+"&api_key="+api_key+"&format=json")