import os
from flask import Flask
import re
import threading
import time
import urllib2

import db_init

normalUsers = []
GMs = []

def create_app():
	app = Flask(__name__)
	
	def doScan():
		global normalUsers
		global GMs
		
		threading.Timer(900.00, doScan).start()
		
		curTime = time.time()
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
		
		scandata = {"allplayers": numUsers, "gms": len(GMs), "time": curTime}
		db_init.db["scans"].insert(scandata)

		for user in normalUsers:
			dbUser = db_init.db["normals"].find_one({"charname": user})
			if dbUser is None:
				db_init.db["normals"].insert({"charname": user, "sightings": 1, "last_seen": curTime})
			else:
				db_init.db["normals"].update({"charname": user}, {"$set": {"sightings": dbUser["sightings"] + 1, "time": curTime}})
			
		for gm in GMs:
			dbGM = db_init.db["gms"].find_one({"charname": gm})
			if dbGM is None:
				db_init.db["gms"].insert({"charname": gm, "sightings": 1, "last_seen": curTime})
			else:
				db_init.db["gms"].update({"charname": gm}, {"$set": {"sightings": dbGM["sightings"] + 1, "time": curTime}})
	
	threading.Timer(900.00, doScan).start()
	return app

app = create_app()

@app.route('/')
def main():
	global GMs
	global normalUsers
	return "GMs:<br /> <b>{0}</b> <br /><br /><br />Players:<br />{1}".format("<br />".join(GMs), "<br />".join(normalUsers))
