8tracks-downloader-python
=========================

Downloads a given playlist from 8tracks to your computer

Inspired and partially based on the php 8tracks downloader created by navinpai and mundofr
https://github.com/mundofr/8Tracks-Downloader

Usage
=====
usage is pretty basic, script is run from command line arguments

    usage: downloader.py [-h] -u PLAYLIST_URL -a API_KEY [-d SAVE_DIRECTORY]
    

-h        ==>           displays help file (above)

-u --playlist_url ==>   any standard 8tracks url, ex `http://8tracks.com/dj-cass/make-some-noise`

-a --API_key       ==> api key, can be obtained here http://8tracks.com/developers/new  usually takes a few days

-d --save_directory ==> OPTIONAL  where the playlists will be saved to, if this is `c:/music` and the playlist above is the given
                     argument, then file structure will be `c:/music/make some noise/(songs).m4a`  defaults
                     to the same directory


ToDo
====
* Convert to mp3 on the fly because nobody likes 
* Create m3u playlist files of each
* Add in Song Metadata
