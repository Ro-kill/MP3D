import os
import json
import uuid
import webbrowser
import youtube_dl

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import ip_required, lookup, duration, durrationConfigure

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///video.db")


# Secures user_ip
@app.route("/missing")
def missing():

    # Pulls mac address
    session.clear()
    user_ip = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])

    # Returns missing.html if no mac address is found
    if not user_ip:
        return render_template("missing.html")

    # Adds mac address to session
    else:
        session["user_ip"] = user_ip
        session["info"] = []

        # Creates sqlite table for the user (with name = mac address) if it does not already exist
        db.execute("CREATE TABLE IF NOT EXISTS :user_ip (number INTEGER PRIMARY KEY NOT NULL, video_id VARCHAR(12) NOT NULL, name VARCHAR(50) NOT NULL, durration VARCHAR(10), changed BOOLEAN)", user_ip = user_ip)
        session["added"] = db.execute("SELECT * FROM :user_ip", user_ip = session["user_ip"])
        return redirect("/")


# Home Route
@app.route("/", methods=["GET", "POST"])
@ip_required
def index():

    if request.method == "POST":

        info = []

        # Pulls key word from textBox, pushes it into api function and pulls data into data object
        key_word = request.form.get("key_word")
        r = lookup(key_word, 10)
        for e in r:
            data = json.loads(e)
            break

        # If no data is returned, it means the requests are maxed out, and notifies the user accordingly
        if not data:
            return render_template("requestsMaxed.html")

        # Fills video_id list with video_ids
        video_id = []
        for result in data["items"]:
            video_id.append(result["id"]["videoId"])

        # Formats video_id into useable data, and passes it into another youtube api which returns additional info about the videos
        holder = str(video_id)
        holder = holder.replace("'", "")
        holder = holder.replace("[", "")
        holder = holder.replace("]", "")
        r = duration(holder)
        for e in r:
            dur = json.loads(e)
            break

        # If no data is returned, it means the requests are maxed out, and notifies the user accordingly
        if not data:
            return render_template("requestsMaxed.html")

        # Appends info with information from data
        for result in data["items"]:
            temp = []
            temp.append(result["id"]["videoId"])
            temp.append(result["snippet"]["title"])
            info.append(temp)

        # Appends info with information from dur
        counter = 0
        for result in dur["items"]:
            temp = []
            holder = result["contentDetails"]["duration"]
            durration = durrationConfigure(holder)
            temp.append(durration)
            temp.append(result["statistics"]["likeCount"])
            temp.append(result["statistics"]["dislikeCount"])
            temp.append(counter)
            for stats in temp:
                info[counter].append(stats)
            counter += 1

        # Sets session value to info
        session["info"] = info

        # Renders index template with searched song info
        session["added"] = db.execute("SELECT * FROM :user_ip", user_ip = session["user_ip"])
        return render_template("index.html", info = session["info"], added = session["added"])

    else:

        # Renders index with only the added songs (as no post request was made)
        if session.get('added') is None:
            session["added"] = db.execute("SELECT * FROM :user_ip", user_ip = session["user_ip"])
        return render_template("index.html", info = session["info"], added = session["added"])


# Adds video to "added"
@app.route("/appendV", methods=['POST'])
@ip_required
def appendV():

    # Sets variabl values to video_id, durration, and name from info
    number = int(request.form['video_number'])
    temp = session["info"][number]
    video_id = temp[0]
    durration = temp[2]
    name = temp[1]

    # Adds the variables to the
    user_ip = session["user_ip"]
    db.execute("INSERT INTO :user_ip (video_id, name, durration, changed) VALUES (:video_id, :name, :durration, 'FALSE')", user_ip = user_ip, video_id = video_id, durration = durration, name = name)

    # Sets and returns session value
    session["added"] = db.execute("SELECT * FROM :user_ip", user_ip = user_ip)
    return jsonify(session["added"])


# Removes video from "added"
@app.route("/removeV", methods=['POST'])
@ip_required
def removeV():

    user_ip = session["user_ip"]
    number = request.form['added_number']

    # Deletes row in table, user_ip, with primary key "number"
    db.execute("DELETE FROM :user_ip WHERE number = :number", user_ip = user_ip, number = number)

    # sets and returns session value
    session["added"] = db.execute("SELECT * FROM :user_ip", user_ip = user_ip)
    return jsonify(session["added"])


# Opens video in new tab
@app.route("/play", methods = ['POST'])
@ip_required
def play():
    # Prepares variable url for usage
    number = int(request.form['video_number'])
    temp = session["info"][number]
    url = temp[0]

    # Returns accessable url information for the use of opening a new tab with the url
    return jsonify({"id" : url})


# Provides for name changing of videos
@app.route("/chosen", methods=['GET', 'POST'])
@ip_required
def chosen():

    if request.method == 'POST':

        user_ip = session["user_ip"]

        # Pulls name and video_number from html file
        number = request.form['number']
        newName = request.form['newName']

        # Updates sqlite table, and returns changed session value "added"
        if newName:
            db.execute("UPDATE :user_ip SET name = :name, changed = 'true' WHERE number = :number", user_ip = user_ip, name = newName, number = number)
            session["added"] = db.execute("SELECT * FROM :user_ip", user_ip = user_ip)
            return jsonify(session["added"])

        # Returns that there is missing data
        return jsonify({'error' : 'Missing data!'})

    else:

        # Renders template added.html with session value "added"
        if session.get('added') is None:
            session["added"] = db.execute("SELECT * FROM :user_ip", user_ip = session["user_ip"])
        return render_template("added.html", added = session["added"])


# Downloads all videos in global variable "added"
@app.route("/download", methods = ['GET', 'POST'])
@ip_required
def download():

    if request.method == 'POST':

        # Loops through session variable "added" and downloads every video in it
        user_ip = session["user_ip"]
        for row in session["added"]:
            outtmpl = user_ip + '_videos/'+ row["name"] + '.%(ext)s'
            song_url = "https://www.youtube.com/watch?v=" + row["video_id"]
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': outtmpl,
                'postprocessors': [
                    {'key': 'FFmpegExtractAudio','preferredcodec': 'mp3',
                     'preferredquality': '192',
                    },
                    {'key': 'FFmpegMetadata'},
                ],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(song_url, download=True)

        # Delets all rows in the sqlite table by the name of :user_ip
        db.execute("DELETE FROM :user_ip", user_ip = user_ip)
        session["added"] = db.execute("SELECT * FROM :user_ip", user_ip = session["user_ip"])

        return jsonify({})

    else:

        # Renders template added.html with session variable "added"
        if session.get('added') is None:
            session["added"] = db.execute("SELECT * FROM :user_ip", user_ip = session["user_ip"])
        return render_template("download.html", added = session["added"])