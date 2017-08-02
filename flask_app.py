#!/var/www/html/optimalvibes/bin python


from flask import Flask, render_template, request, jsonify, send_from_directory, url_for, redirect, send_from_directory

import urllib
import base64
import requests
import json
import subprocess
import logging
import os
import time
#from flaskext.mysql import MySQL
from globals import Globals
import sys
sys.path.append(Globals.SERVICES_PATH)

from app import app
# A very simple Flask Hello World app for you to get started with...

from flask import Flask

##########################################
#   IMPORT ALL SERVICES INTO APP         #
##########################################
from server.status import Status
from server.services.spotify.spotify import SpotifyInterface
from server.services.youtubeDL.youtubedl import YoutubeDLInterface
from server.services.youtubeData.youtubeData import YoutubeInterface

from server.services.id3.id3 import ID3TagEditInterface
from server.models.playlists import PlaylistModel


#from server.globals import Globals


# TEMPLATE_PATH = 'client/templates'
# STATIC_PATH = '/static'					# hostname.com/public/image/daniel.jpg
# STATIC_FOLDER = 'client/static'

logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)


#############################
# define base url endpoints #
#############################
URL_IDENTIFIERS = {
	'youtube-playlist' : 'www.youtube.com/playlist?list=' ,
	'spotify-playlist' : 'spotify:user:',
	'youtube-song' : 'https://www.youtube.com/watch?v='
}



# app = Flask(__name__,
# 			template_folder=TEMPLATE_PATH,
# 			static_url_path=STATIC_PATH,
# 			static_folder=STATIC_FOLDER
# 			)
# app.config['DEBUG'] = True



# #############################
# # connect with MYSQL        #
# #############################
# app.config['MYSQL_DATABASE_USER'] = Globals.DB['username']
# app.config['MYSQL_DATABASE_PASSWORD'] = Globals.DB['password']
# app.config['MYSQL_DATABASE_DB'] = Globals.DB['dbname']
# app.config['MYSQL_DATABASE_HOST'] = Globals.DB['host']




#############################
# integrate with different  #
# interfaces				#
#############################
SPInterface = SpotifyInterface()
YTDLInterface = YoutubeDLInterface()
ID3Interface = ID3TagEditInterface()
YoutubeDataInterface = YoutubeInterface()

PlaylistModelInst = PlaylistModel()

#
#
#	Convert: ls -l /downloads/song one.mp3
#		 To: ls -l /downloads/song\ one.mp3
#

def escapeCMD(filename):
	""" escape filenames with spaces """
	return "\\".join(filename.split())




	#
# zip the files in the playlist
#
def zipPlaylist(file_paths, playlist_id):

	###################################
	# !!!!! THIS WORKS DUMBASS !!!!  !#
	# zip -m 5pG6xbQwHuKo0CbP1EJowx.zip "alt-J - Dancing In The Moonlight {It's Caught Me In Its Spotlight} - Recorded At Spotify Studios NYC.mp3" ;
	###################################


	print('beginning of zipPlaylist() flask_app.py')
	statusObject = Status()
	zip_filename = '{}.zip'.format( playlist_id )
	#zip_filename = Globals.DOWNLOAD_PATH + '/' + playlist_filename
	print('flask_app.py zipPlaylist(): file_paths => ')
	print(file_paths)

	cmd = 'cd {}; zip -m {} "{}" ;'.format(Globals.DOWNLOAD_PATH, zip_filename, '" "'.join(file_paths))
	try:
		print 'Zipping playlist tracks...'
		print cmd
		cmd_req = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)

	except Exception as inst:
	#	self.dump(statusObject)
		print '120 flask_app.py zipPlayist() error'
		print 'Exception: '
		print inst
		statusObject.setSuccess(False)
		statusObject.setDescription('Error zipping playlist...')

	ret_vals = dict()
	ret_vals['statusObject'] = statusObject
	ret_vals['playlist_filename'] = zip_filename

	return ret_vals


def downloadCallBack():
	print 'successfully downloaded the track!'




