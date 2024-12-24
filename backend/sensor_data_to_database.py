import pymongo
import pymongo.database
import datetime

database_client = pymongo.MongoClient("mongodb://localhost:27017/") #TODO change to an environment variable
db = database_client["data"]
col = db["heartrate"]

heart_rate_data = {"timestamp": "test", "bpm": "57"}

x = col.insert_one(heart_rate_data)

print(x)