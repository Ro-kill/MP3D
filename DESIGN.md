Overview

    MP3D is a project designed to make youtube song downloads easy. It is a flask based website with simple
    user interface.

Requirements

    The web interface relies on storing all added songs in a database with a table whose name is the same as
    the user's mac id address. This allows songs to remain stored for future download if the user wished to
    close out of the program.

    Because of how crucial this is, I have implemented a function which checks that the user has an address
    stored in his session["user_id"] before any routes can be called. If the user has no address, then a route
    "/missing" is called which firsts checks for an address (if none are found, "missing.html" is rendered)
    and then puts the outputted value into session["user_ip"]. At this time, a sqlite table, if not already
    existing, is made with the same name as session["user_ip"]. This table will be used throughout the program
    to hold all desired songs as well as desired song information.

    The program also relies on two sessions, specifically session["added"], and session["info"]. Because they
    are needed from the beginning, they are declared with session["user_ip"] at the start of the program.
    Session["added"] is designed to store all songs the user desires, so it is quickly set to the output of
    db.execute("SELECT * FROM {user_ip}").

    All HTML files are built off a layout with a navbar. This navbar allows users to easily move about the
    three pages. I also took the liberty to design and create my own logo and name for the website.
    MP3D stands for mp3 Downloader, and has a pair of 3-D glasses as the logo.

Home screen

    The home screen of MP3D contains a search bar, and a list. Fun fact: This is the only form for the
    entirity of this project. When search is clicked, the information in the search bar is routed to the
    "/" "POST" method. Here, the data is passed through several methods that pull all the api data needed,
    and plugs it all into the session["info"]. Then info is passed into index.html, and all values
    are displayed as alerts with song title, duration, likes, dislikes, and two buttons.

    What is not displayed, but instead lays hidden under each alert is a number holder. Although not visible,
    it is within the buttons div's, so when pushed we can pull the song number associated with each button
    through some variation of $("id").sibling("song_number").html(). This was the only way I could conceive of having
    a separate button for each alert, as opposed to one form for all the alerts where the user would need to
    enter the title of the song they chose.

    The two buttons per alert are play and add. When clicked, they commence a function in javascript.
    First, using a variation of this.sibling("id").html(), the video number is pulled. From here, an ajax function
    is called which pushes this data into a route.

        Play pushes the data into the "/play" route. From here, the video_id is found by pulling all video
        data from session["info"][number]. This video_id is then passed back the ajax function which launches
        a new tab with the url ("www.yout..." + video_id).

        Add, similarly pushed this data through ajax, but to the route "/appendV". From here, the data similarly
        pulls all wanted data from session["info"][number], but this time instead of returning it, it inserts it into
        a the users corresponding table (of name user_ip). Then session["added"] is updated to the latest table
        and returned. ajax takes this returned data and builds a new table with it that contains all the users
        added songs.


    The home screen of MP3D also contain a table. The table holds the names for all songs that the user has added.
    It also contains a hidden tag, in which is the primary key for each song in the added table. Next to each song
    in the table, there is a button remove, and when clicked removes the video. It does this by finding the value
    of the clicked songs primary key - with a variation of this.sibling("id").html() - and then passes this information
    through an ajax command which then directes the data through the route "/removeV". This route removes the row
    with the returned primary key, updates session["added"], and then returns session["added"]. The ajax
    .done(function) takes this data, and builds a new table which it sets the tableBody's innerHTML to.

Edit

    The edit page allows users to change the names of the songs they have chosen to download. If the youtube video
    has some long and obscure name with lots of # and CAPITALIZED WORDS (which happens more often than not), the
    user is able to change it.

    The "/chosen" path, contains both a "GET" and a "POST" request. On call "GET", the edit template is rendered,
    and the user is brought to the page where they can change the names of their songs.

    The interface for this is a text input, and a button next to each song called submit. Once again, I have implemented
    hidden tags per table element allowing the button, on click, to pull the corresponding video id. When submit is clicked, it
    finds this id as well, as the current text value in the input, and pushed it through an ajax call to the path "/chosen"
    "POST". This path takes the two inputs and updates the name of the song row with primary key equal the number to the
    new name. Then session["added"] is updated and returned to .done function. Here, the table is remade, and the innerHTML
    of the tableBody is refreshed.

    The interface also allows for users to remove songs from the edit page, and functions all the same as the remove buttons
    on the home page.

Download

    The download page allows users to review all the mp3.files they will be downloading, and by the click of a button, download
    them. The page has a table with all the user's song, and a download button at the bottom.

    When the button is clicked, a div is revealed that covers the entire screen. This prevents user interface for the corse
    of download, ensuring the files download in peace. After revealing the div, an ajax call is made to the route "/download",
    where a loop runs through every song in the session["added"]. With each loop, the data of the song is passed into the
    youtube-dl module which downloads them to a folder with the name of user_id + "_videos". Then the user_ip table is cleared, and
    session["added"] is updated to the cleared table. Upon the success of the route "/download", the ajax call hides the div
    re-enabiling user interface and updates the table to nothing (as the users table was cleared).

API

    Setting up the different api's was probably the most time consuming and frustrating part of this project. Now that I have
    figured it out through hours of trial and error, I have a pretty good understanding of what is happening. Upon the api call,
    I set a variable equal the api's output. This returns a json object. From here, I dump all the json data into a string because
    json objects can not be hashed, and thus can not be passed through from helpers.py to application.py. On the passing of this
    string, it is reformatted into a set, where the json string is the first input. To over come this, I loop through the set, and
    break after the first itteration, loading the string into the data variable as a json.

    This is all well and good, getting all this data as a single json. But this first youtube api did not have all the data I needed.
    In addition to the video_id, the likes, and the dislikes, I also needed the durration of each video. To do this, I needed to pass
    all the video_id's into a list, and then pass that list into an api. I then needed to repeat this whole conversion process, as my
    second api function was also in application.py. Looking back on it, it would have worked better to simply keep my api functions in
    the application.