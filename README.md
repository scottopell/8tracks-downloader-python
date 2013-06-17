8tracks-downloader-python
=========================

Downloads a given playlist from 8tracks to your computer

Inspired and partially based on the php 8tracks downloader created by navinpai and mundofr
https://github.com/mundofr/8Tracks-Downloader


Usage
=====
usage is pretty basic, script is run from command line arguments

    usage: downloader.py [-h] -u PLAYLIST_URL -a API_KEY [-d SAVE_DIRECTORY] [-mp3 MP3]

    `C:\Users\scott\Google Drive\projects\8tracks-downloader-python>downloader.py -u http://8tracks.com/dj-cass/new-year-party -a 7ad5c(censored)4eb83987e -d "c:\8tracks_downloads" -mp3`



for id3 tagging, download this package and put ID3.py in the same directory you're running the script from, or set it up through python
    

-h        ==>           displays help file (above)

-u --playlist_url ==>   any standard 8tracks url, ex `http://8tracks.com/dj-cass/make-some-noise`

-a --API_key       ==> api key, can be obtained here http://8tracks.com/developers/new  usually takes a few days, hexadecimal, 40 chars long

-d --save_directory ==> OPTIONAL  where the playlists will be saved to, if this is `c:/music` and the playlist above is the given
                     argument, then file structure will be `c:/music/make some noise/(songs).m4a`  defaults
                     to the same directory

-mp3 ==>  usage `-mp3` forces conversion of everything to mp3 even if its not already in mp3 format, **requires faad and lame**, see below for further instruction 

### MP3 Support ###
#### Windows ####
 http://www.rarewares.org/mp3-lame-bundle.php and http://www.rarewares.org/aac-decoders.php are both required, make sure the exe files end up in the Windows PATH or in the same directory as downloader.py
#### Linux  ####
 Untested, but LAME and FAAD should both be able to be installed from your distros package management, ie `sudo apt-get install faad lame`

### ID3 Tagging ###
download and set up id3-py, which can be found at its home here http://id3-py.sourceforge.net/
its basic and a little old, but it works for our purposes
If you're feeling especially lazy you don't even have to install it, you can just copy id3.py into the same directory as downloader.py and go to town

Notes
=====
Even though its inconvenient it really is neccessary to get your own api key.

Dev. Notes
==========
Previously 8tracks stored all songs as m4a files, now it seems the majority are stored in mp3 format, maybe all of them, can't tell for sure -mp3 option may not be needed, I have included it just in case.

UPDATE: m4a's do exist and this has been tested with them.


ToDo
====
~~Convert to mp3 on the fly because nobody likes m4a~~

~~Create m3u playlist files of each~~

~~Add in Song Metadata~~
