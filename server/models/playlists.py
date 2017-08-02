
from flask_app import app
from flaskext.mysql import MySQL




class PlaylistModel(object):


	#############################
	# connect with MYSQL        #
	#############################
	def __init__(self):
		mysql = MySQL()
		mysql.init_app(app)
		self.conn = mysql.connect()
		self.cursor = self.conn.cursor()

	def addPlaylist(self, pid, url):
	   # print('addPlaylist()')
	    #print('pid => ' + pid)
	   # print('url => ' + url)
	    query = 'INSERT INTO playlists (id,url) VALUES ({},{});'.format(pid,url)
	    #.format(pid, url)
	    return query
        #self.cursor.execute(query)
        #data = self.cursor.fetch()
        #print('MYSQL =======> ' + data)
        #self.conn.close()


	def getPlaylist(self, pid):
		query = 'SELECT * FROM playlists WHERE pid={};'.format(pid)
		self.cursor.execute(query)
		data = self.cursor.fetch()

		print 'MYSQL =======> ', data

		self.conn.close()

		return data

# 	def addPlaylist(self, pid, url):
# 	    print('addPlaylist()')
# 	    print('pid => ' + pid)
# 	    print('url => ' + url)
#         query = 'INSERT INTO playlists (id,url) VALUES ({},{});'.format(pid, url)
#         self.cursor.execute(query)
#         data = self.cursor.fetch()
#         print('MYSQL =======> ' + data)
#         self.conn.close()
#         return data








