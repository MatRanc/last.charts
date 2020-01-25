#pip install json
#pip install requets

import requests
import json
import sys
from userkey import *


# Error and exits if fields arent proper
if api_key == "INSERT_KEY" :
	print("Error 1: Insert an API key before using.\n")
	sys.exit()

if username == "INSERT_USRNAME" :
	print("Error 2: Inster a username before using.\n")
	sys.exit()


# DEFINITIONS

#-------------------------------------------------------------
# Top artists data -- gets artist name and playcount

# Get url for browser view
#print("http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user="+username+"&api_key="+api_key+"&format=json&limit=1000")

# Gets json data and parses
top_artists_raw = requests.get("http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user="+username+"&api_key="+api_key+"&format=json&limit=1000")
top_artists_json = json.loads(top_artists_raw.text)

# Get total number of artists and convert to an integer to avoid "list index out of range"
total_artist_count = int(top_artists_json["topartists"]["@attr"]["total"])

def artist_playcount_function():

	# Loops through all artists
	for x in range(0, total_artist_count):

			# Get artist name and playcount through the json
			artist_name = top_artists_json["topartists"]["artist"][x]["name"]
			artist_playcount = top_artists_json["topartists"]["artist"][x]["playcount"]

			# Only prints artists that have been played more than once -- also converts artist_playcount to an interger
			if int(artist_playcount) >= 2:
				print(artist_name)
				print(artist_playcount)

#-------------------------------------------------------------	

#-------------------------------------------------------------
# Top albums data -- gets top albums and artist name

# Take input for album range
# album_number_imput = input("Display my top ___ albums: ")

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
# top_albums(album_number_imput)

#--------------------------------------------------------------









'''
save alltime scrobbles by artist and album
make a graph of albums vs scrobbles
				artists over time
'''

#debug/display full link to view in web browser
#print("https://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user="+username+"&api_key="+api_key+"&format=json")