def getSpotifyPlaylistTracks(spotify_uri,token):
	""" Find matching youtube urls  """

	# get playlist tracks
	spotify_playlist_tracks = SPInterface.listPlaylistTracks(spotify_uri, token)
	spotify_playlist_tracks = SPInterface.parsePlaylistJson(spotify_playlist_tracks)
	pid = spotify_uri.split(':')[4]

	####################
	# SAVE TO DATABASE
	###################


	# download tracks
	playlist = []
	file_paths = []
	tracks = []
	for item in spotify_playlist_tracks:
		track = dict()
		# use youtube search api to find a video matching the args artist and song
		ytube_data_vals = YoutubeDataInterface.search_youtube_music_video(
							item['artist'],
							item['song'],
							item['duration_ms']
						)
		#print item['artist'],' - ',item['song'],ytube_data_vals['youtube_video']['video_id']


		if ytube_data_vals['success']:	# found a youtube video

			video_id = ytube_data_vals['youtube_video']['video_id']
			youtube_video_url = 'https://www.youtube.com/watch?v=' + video_id

			############
			# download #
			############
			# print 'Downloading track to server...'
			filename = YTDLInterface.formatSongFilename(item['artist'], item['song'])
			#filename = escapeCMD(filename)
			full_filename = filename + '.mp3'

			print 'full_filename: 166 flask_app.py === ' + full_filename
			'{} - {}.mp3'.format(item['artist'], item['song'])


			path_to_file = '{}/{}'.format( Globals.DOWNLOAD_PATH , filename )
			
			#print('186 flask.app')
			#print('escapeCMD(full_filename) => ')
	#		print(escapeCMD(full_filename))
		#	print('path_to_file =>')
		#	print(path_to_file)

			#file_paths.append(escapeCMD(full_filename))
			file_paths.append(full_filename)
			download_ret_vals = YTDLInterface.download(youtube_video_url, filename=filename, pid=pid,artist=item['artist'],name=item['song'])
			fid = download_ret_vals['fid']  	# get the id of the downloaded track
		#	print('196 getSpotifyPlaylistTracks() download_ret_vals[status]')
		#	print(download_ret_vals['status'])
			statusObject = download_ret_vals['status']


			if statusObject['success'] is False:
				print 'Exception: YoutubeDL Failed on ' + item['artist'] + ' - ' + item['song']
				track['artist'] = 'Failed!'
				track['song'] = statusObject['description']
			else:
				############
				# edit id3 #
				############
				print 'Editing ID3 Tag...'
				ID3Interface.editTag(item['artist'], item['song'], full_filename)
				#print 'successfully got track!'

			print '-----------------------------------------------------------------------'

		else:	# didn't find a youtube video


			#print ytube_data_vals['error_des']
			item['artist'] = 'Failed!'
			item['song'] = ytube_data_vals['error_des']

			print ytube_data_vals['error_des']
			print '-----------------------------------------------------------------------'

			statusObject.setSuccess(False)
			statusObject.setDescription(ytube_data_vals['error_des'])


		tracks.append({
				'artist': item['artist'],
				'song': item['song'],
				'duration_ms': item['duration_ms'],
				'fid': int(time.time()),
				'filename': filename,
				'url': youtube_video_url,
				'pid': pid
			})

	print('229 flask_app.py file_paths:')
	print(file_paths)	
	#################################
	# zip the files in the playlist #
	#################################
	zip_rtn_vals = zipPlaylist(file_paths, pid)
	statusObject = zip_rtn_vals['statusObject']
	playlist_filename = zip_rtn_vals['playlist_filename']

	print('248 flask_app statusObject')
	print(statusObject)
	

	return {
		'filename' : playlist_filename,
		'pid' : pid,
		'statusObject' : statusObject,
		'tracks': tracks

	}




def songDownloadPipeline(track):
    pid = track['pid']
   # print('track["fid"] => ' + track['fid'])
#    print('track["song"] => ' + track['song'])
    fid = track['fid']
    url = track['url']
    artist = track['artist']
    song = track['song']
    duration_ms = track['duration_ms']
    filename = track['filename']

    print('260: flask_app.py before YTDLInterface.download()')
    req_vals = YTDLInterface.download(URL=url, filename=filename, pid=pid, fid=fid)
    print('260: flask_app.py after YTDLInterface.download()')
    statusObject = req_vals['status']

    print('filename : '+ filename)
    print('statusObject => ')
    print(statusObject['description'])
#    if filename is None or filename is '':
    print('280 flask_app.oy songDownloadPipline : "if true" set')   
    if True:
	print('279')
        filename = req_vals['filename']
	print('281')


	if statusObject['success'] is False:
		print 'Exception: YoutubeDL Failed on ' + artist + ' - ' + song
		artist = 'Failed!'
		song = statusObject['description']
	else:
		print('289')
		# if (artist is None) and (song is None):
		# 	print 'Editing ID3 Tag...'
		# 	filename = req_vals['filename']
		# 	req_vals = YTDInterface.getArtistAndSong(req_vals['filename'])
		# 	artist = req_vals['artist']
		# 	song = req_vals['song']

		full_filename = filename + '.mp3'
		print('294 flask_app.py right before  ID3Interface.editTag()')
		print('!!!!!COMMENTING OUT ID3.EDITTAG!!!!!' )
		#ID3Interface.editTag(artist, song, full_filename)
	

	###################################################################
	# LOOK HERE STUPID. WE NEED TO JSONIFY THE RETURN DICT THIS BITCH #
	###################################################################
	return {
		'artist': artist,
		'song': song,
		'filename': filename,
		'duration_ms': duration_ms,
		'fid': fid,
		'pid': pid,
		'url': url

	}

  

