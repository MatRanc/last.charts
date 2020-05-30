import json
import requests as rq
import random
from secret_key import *
from flask import Flask, render_template, request

app = Flask(__name__)

top_artists_rawarray = None
top_artists_playcount_rawarray = None
top_artists_acceptablerange = None
top_albums_rawarray = None
top_albums_playcount_rawarray = None
top_albums_acceptablerange = None
daterange = None
artistloadlimit = None
display_username = None
daterange_proper = None
uni_array_top_named = None
uni_array_playcount = None

display_username_randomarray = [
    "LouisVuittonDon",
    "jxns",
    "soleados",
    "tyler",
    "JQEtin",
    "cudderrr",
    "hurricane",
    "byebyebaby",
    "yyyyandHI",
    "jerome",
    "DarkFantasy",
    "chicagosessions",
    "newbody",
    "robert",
    "WSGx",
    "westlakeranch",
    "kennyy",
    "rupert3",
    "PIE",
    "yedits",
    "stanloona",
    "sifruita",
    "blonded",
    "lastone",
    "kimas",
    "NeilOO",
    "pop_xxs",
    "slab_goose",
    "10day",
    "ovo",
    "Shakeee",
    "BVFxx",
    "nikecrossfit",
    "RAGER",
    "EGODEATH",
    "ALIENS",
    "speedinbullet",
]

preload_user = [
    "shady",
    "meechymikko",
    "st-silver",
    "mynamesreed",
    "MatRanc",
    "acepear",
    "Memecycle1",
    "bladderweak",
    "luce_goose",
    "NoelThomas97",
    "kuromugiwara",
]

random_preload_user = random.choice(preload_user)

# artist load limit = 1-1000   ///   time period = overall, 7day, 1month, 3month, 6month, 12month
def load_top_artists(lastfm_username, artist_limit, time_period):

    # declares array
    global top_artists_rawarray
    global top_artists_playcount_rawarray
    global top_artists_acceptablerange

    top_artists_rawarray = []
    top_artists_playcount_rawarray = []
    top_artists_acceptablerange = 0

    # loads from api and formats
    # print("http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user="+lastfm_username+"&api_key="+lastfm_apikey+"&format=json&limit="+str(artist_limit)+"&period="+time_period)
    lastfm_apiurl_top_artists = "http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user="+lastfm_username+"&api_key="+lastfm_apikey+"&format=json&limit="+str(artist_limit)+"&period="+time_period
    top_artists_requests_json = json.loads(rq.get(lastfm_apiurl_top_artists).text)
    top_artists_total = int(top_artists_requests_json["topartists"]["@attr"]["total"])
    top_artists_perpage = int(top_artists_requests_json["topartists"]["@attr"]["perPage"])

    # if user input for artist range is bigger than whats availible, to avoid error it will display the max availible number of artists
    if top_artists_perpage <= top_artists_total:
        top_artists_acceptablerange = top_artists_perpage
    else:
        top_artists_acceptablerange = top_artists_total

    print("Loaded data for "+lastfm_username+"'s top "+str(top_artists_acceptablerange)+" artists for a time period of "+time_period+"\n")
    for x in range(top_artists_acceptablerange):
        # only adds artist to array if their playcount is greater than __
        # make this a clickable option
        if int(top_artists_requests_json["topartists"]["artist"][x]["playcount"]) >= 2:
            # adds artist name to array
            artist_name = (top_artists_requests_json["topartists"]["artist"][x]["name"]).replace("'", " ").replace("\\", " ").replace(",", ";").replace("/", " ")  # whats with artists putting \ and ' in there name?
            top_artists_rawarray.append(artist_name)

            # adds artist playcount to arrays
            artist_playcount = top_artists_requests_json["topartists"]["artist"][x]["playcount"]
            top_artists_playcount_rawarray.append(artist_playcount)
        else:
            pass

