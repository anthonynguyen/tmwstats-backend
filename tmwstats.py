import os
from flask import Flask
import threading
import time

threadTime = ""

def create_app():
	app = Flask(__name__)
	def writeTime():
		global threadTime
		threading.Timer(60.00, writeTime).start()
		threadTime = str(time.time())
	writeTime()
	return app

app = create_app()

@app.route('/')
def hello():
	return 'Hello World!'

@app.route("/times")
def times():
	return threadTime
