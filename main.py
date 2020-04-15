from secret_key import *

import time
import pandas as pd
import requests as rq
import json

def load_top_artists(limit_number, time_period): #limt number = 1-1000   ///   time period = overall, 7day, 1month, 3month, 6month, 12month
    tic1 = time.perf_counter()

    #declares array
    global top_artists_rawarray
    global top_artists_playcount_rawarray
    top_artists_rawarray = []
    top_artists_playcount_rawarray = []

    #loads from api and formats
    top_artists_requests_json = json.loads(rq.get("http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user="+lastfm_username+"&api_key="+lastfm_apikey+"&format=json&limit="+str(limit_number)+"&period="+time_period).text)
    top_artists_numberfetched = int(top_artists_requests_json["topartists"]["@attr"]["perPage"])
    print("Loaded user data from "+str(top_artists_numberfetched)+" artists")

    for x in range(top_artists_numberfetched):
        #adds artist name to array
        artist_name = top_artists_requests_json["topartists"]["artist"][x]["name"]
        top_artists_rawarray.append(artist_name)

        #adds artist playcount to array
        artist_playcount = top_artists_requests_json["topartists"]["artist"][x]["playcount"]
        top_artists_playcount_rawarray.append(artist_playcount)

    #tracks time it takes to process
    toc1 = time.perf_counter()
    print("\nCompleted in "+str((toc1-tic1))+" seconds\n")

load_top_artists(50, "6month")

top_artists = pd.Series(top_artists_rawarray)
top_artists_playcount = pd.Series(top_artists_playcount_rawarray)

artists_dataframe = pd.DataFrame({"Artists":top_artists,"Playcount":top_artists_playcount})

print(artists_dataframe)
artists_dataframe.to_excel(r"D:\Development\last.charts\output\useroutput.xlsx")

#top_artists = pd.Series(["Kanye West", "Kid Cudi", "Travis Scott", "Chance the Rapper", "Pusha T"])
#top_artists_playcount = pd.Series([3630,1927,428,310,281])
