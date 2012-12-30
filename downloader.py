#Copyright Scott Opell 2012
#Licensed under the GPL license, see COPYING
import urllib2
import re
import pprint
import argparse
import os
import sys
import subprocess
from urlparse import urlparse
try:
    import simplejson as json
except ImportError:
    import json

class ConversionError(Exception):
    """Exception raised for error during conversion process
    Attributes:
        expr -- expression in which the error occurred
        msg  -- explanation of the error
    """
    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg

def ensure_dir(f):  #stolen from http://stackoverflow.com/questions/273192/python-best-way-to-create-directory-if-it-doesnt-exist-for-file-write
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

#takes a path to an m4a and returns the path to an mp3, will attempt to delete the m4a on successful conversion
def to_mp3(m4a_path):
    wav_path = m4a_path[:-4] + ".wav"
    mp3_path = m4a_path[:-4] + ".mp3"
    subprocess.call(["faad", '-o', wav_path, m4a_path])
    subprocess.call(["lame", '-h', '-b', '128', wav_path, mp3_path])
    os.remove(wav_path)
    if f.open(mp3_path, "r") is not None:
        os.remove(m4a_path)
        return mp3_path
    else:
        raise ConversionError(m4a_path, "mp3 file path is None for some reason")

pp = pprint.PrettyPrinter(indent=4)
parse = argparse.ArgumentParser(description = "Get valid playlist url/id and api key")
parse.add_argument('-u', '--playlist_url', required = True, help = "the URL of the playlist to be downloaded")
parse.add_argument('-a', '--API_key', required = True, help = "the URL of the playlist to be downloaded")
parse.add_argument('-d', '--save_directory', required = False, default = "./", help = "the directory where the files will be saved")
parse.add_argument('-mp3', required = False, help = "if this is present then files will be output in mp3 format")

args = parse.parse_args()

api = args.API_key
mp3 = False
if args.mp3 is not None:
    mp3 = True

if len(api) != 40:
    sys.exit("invalid api key")

try:
    urllib2.urlopen(args.playlist_url)
except:
    sys.exit("invalid URL")
    raise 


#initialize api and get playtoken
api_url = 'http://8tracks.com/sets/new.json?api_key='+api
url = urllib2.urlopen(api_url)
json_result = json.load(url)
play_token = json_result[unicode('play_token')]

#get playlist id from the playlist url given
playlist_url = args.playlist_url
url = urllib2.urlopen(playlist_url)
data = url.read()
matches = re.search(r'mixes/(\d+)/player',data)  #seach through raw html for string mixes/#######/player, kind of messy, but best method currently
if matches.group(0) is not None:
    playlist_id = matches.group(1) #this chooses the first match, its possible that 8tracks could change this later, but this works for now
else:
    sys.exit("invalid URL or 8tracks has updated to break compatibility, if the latter, contact me")
#possible improvement to above, list all matches and take mode

#get playlist "loader" basically the variable that will return song urls and will be iterated through
playurl = 'http://8tracks.com/sets/'+play_token+'/play?mix_id='+playlist_id+'&format=jsonh&api_key=' + api
url = urllib2.urlopen(playurl)
playlist_loader = json.load(url)

pp.pprint(playlist_loader)

#get playlist info
playlist = 'http://8tracks.com/mixes/'+playlist_id+'.json?api_key='+api
url = urllib2.urlopen(playlist)
playlist_info = json.load(url)

#pp.pprint(playlist_info)

#store playlist name from above
playlist_name = playlist_info['mix']['name']

#get directory ready for some new tunes
directory = os.path.join(args.save_directory,playlist_name)
#os.makedirs(directory)
try:
    ensure_dir(os.path.join(directory, "test.txt"))
except:
    print "invalid path given, saving to current directory instead"
    directory = os.path.join(args.save_directory,playlist_name)
    raise



at_end = False
song_number = 1
while not at_end:
    curr_song_url = playlist_loader['set']['track']['track_file_stream_url']
    curr_artist = playlist_loader['set']['track']['performer']
    curr_song_title = playlist_loader['set']['track']['name']
    curr_year = playlist_loader['set']['track']['year']
    curr_album = playlist_loader['set']['track']['release_name']
    actual_url = urllib2.urlopen(curr_song_url).geturl()
    parsed_url = urlparse(actual_url)
    filetype = parsed_url.path[len(parsed_url.path)-4:len(parsed_url.path)]
    file_name = (str(song_number) + u' - ' + curr_artist + u'-' + curr_song_title + u' (' + str(curr_year) + u')' + filetype).encode('UTF-8')
    file_path = os.path.join(directory, unicode(file_name,errors='ignore'))
    if bool(os.access(file_path, os.F_OK)):
        print "File number "+str(song_number)+" already exists!"
    else:
        print "Downloading " + file_name
        u = urllib2.urlopen(curr_song_url)
        f = open(file_path,'wb')
        f.write(u.read())
        if mp3 and not (filetype == ".mp3"):
            try:
                to_mp3(file_path)
            finally:
                print "an error has occured converting track number " + str(song_number) + "to mp3 format, tracks will be left in m4a format"
    song_number +=1
    #rerun this snippet from earlier to load information about next song
    playurl = 'http://8tracks.com/sets/'+play_token+'/next?mix_id='+playlist_id+'&format=jsonh&api_key=' + api
    url = urllib2.urlopen(playurl)
    playlist_loader = json.load(url)

    #check to see if its at the end of the playlist
    if playlist_loader['set']['at_end'] == True:
        at_end = True
print "Done, files can be found in "+directory