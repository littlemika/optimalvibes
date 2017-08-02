from apiclient.discovery import build
from apiclient.errors import HttpError
from status import Status
# pip install --ignore-installed six --upgrade google-api-python-client


class YoutubeInterface(object):

	#DEVELOPER_KEY = "AIzaSyDkgTID3lRal8nSHyQl-OEiuWnLSsHpgqE"
	DEVELOPER_KEY = 'AIzaSyDn-57_k6Hen0YRLkShbgFvKn11NgcBCS0'
	YOUTUBE_API_SERVICE_NAME = "youtube"
	YOUTUBE_API_VERSION = "v3"

	def __init__(self):
		self.youtube = None

	def authorize(self):
		"""
		Connect with api and build youtube service 
		"""

		print 'Authorizing...'

		if self.youtube:
			print 'Already authorized'
			return False

		self.youtube = build(self.YOUTUBE_API_SERVICE_NAME, 
						 self.YOUTUBE_API_VERSION,
  						 developerKey=self.DEVELOPER_KEY)



	#
	#
	#	returns boolean
	#		True if skip video (not a candidate)
	#
	def check_video_pruning(self, artist, name, title):
		"""
		check if video title contains a weed word
		?check if video duration equals the duration of the spotify track
		"""

		weeders = ['cover','live','vevo','remix']			# words that we want to ignore in our video search
		name_contains_weed_word = any(weed_word in name.lower() for weed_word in weeders) 
		artist_cointains_weed_word = any(weed_word in artist.lower() for weed_word in weeders)
		video_title_contains_weed_word = any(weed_word in title.lower() for weed_word in weeders)

		# ensure that the artist or track name does not actually include the weeders Ex. live house
		if video_title_contains_weed_word and (name_contains_weed_word is False and artist_cointains_weed_word is False):
			ret_val = True
		else:
			ret_val = False



		# check duration of song

		return ret_val



	#
	#
	#	=> Return Vals
	#			success : False if couldn't find matching track
	#			error_des : string, description of error
	#			youtube_video_best : {
	#									'video_id': val,
	#									'title': val
	#								 }
	#
	#
	#	https://developers.google.com/apis-explorer/#p/youtube/v3/youtube.search.list
	#
	def search_youtube_music_video(self, artist, name, duration_ms):
		""" 
		Search youtube for music video matching artist and name
		"""
		# return val : false until proven wrong
		success = False        # could not find matching youtube video
		error_des = "none"

		self.authorize()



		# build search params aka q
		#finders = ['vevo','lyrics']			# words that we want to see in our search
		try:
			search_response_j = self.youtube.search().list(
				videoCategoryId = 10,
				type = 'video',
				order = 'relevance',
				#q = '{} {} lyrics'.format(artist, name),
				q = artist + ' ' + name + ' lyrics',
				part = "snippet",
				maxResults = 5
			).execute()


			youtube_videos_j = search_response_j['items']

			if len(youtube_videos_j) == 0:	# NO results
				error_des = 'Sorry! Could not find track to download...'
				success = False
			else:				

				######################################################################################################
				# set default best video to the first relevant video
				# will be overwritten in next block of code if a better option is found
				# if self.check_video_pruning(artist, name, youtube_videos_j[0]['snippet']['title']) is False:
				######################################################################################################
				# youtube_video_best = {
				# 	'video_id': youtube_videos_j[0]['id']['videoId'],
				# 	'title': youtube_videos_j[0]['snippet']['title']
				# }


				# Let's see if we can find a better video then the default: 0
				for index,video in enumerate(youtube_videos_j):
					snippet = video['snippet']
					channel_title = snippet['channelTitle']
					title = snippet['title']

					# weed out covers,vevo, live videos
					# not yet implemented : weed out videos that are not of the same duration as the spotify track
					if self.check_video_pruning(artist, name, title):	# ensure that the artist or track name does not actually include the weeders Ex. live hous
						print '==========\nTESTING!!!!\n=========='
						print 'weeding out video: '
						print 'name: ', name
						print 'artist: ', artist
						print 'title: ', title

						continue	# skip video because it contains a weed word

					# select first video that is not pruned
					else:

						youtube_video_best = {
						 	'video_id': youtube_videos_j[index]['id']['videoId'],
						 	'title': youtube_videos_j[index]['snippet']['title']
						}

						break


					#####################################################################################
					# check if vevo channel
					# check if channel title owned by artist
					#####################################################################################
					# if 'vevo' in channel_title.lower() or artist in channel_title.lower():
					# 	print '==========\nVEVO Found!!!!\n=========='

					# 	youtube_video_best['video_id'] = video['id']['videoId']
					# 	youtube_video_best['title'] = title

					# 	break	# stop looking


				success = True

		except HttpError, e:
			error_des  = "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
			success = False
			print error_des


		return  {
					'success' : success,
					'error_des' : error_des,
					'youtube_video' : youtube_video_best
				}

	# guess the artist and song of track
	def getArtistAndSong(self, video_id, video_title):

		if '.mp3' in video_title:
			video_title = video_title[0:-4]



		if '-' in video_title:
			tokens = video_title.split('-')

			if len(tokens) >= 2:
				artist = tokens[0].strip()
				song = tokens[1].strip()
			else:
				artist = tokens[0]
				song = None

		else:
			artist = video_title
			song = None

		ret_vals = dict()
		ret_vals['artist'] = artist
		ret_vals['song'] = song

		return ret_vals



	def getYoutubePlaylistTracks(self, pid):
		statusObject = Status()

		try:
			res = self.youtube.playlistItems().list(
			    part="snippet",
			    playlistId=pid
		    ).execute()

			video_id = res.items['snippet']['resourceId']['videoId']
			video_title = res.items['snippet']['title']

			print 'getYoutubePlaylistTracks(self, pid) =================='
			print res.items

			url = 'https://www.youtube.com/playlist?list=' + video_id
	

			req_vals = getArtistAndSong(video_title)

			track = {
				'artist': req_vals['artist'],
				'song': req_vals['song'],
				'duration_ms': '',
				'fid': videoId,
				'filename': video_title,
				'url': url
			}


		except Exception as inst:
			statusObject.setDescription(inst)
			print inst





		# res = self.youtube.playlistItems().list(
		#     part="snippet",
		#     playlistId=pid,
		#     maxResults="50"
	 #    ).execute()


		#nextPageToken = res.get('nextPageToken')
		
		# while ('nextPageToken' in res):
		# 	nextPage = youtube.playlistItems().list(
		# 		part="snippet",
		# 		playlistId=pid,
		# 		maxResults="50",
		# 		pageToken=nextPageToken
		# 	).execute()
		
		# 	res['items'] = res['items'] + nextPage['items']

		# 	if 'nextPageToken' not in nextPage:
		# 		res.pop('nextPageToken', None)
		# 	else:
		# 		nextPageToken = nextPage['nextPageToken']

		ret_vals = dict()
		ret_vals['tracks'] = track
		ret_vals['status'] = statusObject

		return res.items











