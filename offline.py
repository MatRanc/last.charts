#THIS FILE ALLOWS FOR THE SCRIPT TO BE USED LOCALLY IN THE COMMAND LINE.

from secret_key import *

import time
import pandas as pd
import requests as rq
import json

def load_top_artists(lastfm_username, artist_limit, time_period): #artist load limit = 1-1000   ///   time period = overall, 7day, 1month, 3month, 6month, 12month

    #declares array
    global top_artists_rawarray
    global top_artists_playcount_rawarray
    top_artists_rawarray = []
    top_artists_playcount_rawarray = []

    #loads from api and formats
    top_artists_requests_json = json.loads(rq.get("http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user="+lastfm_username+"&api_key="+lastfm_apikey+"&format=json&limit="+str(artist_limit)+"&period="+time_period).text)
    top_artists_total = int(top_artists_requests_json["topartists"]["@attr"]["total"])
    top_artists_perpage = int(top_artists_requests_json["topartists"]["@attr"]["perPage"])

    #if user input for artist range is bigger than whats availible, to avoid error it will display the max availible number of artists
    if top_artists_perpage < top_artists_total:
        top_artists_acceptablerange = top_artists_perpage
    else: top_artists_acceptablerange = top_artists_total

    print("Loaded data for "+lastfm_username+"'s top "+str(top_artists_acceptablerange)+" artists for a time period of "+time_period+"\n")

    for x in range(top_artists_acceptablerange):
        #adds artist name to array
        artist_name = top_artists_requests_json["topartists"]["artist"][x]["name"]
        top_artists_rawarray.append(artist_name)

        #adds artist playcount to arrays
        artist_playcount = top_artists_requests_json["topartists"]["artist"][x]["playcount"]
        top_artists_playcount_rawarray.append(artist_playcount)

def load_top_artist_pandadb():
    global artists_dataframe
    #sets panda series
    top_artists = pd.Series(top_artists_rawarray)
    top_artists_playcount = pd.Series(top_artists_playcount_rawarray)
    #combines into single dataframe
    artists_dataframe = pd.DataFrame({"Artists":top_artists,"Playcount":top_artists_playcount})


load_top_artists("MatRanc", 1000, "12month")
load_top_artist_pandadb()

print(artists_dataframe)

artists_dataframe.to_excel(r"D:\Development\last.charts\output\useroutput.xlsx")

#top_artists = pd.Series(["Kanye West", "Kid Cudi", "Travis Scott", "Chance the Rapper", "Pusha T"])
#top_artists_playcount = pd.Series([3630,1927,428,310,281])

"""
pip install:
flask
requests
pandas
openpyxl
"""
