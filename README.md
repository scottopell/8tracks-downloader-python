8tracks-downloader-python
=========================

Downloads a given playlist from 8tracks to your computer

Inspired and partially based on the php 8tracks downloader created by navinpai and mundofr
https://github.com/mundofr/8Tracks-Downloader

Usage
=====
usage is pretty basic, script is run from command line arguments

    usage: downloader.py [-h] -u PLAYLIST_URL -a API_KEY [-d SAVE_DIRECTORY] [-mp3 MP3]
    

-h        ==>           displays help file (above)

-u --playlist_url ==>   any standard 8tracks url, ex `http://8tracks.com/dj-cass/make-some-noise`

-a --API_key       ==> api key, can be obtained here http://8tracks.com/developers/new  usually takes a few days

-d --save_directory ==> OPTIONAL  where the playlists will be saved to, if this is `c:/music` and the playlist above is the given
                     argument, then file structure will be `c:/music/make some noise/(songs).m4a`  defaults
                     to the same directory

-mp3 ==> forces conversion of everything to mp3 even if its not already in mp3 format, requires faad.exe and lame.exe to be in the system path, these might be able to be found at rarewares.org
 usage `-mp3 True'

Notes
=====
Even though its inconvenient it really is neccessary to get your own api key, otherwise 8tracks would shut this down very quickly

Dev. Notes
==========
Previously 8tracks stored all songs as m4a files, now it seems the majority are stored in mp3 format, -mp3 option may not be needed, I have included it just in case

ToDo
====
~~* Convert to mp3 on the fly because nobody likes m4a~~
* Create m3u playlist files of each
* Add in Song Metadata
