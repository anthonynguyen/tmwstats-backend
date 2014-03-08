import pymongo
import os

client = pymongo.MongoClient(os.environ["MONGOLAB_URI"])
db = client.get_default_database()
