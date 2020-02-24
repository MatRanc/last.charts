import requests
import json
import sys
from userkey import *
import csv


# Error and exits if fields arent proper
if api_key == "INSERT_KEY" :
	print("Error 1: Insert an API key before using.\n")
	sys.exit()

if username == "INSERT_USRNAME" :
	print("Error 2: Inster a username before using.\n")
	sys.exit()


# Gets json data and parses
top_artists_raw = requests.get("http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user="+username+"&api_key="+api_key+"&format=json&limit=1000")
top_artists_json = json.loads(top_artists_raw.text)

# Get total number of artists and convert to an integer to avoid "list index out of range"
total_artist_count = int(top_artists_json["topartists"]["@attr"]["total"])


def artist_playcount_csv():
	# Loops through all artists
	for x in range(0, total_artist_count):

			# Get artist name and playcount through the json
			artist_name = top_artists_json["topartists"]["artist"][x]["name"]
			artist_playcount = top_artists_json["topartists"]["artist"][x]["playcount"]

			# Only prints artists that have been played more than once -- also converts artist_playcount to an interger
			if int(artist_playcount) >= 2:
				playcount_csv = open("playcount.csv", "w")
				with playcount_csv:
					writer.csvwriter(playcount_csv)
					writer.writerows(artist_name)

artist_playcount_csv()