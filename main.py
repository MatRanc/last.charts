from secret_key import *

import requests as rq
import json

from flask import Flask, render_template, request, json #$env:FLASK_APP = "main.py"
app = Flask(__name__)

def load_top_artists(lastfm_username, artist_limit, time_period): #artist load limit = 1-1000   ///   time period = overall, 7day, 1month, 3month, 6month, 12month

    #declares array
    global top_artists_rawarray
    global top_artists_playcount_rawarray
    global top_artists_acceptablerange
    top_artists_rawarray = []
    top_artists_playcount_rawarray = []

    #loads from api and formats
    top_artists_requests_json = json.loads(rq.get("http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user="+lastfm_username+"&api_key="+lastfm_apikey+"&format=json&limit="+str(artist_limit)+"&period="+time_period).text)
    top_artists_total = int(top_artists_requests_json["topartists"]["@attr"]["total"])
    top_artists_perpage = int(top_artists_requests_json["topartists"]["@attr"]["perPage"])

    #if user input for artist range is bigger than whats availible, to avoid error it will display the max availible number of artists
    if top_artists_perpage <= top_artists_total:
        top_artists_acceptablerange = top_artists_perpage
    else: top_artists_acceptablerange = top_artists_total

    print("Loaded data for "+lastfm_username+"'s top "+str(top_artists_acceptablerange)+" artists for a time period of "+time_period+"\n")

    for x in range(top_artists_acceptablerange):
        #adds artist name to array
        artist_name = (top_artists_requests_json["topartists"]["artist"][x]["name"]).replace("'", " ").replace("\"", " ") #whats with artists putting \ and ' in there name???
        top_artists_rawarray.append(artist_name)

        #adds artist playcount to arrays
        artist_playcount = top_artists_requests_json["topartists"]["artist"][x]["playcount"]
        top_artists_playcount_rawarray.append(artist_playcount)

@app.route('/', methods=["GET", "POST"])
def home():

    load_top_artists("MatRanc", 1000, "1month")

    #HAVE TO DEFINE IF NO CACHE (CODE BREAKS AND CAUSES ERROR 500 AS daterange AND OTHER VARIABLES ARE CALLED BEFORE DECLARE. THIS DUMMY CODE ALLOWS IT TO INITIALLY RUN THEN USES THE CACHED CODE)
    global daterange
    daterange = ""
    global artistloadlimit
    artistloadlimit = 1000
    global username
    username = "sev"
    global daterange_proper
    daterange_proper = "the past month"


    if request.method == "POST":
        username = str(request.form["username"])
        artistloadlimit = int(request.form["artistloadlimit"])
        daterange = str(request.form["daterange"])

        result = load_top_artists(username, artistloadlimit, daterange)

    #converts short form from api into proper english
    if daterange == "7day":
        daterange_proper = "over the past 7 days"
    else: pass

    if daterange == "1month":
        daterange_proper = "over the past month"
    else: pass

    if daterange == "3month":
        daterange_proper = "over the past 3 months"
    else: pass

    if daterange == "6month":
        daterange_proper = "over the past 6 months"
    else: pass

    if daterange == "12month":
        daterange_proper = "over the past year"
    else: pass

    if daterange == "overall":
        daterange_proper = "of all time"

    #for artist count
    if artistloadlimit == 1000:
        top_artists_acceptablerange_proper = ""
    else: top_artists_acceptablerange_proper = top_artists_acceptablerange

    return render_template("index.html", top_artists_rawarray=json.dumps(top_artists_rawarray), top_artists_playcount_rawarray=json.dumps(top_artists_playcount_rawarray), username=username, top_artists_acceptablerange_proper=top_artists_acceptablerange_proper, daterange_proper=daterange_proper)

if __name__ == "__main__":
    app.run(debug=True)


'''
required packages?:
flask
requests
openpyxl
json?
'''
