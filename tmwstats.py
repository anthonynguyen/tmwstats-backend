import os
from flask import Flask
import re
import threading
import urllib2

normalUsers = []
GMs = []

def create_app():
	app = Flask(__name__)
	
	def writeTime():
		global normalUsers
		global GMs
		
		threading.Timer(60.00, writeTime).start()
		
		try:
			req = urllib2.urlopen("http://server.themanaworld.org")
			rawHTML = req.read()
			
			allUsers = re.findall(r'\<td\>(.+?)\</td\>', rawHTML)
			numUsers = len(allUsers)
			GMs = []
			normalUsers = []
			
			for user in allUsers:
				m = re.match(r'\<b\>(.+?)\<\/b\> \(GM\)', user)
				if m is not None:
					GMs.append(m.group(1))
				else:
					normalUsers.append(user)
		except:
			pass
	
	writeTime()
	return app

app = create_app()

@app.route('/')
def main():
	global GMs
	global normalUsers
	return "GMs:<br /> <b>{0}</b> <br /><br /><br />Players:<br />{1}".format("<br />".join(GMs), "<br />".join(normalUsers))
