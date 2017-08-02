#!/var/www/html/optimalvibes/bin python

from flask import Flask
from globals import Globals

app = Flask(__name__, 
			template_folder=Globals.TEMPLATE_PATH,
			static_url_path=Globals.STATIC_PATH,
			static_folder=Globals.STATIC_FOLDER
			)
app.config['DEBUG'] = True



#############################
# connect with MYSQL        #
#############################
app.config['MYSQL_DATABASE_USER'] = Globals.DB['username']
app.config['MYSQL_DATABASE_PASSWORD'] = Globals.DB['password']
app.config['MYSQL_DATABASE_DB'] = Globals.DB['dbname']
app.config['MYSQL_DATABASE_HOST'] = Globals.DB['host']
