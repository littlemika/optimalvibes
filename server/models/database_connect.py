import sys
sys.path.append('/var/www/html/optimalvibes/')
from globals import Globals

import mysql.connector as mariadb


db_conn = mariadb.connect(user=Globals.DB['username'], password=Globals.DB['password'], database=Globals.DB['dbname'])
CURSOR  = db_conn.cursor()

#fid=123123
#filename='song.mp3'
#pid=123
#query = 'INSERT INTO `tracks` (`id`,`filename`,`playlistID`) VALUES ("{}","{}","{}");'.format(fid, filename, pid)
#CURSOR.execute("""INSERT INTO tracks (id,filename,playlistID) VALUES(%s,%s,%s)""", (fid,filename,pid))
#CURSOR.execute(query)
#db_conn.commit()
#result = CURSOR.fetchone()
#print(result)


CURSOR.execute('SELECT * FROM tracks')
print(CURSOR.fetchone())
#for name,artist in CURSOR:
#
#	print('DB ENTRY')
#	print(artist + ' - ' + name)
	
	