# SPI = SpotifyInterface()
# YT = YoutubeInterface()

# AUTHENTICATION_REDIRECT_URL = 'http://localhost:80/spotify/authenticate'


# @app.route('/success')
# def success():
# 	return render_template('data.html')

# @app.route('/spotify/playlist')
# def playlist():
# 	sptfy_uri = request.args.get('sptfy_uri')
# 	playlist_tracks_complex = SPI.listPlaylistTracks(sptfy_uri)
# 	playlist_tracks = []

# 	for item in playlist_tracks_complex['items']:
# 		track = {}
# 		track['name'] = item['track']['name']
# 		track['artist'] = ''.join(artist['name'] for artist in item['track']['artists'])
# 		track['duration_ms'] = item['track']['duration_ms']



# 		# don't use name 'youtube' client side
# 		# alias dogs
# 		youtube_res = YT.search_youtube_music_video(
# 			artist=track['artist'],
# 			name=track['name'],
# 			duration_ms=track['duration_ms']
# 		)

# 		if youtube_res['success']:
# 			track['youtube'] = youtube_res['youtube_video']
# 		else:
# 			return redirect(url_for('error'), error=youtube_res['error_des'])

# 		print '============= Track ============= '
# 		print track
# 		print '================================= '

# 		playlist_tracks.append(track)



# 	return render_template('playlist.html', playlist=playlist_tracks)


############################################################################
#					########################################################
#		ROUTES		########################################################
#					########################################################
############################################################################


@app.route('/public/<path:path>/<filename>', methods=['GET'])
def serve_static(path, filename):
    root_dir = Globals.ROOT_DIR

    static_file_path = os.path.join(root_dir,'client','static', path)


    print('serving static =>' + static_file_path)
	#print 'Serving static file from ', static_file_path
	#print 'filename ', filename

    return send_from_directory(static_file_path, filename)




@app.route("/", methods=["GET"])
def index():
	authentication_redirect_url = request.url + 'spotify'

	#SPInterface.getAuthUrl('http://localhost:3000/'
	return render_template('base.html')






@app.route("/spotify/authorize", methods=["GET"])
def spotifyAuthorize():

	spotify_auth_url = None
	access_token = None
	spotify_playlist_tracks = None
	statusObject = Status()
	redirect_url = 'http://' + request.headers['Host']  + '/spotify/authorize'

	auth_stage =  'request_access' if request.args.get('spotify_uri') else 'token'

	# request access to user's spotify info
	if auth_stage == 'request_access':
		print 'Authorization Step 1: Requesting access to users spotify...'
		spotify_uri = request.args.get('spotify_uri')
		spotify_auth_url = SPInterface.getAuthUrl(redirect_url, spotify_uri)


		return jsonify({'spotify_auth_url':spotify_auth_url})

	elif auth_stage == 'token':
		print 'Authorization Step 2: Getting access tokens...'
		code = request.args.get('code')
		spotify_uri = request.args.get('state')

		# request token
		token = SPInterface.requestToken(code, redirect_url)



		print "================================================================================================="
		#print json.dumps(playlist)

		#return jsonify(playlist)

		#return redirect(url_for('download', playlist=json.dumps(playlist)))
		#return render_template('base.html', playlist = playlist)

		return redirect(url_for('spotify', access_token=token['access_token'], spotify_uri=spotify_uri) )


	statusObject.setSuccess(False)
	statusObject.setDescription('Issue authorizing spotify user...')
	return statusObject



@app.route("/spotify", methods=["GET"])
def spotify():
	access_token = request.args.get('access_token')
	spotify_uri = request.args.get('spotify_uri')

	print('spotify_uri ' + spotify_uri)
	pid = spotify_uri.split(':')[4]
	requestURL = '/download/grab/' + pid  + '/zip'

 	return render_template('base.html', downloading=True, grab_track_url=requestURL, access_token=access_token, spotify_uri=spotify_uri)




