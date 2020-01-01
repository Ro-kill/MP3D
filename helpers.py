import os
import requests
import urllib.parse
import json

from cs50 import SQL
from flask import redirect, render_template, request, session
from functools import wraps


# Opens database for edit
db = SQL("sqlite:///video.db")


# Ensurs the user has a valid mac address to save his videos to
def ip_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_ip") is None:
            return redirect("/missing")
        return f(*args, **kwargs)
    return decorated_function


# Ensures that all required sessions exist
def sessions_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("info") or session.get("added") is None:
            return redirect("/missing_info")
        if session.get("added") is None:
            return redirect("/missing_added")
        return f(*args, **kwargs)
    return decorated_function


# Finds the durration of all videos inputted by video_id
def duration(video_id):

    api_key = "AIzaSyCx9MIimTzy9osc8jIqcNdJOM2eKxJlnBI"
    #TODO: change max results output
    video_id = video_id.replace(", ", "%2C")
    r = requests.get(f"https://www.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id={video_id}&type=video&key={api_key}")
    r = r.json()
    data = json.dumps(r)
    return {data}


# Finds the top x listed videos under 4 minunits with the specified key work
def lookup(key_word, ammount):

    # Sets api key, and then requests from api, then converts output to json fine which is dumped into a string that is returned
    api_key = "AIzaSyCx9MIimTzy9osc8jIqcNdJOM2eKxJlnBI"
    r = requests.get(f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults={ammount}&q={key_word}&videoDuration=medium&type=video&key={api_key}")
    r = r.json()
    data = json.dumps(r)
    return {data}

# Converts the youtube durration output into something more ledgable
def durrationConfigure(value):

    value = value[2:]
    if "M" not in value:
        value = "M" + value
    value = value.replace("M", ":")
    value = value.replace("S", "")

    if value[0] == ":":
        value = '0' + value

    if value[-2] == ":":
        value = value[:-1] + '0' + value[-1:]

    return value

