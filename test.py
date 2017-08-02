#!/usr/bin/python2.7
import subprocess
import os

i = os.path.dirname(os.path.abspath(__file__))

print(i)

file_paths = [
	'alt-J - Dancing In The Moonlight (It\'s Caught Me In Its Spotlight) - Recorded At Spotify Studios NYC.mp3'
]
cmd = 'cd {}; zip -m {} {} ;'.format('/var/www/html/optimalvibes/server/downloads', 'daposdufi9wae.zip', ' '.join(file_paths))
print(cmd)
cmd_req = subprocess.check_output(cmd,stderr=subprocess.STDOUT, shell=True)
print(cmd_req)

       
       #         print 'Zipping playlist tracks...'
        #        print cmd

        #        cmd_req = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)

        #e#xcept Exception as inst:
        #       self.dump(statusObject)
         #       print '120 flask_app.py zipPlayist() error'
          #      print 'Exception: '
           #     print inst
#
