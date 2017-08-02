


from flaskext.mysql import MySQL
import peewee
from peewee import *
#import mysql.connector
import sys
import os

#cwd = os.getcwd()
#if '/home/trackfinity' in cwd:
#    sys.path.append('/home/trackfinity/mysite/')
#else:
#    sys.path.append('/Users/danielhui/Documents/apps/OptimalVibes/server')



sys.path.append('/var/www/html/optimalvibes')
from app import app
from globals import Globals


#from database_connect import CURSOR,db_conn

import mysql.connector as mariadb



class SongModel(object):


	#############################
	# connect with MYSQL        #
	#############################
	def __init__(self):
		self.db_conn = mariadb.connect(user=Globals.DB['username'], password=Globals.DB['password'], database=Globals.DB['dbname'])
		self.CURSOR  = self.db_conn.cursor()


		#mysql = MySQL()
		#mysql.init_app(app)
		#self.conn = mysql.connect()
		#CURSOR = self.conn.cursor()

		#print('MYSQL CONNECT:')
		#print(self.conn.cursor())
		#print(CURSOR)

#		CURSOR = db.cursor()
		   # cursor.execute("""
		   #    select 3 from your_table
		   # """)
		   # result = cursor.fetchall()
		   # print result


	def getSong(self, filename):
		query = 'SELECT * FROM tracks WHERE filename={};'.format(filename)
		self.CURSOR.execute(query)
		data = self.CURSOR.fetch()

		print('MYSQL =======> ' + data)

		#self.CURSOR.close()

		return data

	def addSong(self, fid, filename, pid=None,artist=None, name=None):

		if pid == '':
			pid = 'None'
	
	#	query = 'INSERT INTO `tracks` (`id`,`filename`,`playlistID`) VALUES ("{}","{}","{}");'.format(fid, filename, pid)
#

		self.CURSOR.execute("""INSERT INTO tracks (id,filename,playlistID,artist,name) VALUES(%s,%s,%s,%s,%s)""", (fid,filename,pid,artist,name))
		self.db_conn.commit()
		
		result = self.CURSOR.fetchone()
		print("Adding new track to tracks table...")
		#print(query)
		print(result)

		#self.CURSOR.close()

		return 1







# db = MySQLDatabase('jonhydb', user='john',passwd='megajonhy')

# class Book(peewee.Model):
#     author = peewee.CharField()
#     title = peewee.TextField()

#     class Meta:
#         database = db

# Book.create_table()
# book = Book(author="me", title='Peewee is cool')
# book.save()
# for book in Book.filter(author="me"):
#     print book.title
