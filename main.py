from secret_key import *

import requests as rq
import json

from flask import Flask, render_template, request #$env:FLASK_APP = "main.py"
app = Flask(__name__)

def load_top_artists(lastfm_username, artist_limit, time_period): #artist load limit = 1-1000   ///   time period = overall, 7day, 1month, 3month, 6month, 12month

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

#need to edit
@app.route('/', methods=["GET", "POST"])
def home():

    load_top_artists("MatRanc", 10, "3month")

    if request.method == "POST":
        username = str(request.form["username"])
        artistloadlimit = int(request.form["artistloadlimit"])
        daterange = str(request.form["daterange"])

        result = load_top_artists(username, artistloadlimit, daterange)

    return render_template("index.html", top_artists_rawarray=json.dumps(top_artists_rawarray), top_artists_playcount_rawarray=json.dumps(top_artists_playcount_rawarray))

if __name__ == "__main__":
    app.run(debug=True)


"""
pip install:
flask
requests
openpyxl
json?
"""
