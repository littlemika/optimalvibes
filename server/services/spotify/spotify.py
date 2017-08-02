import urllib
import requests
import base64
import json


class SpotifyInterface(object):

	BASE_API_URL = 'https://api.spotify.com'
	AUTHORIZE_URL = 'https://accounts.spotify.com/authorize?'
	TOKEN_BASE_URL = 'https://accounts.spotify.com/api/token'
	END_POINTS = {
		'playlist_tracks' : '/v1/users/{user_id}/playlists/{playlist_id}/tracks'
	}



	#	*Authorization Step 1:
	#	------------------------------------------------------
	#	=> Params:
	#			redirect_uri : after user accepts and logins to their spotify account they will be redirected to this url
	#
	# 	=> Return Val:
	#			auth_url : url that will be sent to user so they can login to their account and accept
	#
	def getAuthUrl(self, redirect_url, spotify_uri):
		"""
			Get user's authorization to access their spotify info
		"""
		SCOPES = 'playlist-read-private user-read-private user-library-read playlist-read-collaborative'

		print('getAuthUrl(): redirect_uri => ' + redirect_url)

		query_params = urllib.urlencode({
				'scope':SCOPES,
				'client_id': '3edd3fa947c64ddb843a0380e07e10e7',		# client id associated with this app
				'response_type': 'code',
				'redirect_uri':  redirect_url,
				'show_dialog': True,
				'state' : spotify_uri
			})

		auth_url = SpotifyInterface.AUTHORIZE_URL + query_params
		print('auth_url=> ' + auth_url)

		return auth_url




	#	*Authorization Step 2:
	#	------------------------------------------------------
	#	=> Params:
	#			code 			: 	An authorization code that can be exchanged for an access token.
	#			redirect_uri 	: 	This parameter is used for validation only (there is no actual redirection).
	#						   		The value of this parameter must exactly match the value of redirect_uri
	# 						   		supplied when requesting the authorization code. (aka redirect_uri passed to get_auth_url )
	#
	# 	=> Return Val:
	#			token {'access_token','token_type','refresh_token'}
	def requestToken(self, code, redirect_uri):
		# request access token
		CLIENT_ID = '3edd3fa947c64ddb843a0380e07e10e7'
		CLIENT_SECRET = '81e5b59f982b4e139829b3fc4c2573b9'


		# print 'HERE IS THE redirect_uri ============'
		# print redirect_uri

		query_params = {
					'grant_type': 'authorization_code',
					'code': code,
					'redirect_uri':  redirect_uri
				}

		base64encoded = base64.b64encode("{}:{}".format(CLIENT_ID, CLIENT_SECRET))
		headers = {"Authorization": "Basic {}".format(base64encoded)}

		# POST REQUEST to retrieve token
		token_post_req = requests.post(SpotifyInterface.TOKEN_BASE_URL, data=query_params, headers=headers)

		if(int(token_post_req.status_code) >= 400):
			print(token_post_req.content)
			return False


		token_res_data_j = json.loads(token_post_req.text)
		token = {}
		token['access_token'] = token_res_data_j['access_token']
		token['token_type'] = token_res_data_j['token_type']
		token['refresh_token'] = token_res_data_j['refresh_token']

		return token



	#
	#
	#	Params
	#		spotifty_uri => spotify:user:1212962782:playlist:3jwoEN131CeQ1cly4APzv2
	#
	def listPlaylistTracks(self, sptfy_uri, access_token):
		"""
			Get List of Tracks on Playlist
		"""

		sptfy_uri_tokens = sptfy_uri.split(':')
		user_id = sptfy_uri_tokens[2]
		playlist_id = sptfy_uri_tokens[4]



		endpoint = SpotifyInterface.END_POINTS['playlist_tracks']
		endpoint = endpoint.replace('{user_id}', user_id)
		endpoint = endpoint.replace('{playlist_id}', playlist_id)
		playlist_api_url = SpotifyInterface.BASE_API_URL + endpoint


		req_hdrs =  {"Authorization" : "Bearer {}".format(access_token)}
		playlist_post_req = requests.get(playlist_api_url, headers = req_hdrs)

		if(int(playlist_post_req.status_code) >= 300):
			print(playlist_post_req.content)

		playlist_data_j = json.loads(playlist_post_req.text)
		return playlist_data_j



	def parsePlaylistJson(self, spotify_playlist_tracks):
		playlist_tracks_complex = spotify_playlist_tracks
		playlist_tracks = []

		for item in playlist_tracks_complex['items']:
			track = {}
			track['song'] = item['track']['name']
			track['artist'] = ' '.join(artist['name'] for artist in item['track']['artists'])
			track['duration_ms'] = item['track']['duration_ms']

			playlist_tracks.append(track)

		return playlist_tracks

