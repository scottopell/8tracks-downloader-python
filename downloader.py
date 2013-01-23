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
from ID3 import *

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

def norm_year(y):
    if y == '':
        return 0
    try:
        int(y)
        return y
    except:
        return 0

#takes a path to an m4a and returns the path to an mp3, will attempt to delete the m4a on successful conversion
def to_mp3(m4a_path):
    wav_path = m4a_path[:-4] + ".wav"
    mp3_path = m4a_path[:-4] + ".mp3"
    subprocess.call(["faad", '-o', wav_path, m4a_path])
    subprocess.call(["lame", '-h', '-b', '128', wav_path, mp3_path])
    try:
        os.remove(wav_path)
    except WindowsError:
        print "windows error, error deleting wav"
    if os.path.isfile(mp3_path):
        try:
            os.remove(m4a_path)
        except WindowsError:
            print "Windows cannot delete the original m4a file, feel free to delete it manually after conversion"
        return mp3_path
    else:
        raise ConversionError(m4a_path, "mp3 file path does not exist for some reason")

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

#pp.pprint(playlist_loader)

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
m3u = []
while not at_end:
    #song metadata/info
    curr_song_url = playlist_loader['set']['track']['track_file_stream_url']
    curr_artist = playlist_loader['set']['track']['performer']
    curr_song_title = playlist_loader['set']['track']['name']
    curr_year = norm_year(playlist_loader['set']['track']['year'])
    curr_album = playlist_loader['set']['track']['release_name']
    #tracing through redirects
    actual_url = urllib2.urlopen(curr_song_url).geturl()
    parsed_url = urlparse(actual_url)
    #gets the filetype designated by the server
    filetype = parsed_url.path[len(parsed_url.path)-4:len(parsed_url.path)]

    mp3_name = (str(song_number) + u' - ' + curr_artist + u'-' + curr_song_title + u' (' + str(curr_year) + u')' + ".mp3").encode('UTF-8')
    file_name = (str(song_number) + u' - ' + curr_artist + u'-' + curr_song_title + u' (' + str(curr_year) + u')' + filetype).encode('UTF-8')
    file_path = os.path.join(directory, unicode(file_name,errors='ignore'))
    if bool(os.access(file_path, os.F_OK)):# and filetype == ".m4a" and mp3:
        print "File number "+str(song_number)+" already exists!"
    elif os.path.isfile(os.path.join(directory, unicode(mp3_name, errors='ignore'))):
        print "File number "+str(song_number)+" already exists in mp3 format!"
        file_name = mp3_name
    else:
        print "Downloading " + file_name
        u = urllib2.urlopen(curr_song_url)
        f = open(file_path,'wb')
        f.write(u.read())
        f.close()
        if mp3 and not (filetype == ".mp3"):
            try:
                to_mp3(file_path)
                file_name = mp3_name
                file_path = os.path.join(directory, file_name)
            except ConversionError:
                print "an error has occured converting track number " + str(song_number) + " to mp3 format, track will be left in m4a format"
        if file_name[len(file_name)-4:len(file_name)] == ".mp3":
            #working here, this happens if the conversion was absolutely succesful, no access errors
            print "great success"
        try:
            id3info = ID3(file_path)
            id3info['TITLE'] = curr_song_title.encode("ascii", "ignore").decode()
            id3info['ARTIST'] = curr_artist.encode("ascii", "ignore").decode()
            id3info['ALBUM'] = curr_album.encode("ascii", "ignore").decode()
            id3info['YEAR'] = str(curr_year)
        except InvalidTagError, message:
            print "Invalid ID3 tag:", message
    m3u.append(file_name)
    song_number += 1
    #rerun this snippet from earlier to load information about next song
    playurl = 'http://8tracks.com/sets/'+play_token+'/next?mix_id='+playlist_id+'&format=jsonh&api_key=' + api
    url = urllib2.urlopen(playurl)
    playlist_loader = json.load(url)

    #check to see if its at the end of the playlist
    if playlist_loader['set']['at_end'] == True:
        at_end = True
m3u_path = os.path.join(directory, playlist_name + ".m3u")
m3u_file = open(m3u_path, 'w')
m3u_file.write("\n".join(m3u))
m3u_file.close()
print "Done, files can be found in "+directory