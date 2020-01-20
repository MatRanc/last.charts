# https://www.last.fm/api/show/user.getTopAlbums

#pip install json
#pip install requets

import requests
import json
import sys

# Insert an api key
api_key = "INSERT_KEY"
# Insert a username
username = "INSERT_USRNAME"

# Take input for album range
album_number_imput = input("Display my top ___ albums: ")

# Error and exits if fields arent proper
if api_key == "INSERT_KEY" :
	print("Error 1: Insert an API key before using.\n")
	sys.exit(1)

if username == "INSERT_USRNAME" :
	print("Error 2: Inster a username before using.\n")
	sys.exit(2)


# Get data with api, save it and load it as json
top_albums_raw = requests.get("http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user="+username+"&api_key="+api_key+"&format=json")
top_albums_json = json.loads(top_albums_raw.text)

# Define the top albums function and make "number_top_albums_list" an argument that needs to be filled
def top_albums(number_top_albums_list):
	print("\nYour top "+number_top_albums_list+" albums are:\n")
	for album_number in range(0, int(number_top_albums_list)):

		# Get album artist
		top_album_artist = top_albums_json["topalbums"]["album"][album_number]["artist"]["name"]
		# Get album name
		top_album_name = top_albums_json["topalbums"]["album"][album_number]["name"]

		# Display albums
		print(top_album_artist+" - "+top_album_name)
	print("\n")

# Use the "top_albums" function and use the "album_number_imput" as "number_top_albums_list"
top_albums(album_number_imput)




#debug/display full link to view in web browser
#print("https://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user="+username+"&api_key="+api_key+"&format=json")