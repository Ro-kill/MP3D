#Demo

You can see a demo of this site being used here:  https://youtu.be/ijg28Rrjr7Q 

#Installation

In order this website uses youtube_dl, and for that reason you must install it.
In terminal, execute the following:
    pip install youtube-dl --user
Make sure youtube-dl is up to date with pip install --upgrade youtube-dl

After installing youtube-dl you will still need to install one more package that did not come with youtube-dl.
If you recieve the error: "ffprobe/avprobe and ffmpeg/avconv not found. Please install one." It is because
you are missing this package.
In the terminal, execute the following:
    sudo apt-get install ffmpeg

Now you should have everything you need to run the website.

The youtube V3 data api is used for this project in order to pull video information such as video_id from a search.
This api does require a key, but I have hard coded in my own as it is rather complicated to get. If you do wish to
get and enter your own api key for this api, you would get the key through youtube developer console and enter it
into the api_key objects in helpers.py. To get the key, you must first make a project. From there scroll down to the
youtube V3 api, and click it. From here retirve your key. The api has a maximum amount of requests per day, so if the
interface ever stops working durring testing, this may be the case.

I have encountered some errors with the ide not being able to open all mp3 files due to length and size. Try to keep
downloaded content under 10 minunits. If you would like to download something more than 10 minunits and encounter
this error, export the mp3 first, and then play it.

#Description

MP3D is a flask web interface that allows users to download audio files of coresponding youtube videos with ease.
There are 3 pages that can be navigated among: Choose, Edit, and Download.

On the choose page, the user is to type a key word for the video they wish to play. A list of alerts will apear
with titles and buttons. Press the play button, and the video will open in a new tab. Press the add button, and
the video will be added to the users table for future edditing and downloading. Press the remove button next to
any song in a table, and it will be removed.

On the Edit page, the users table will apear with a text box atop it. Type a songs desired name into it and press
submit next to the song that you wish to have that title. The songs title will change, and the table will be updated.
If you press any of the remove buttons, the coresponding songs will be removed.

On the Download page, you will be able to view the table of songs that will be downloaded. You can press the
download button, and the donwload will commence. Durring the download process, the user interface will be
locked to prevent download interruption All mp3 files downloaded will appear in a folder with a name coresponding
to the users mac address.

#Options

The ammount of search results is easily changable, as the helpers.py function lookup takes two inputs. The first is
Word you would like to search, and the second is the amount of results you would like. Results can be no larger than
50.

I have maxed out the video length of search results to 20 minunits. This is because any smaller would have cut off
results at 4 minunits, and many songs are longer than that. You can change this setting in the api url in helpers.py.
Where you see "medium" in the link, you can change it to small, large, or remove it all together to yield different
search results.

Currently the output file with all the songs has a name coresponding to the users mac address. This can also be changed
in the application.py file. Whatever you change it to will be the name of your music file.