@app.route("/download", methods=["POST"])
def download():
	req_data = request.get_json()
	ret_vals = dict()
	ret_vals['tracks'] = []
	ret_vals['status'] = None
	url = req_data['url']
	fid = ''

	isSpotifyPlaylist = (req_data['download_type'] == 'spotify')
	isYoutubePlaylist = ('playlist?list=' in req_data['url'])

	if isSpotifyPlaylist:
		pid = url.split(':')[4]
		req_vals = getSpotifyPlaylistTracks(
												req_data['url'],
												req_data['token']
											)

		status = req_vals['statusObject'].toDict()
		tracks = req_vals['tracks']
		PlaylistModelInst.addPlaylist(pid, url)
		grab_track_url = None					# this will be set in /spotify request

	elif isYoutubePlaylist:
		pid = url.split('=')[1]
		req_vals = YTDLInterface.getYoutubePlaylistTracks(pid)		# get video id of every video in playlist
		tracks = req_vals['tracks']
		status = req_vals['statusObject'].toDict()
		PlaylistModel.addPlaylist(pid, url)
		grab_track_url = '/download/grab/' + pid  + '/zip'

	######## Single Track #########################
	else:
		pid = None
		fid = int(time.time())
		tracks = []
		tracks.append({
			'artist': '',
			'song': '',
			'duration_ms': '',
			'fid': fid,
			'pid': '',
			'url': url,
			'filename': ''

		})
		status = {
			'description' : '',
			'success': True
		}
		grab_track_url = '/download/grab/' + str(fid)  + '/mp3'

	print('line 493 flask_app.py')
	for key in tracks:
	    print('key => ')
	    print(key)



	#############################################
	# Download, Edit ID3 Tag, Save to DATABASE  #
	#############################################
	ret_vals['tracks'].append(
		map(songDownloadPipeline,tracks)
	)



	ret_vals['status'] = status
	ret_vals['grab_track_url'] = grab_track_url
	print('before')
	print(ret_vals)
	return jsonify(ret_vals)



################
#	work on this:
#	/download/grab/<fid>/<ext>
#
#
#
#
#
#
#################


@app.route("/download/grab/<data_id>/<ext>", methods=["GET"])
def returnTracks(data_id, ext):

	data_id = data_id + '.' + ext

	mimetype =  'application/zip, application/octet-stream' if ext=='zip' else 'audio/mpeg'

	print 'MIME TYPE ========='
	print mimetype

	print 'Globals.DOWNLOAD_PATH => ' + Globals.DOWNLOAD_PATH

	return send_from_directory(Globals.DOWNLOAD_PATH,
								data_id,
								as_attachment=True,
								attachment_filename=data_id,
								mimetype=mimetype
							)



@app.route("/music/search", methods=["POST"])
def search():
	URL = request.form['url']
	artist = request.form['artist']
	song = request.form['song']
	option_type = request.form['option_type']


	ValidURL = (
			(YTDLInterface.URL_IDENTIFIERS['youtube-playlist'] in URL) or
			(YTDLInterface.URL_IDENTIFIERS['spotify-playlist'] in URL) or
			(YTDLInterface.URL_IDENTIFIERS['youtube-song'] in URL)
	)


	if ValidURL:

		tracks = None

		if option_type in ['search','youtube'] :		# youtube video/playlist or song/artist
			statusObject = YTDLInterface.parseRequest(URL, artist, song)

		elif option_type == 'spotify':	# spotify uri
			statusObject = Status()
			pass


		#statusObject = YTDLInterface.parseRequest(URL, artist, song)

	else:
		statusObject = Status()
		statusObject.setSuccess(False)
		statusObject.setDescription('URL is not valid!')

	ret_vals = dict()
	ret_vals['status'] = statusObject.toDict()


	return jsonify(ret_vals)




# @app.route('/getTrack', methods=['GET'])
# def getTrack():
#     artist = request.args.get('artist')
#     track_name = request.args.get('track_name')
#     filename = getTrackName(artist, track_name)
#     attachment_fn = ''


#     if "extTrack" in filename:
#         attachment_fn = filename[0:len(filename)-14] + '.mp3'
#     else:
#         attachment_fn = filename

#     print('Getting Track ' + attachment_fn + '.'+app.config['DEST_DIR'] +'.')
#     return send_from_directory(app.config['DEST_DIR'],
#                               filename,
#                               as_attachment=True,
#                               attachment_filename=attachment_fn,
#                               mimetype='audio/mpeg'
#                               )


# @app.route("/error")
# def error(status):
# 	return render_template('error.html', status=status)


if __name__ == "__main__":
    app.run(
    		host = '127.0.0.1',
    		port = 3000
    	)

