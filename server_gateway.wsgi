#!/var/www/html/optimalvibes/bin python

import sys
from globals import Globals
sys.path.append(Globals.ROOT_DIR)

import flask_app
from app import app as application
