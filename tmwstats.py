import datetime
from flask import Flask
import os
import pygal
import re
import threading
import time
import urllib2

import db_init

normalUsers = []
GMs = []

def create_app():
	app = Flask(__name__)
	return app

app = create_app()

@app.route('/ggraph')
def getgraph():
	playerNums = []
	ct = time.time()
	cur = db_init.db["scans"].find({"time": {"$gt": ct-86499}}).sort([("time", -1)]).limit(96)
	ltime = cur[0]["time"]
	ftime = cur[cur.count(True) - 1]["time"]
	numScans = int((ltime-ftime)/900) + 1
	ftime = int(ftime)
	for r in cur:
		playerNums.append(r["allplayers"])
	playerNums.reverse()
	
	pRange = max(playerNums) - min(playerNums)
	
	graphConfig = pygal.Config(
		style = pygal.style.Style(
			background = "#f7f7f7",
			plot_background = "transparent",
			foreground = "#777",
			foreground_light = "#222",
			foreground_dark = "#ddd",
			opacity = "0",
			opacity_hover = "0",
			colors = ("#b33636", "#b33636")
		),
		x_labels_major_count = 5,
		show_minor_x_labels = False,
		truncate_label = 20,
		title = "Number of players (last day)",
		interpolate = "cubic",
		range = (min(playerNums) - pRange/4, max(playerNums) + pRange/4),
		show_legend = False,
		width = 780,
		height = 450,
		explicit_size = True,
		fill = False,
		pretty_print = True,
		margin = 50,
		show_y_guides = True,
		dots_size = 2.0
	)
	
	graphConfig.css.append("graphs.css")
	
	chart = pygal.Line(config = graphConfig)
	chart.x_labels =  [datetime.datetime.fromtimestamp(x).strftime('%Y/%m/%d %H:%M') for x in range(ftime, numScans * 900 + ftime, 900)]
	chart.add("Players", playerNums)
	
	
	return chart.render()
	

@app.route("/")
def main():
	return "<object type=\"image/svg+xml\" data=\"/ggraph\"></object>"