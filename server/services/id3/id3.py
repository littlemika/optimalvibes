import eyed3

import sys
sys.path.append('/var/www/html/optimalvibes')
from globals import Globals

class ID3TagEditInterface:

	def editTag(self, artist, song, full_filename):
		song_path = '{}/{}'.format(Globals.DOWNLOAD_PATH, full_filename)
#		song_path = '\ '.join(song_path.split())
#		#song_path = song_path.replace(' ','\ ')
		#song_path = song_path.replace('\\','\')
	#	song_path = '"' + song_path + '"'

		print('Commenting out id3 tag stuff ID3TagEditInterface')
		print 'song path: ',song_path
#		audiofile = eyed3.load(song_path)
#		audiofile.initTag()
#		audiofile.tag.artist = artist.decode('utf-8')
#		audiofile.tag.title = song.decode('utf-8')


#		audiofile.tag.save()
