#THIS FILE ALLOWS FOR THE SCRIPT TO BE USED LOCALLY IN THE COMMAND LINE.

from secret_key import *

import time
import pandas as pd
import requests as rq
import json

lastfm_username = "MatRanc"

def load_top_artists(artist_limit, time_period): #artist load limit = 1-1000   ///   time period = overall, 7day, 1month, 3month, 6month, 12month
    #tic1 = time.perf_counter()

    #declares array
    global top_artists_rawarray
    global top_artists_playcount_rawarray
    top_artists_rawarray = []
    top_artists_playcount_rawarray = []

    #loads from api and formats
    top_artists_requests_json = json.loads(rq.get("http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user="+lastfm_username+"&api_key="+lastfm_apikey+"&format=json&limit="+str(artist_limit)+"&period="+time_period).text)
    top_artists_numberfetched = int(top_artists_requests_json["topartists"]["@attr"]["perPage"])
    print("Loaded "+lastfm_username+"'s user data for "+str(top_artists_numberfetched)+" artists for a time period of "+time_period+"\n")

    for x in range(top_artists_numberfetched):
        #adds artist name to array
        artist_name = top_artists_requests_json["topartists"]["artist"][x]["name"]
        top_artists_rawarray.append(artist_name)

        #adds artist playcount to array
        artist_playcount = top_artists_requests_json["topartists"]["artist"][x]["playcount"]
        top_artists_playcount_rawarray.append(artist_playcount)

    #tracks time it takes to process
    #toc1 = time.perf_counter()
    #print("\nCompleted in "+str((toc1-tic1))+" seconds\n")

def load_top_artist_pandadb():
    global artists_dataframe
    #sets panda series
    top_artists = pd.Series(top_artists_rawarray)
    top_artists_playcount = pd.Series(top_artists_playcount_rawarray)
    #combines into single dataframe
    artists_dataframe = pd.DataFrame({"Artists":top_artists,"Playcount":top_artists_playcount})


load_top_artists(10, "3month")
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