def load_top_albums(lastfm_username, album_limit, time_period): #artist load limit = 1-1000   ///   time period = overall, 7day, 1month, 3month, 6month, 12month

    #declares array
    global top_albums_rawarray
    global top_albums_playcount_rawarray
    global top_albums_acceptablerange
    
    top_albums_rawarray = []
    top_albums_playcount_rawarray = []
    top_albums_acceptablerange = 0

    #loads from api and formats
    lastfm_apiurl_albums = "http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user="+lastfm_username+"&api_key="+lastfm_apikey+"&format=json&limit="+str(album_limit)+"&period="+time_period
    top_albums_requests_json = json.loads(rq.get(lastfm_apiurl_albums).text)
    top_albums_total = int(top_albums_requests_json["topalbums"]["@attr"]["total"])
    top_albums_perpage = int(top_albums_requests_json["topalbums"]["@attr"]["perPage"])

    #if user input for artist range is bigger than whats availible, to avoid error it will display the max availible number of artists
    if top_albums_perpage <= top_albums_total:
        top_albums_acceptablerange = top_albums_perpage
    else: top_albums_acceptablerange = top_albums_total

    print("Loaded data for "+lastfm_username+"'s top "+str(top_albums_acceptablerange)+" artists for a time period of "+time_period+"\n")
    for x in range(top_albums_acceptablerange):
        #only adds artist to array if their playcount is greater than __
        #make this a clickable option
        if int(top_albums_requests_json["topalbums"]["album"][x]["playcount"]) >= 2:
            #adds artist name to array
            album_name = (top_albums_requests_json["topalbums"]["album"][x]["name"]).replace("'", " ").replace("\\", " ").replace(",",";").replace("/", " ") #whats with artists putting \ and ' in there name?
            top_albums_rawarray.append(album_name)

            #adds artist playcount to arrays
            album_playcount = top_albums_requests_json["topalbums"]["album"][x]["playcount"]
            top_albums_playcount_rawarray.append(album_playcount)
        else: pass

@app.route('/', methods=["GET", "POST"])
def home():

    # HAVE TO DEFINE IF NO CACHE (CODE BREAKS AND CAUSES ERROR 500 AS daterange AND OTHER VARIABLES ARE CALLED BEFORE DECLARE. THIS DUMMY CODE ALLOWS IT TO INITIALLY RUN THEN USES THE CACHED CODE)
    global daterange
    global artistloadlimit
    global display_username
    global daterange_proper

    load_top_artists(random_preload_user, 60, "1month")
    uni_array_top_named = top_artists_rawarray
    uni_array_playcount = top_artists_playcount_rawarray

    daterange = ""
    artistloadlimit = 1000
    display_username = str(random.choice(display_username_randomarray)+str(random.randint(0,62)))
    daterange_proper = "over the past month"

    '''
    Problems:

    ALBUM MODE:
    fix line 55 to work with album mode
    make "top_artists_acceptablerange_proper" useable with album mode too

    Need to add something to dispaly either aritsts or albums on front end text

    need to properly fix escape characters in the arrays. the hacky method isnt working well.

    need to update variables in index.html
    '''
    
    if request.method == "POST":
        display_username = str(request.form["username"])
        artistloadlimit = int(request.form["artistloadlimit"])
        daterange = str(request.form["daterange"])
        loadselect = str(request.form["loadselection"])

        if loadselect == "artists":
            result = load_top_artists(display_username, artistloadlimit, daterange)
            uni_array_top_named = top_artists_rawarray
            uni_array_playcount = top_artists_playcount_rawarray

        if loadselect == "albums":
            result = load_top_albums(display_username, artistloadlimit, daterange)
            uni_array_top_named = top_albums_rawarray
            uni_array_playcount = top_albums_playcount_rawarray

    # converts short form from api into proper english
    if daterange == "7day":
        daterange_proper = "over the past 7 days"
    else:
        pass

    if daterange == "1month":
        daterange_proper = "over the past month"
    else:
        pass

    if daterange == "3month":
        daterange_proper = "over the past 3 months"
    else:
        pass

    if daterange == "6month":
        daterange_proper = "over the past 6 months"
    else:
        pass

    if daterange == "12month":
        daterange_proper = "over the past year"
    else:
        pass

    if daterange == "overall":
        daterange_proper = "of all time"

    # for artist count
    if artistloadlimit == 1000:
        top_artists_acceptablerange_proper = ""
    else:
        top_artists_acceptablerange_proper = top_artists_acceptablerange

    return render_template(
        "index.html", 
        top_artists_rawarray=json.dumps(uni_array_top_named), 
        top_artists_playcount_rawarray=json.dumps(uni_array_playcount), 
        username=display_username, 
        top_artists_acceptablerange_proper=top_artists_acceptablerange_proper, 
        daterange_proper=daterange_proper
    )

if __name__ == "__main__":
    app.run(debug=True)
