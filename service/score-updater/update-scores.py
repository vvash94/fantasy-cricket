import requests
import pymongo
from pymongo import MongoClient
import time
import sys
import json

current_time = int(time.time())

client = MongoClient('mongo', 27017)

api_key = sys.argv[1]

db = client['ipl_db']

matches = db['matches']
match_data = db ['match_data']

for match in matches.find({"match_status": {"$ne": "Finished"}}):
  if match['match_status'] == "Not Started":
    if current_time < int(match['start']):
      print("Match not started")
    else:
      request_string = 'http://cricapi.com/api/fantasySummary?apikey='+ api_key + '&unique_id=' + match['unique_id']
      request = requests.get(request_string)
      summary = request.json()                                                      
      summary['unique_id'] = match['unique_id']

      match_data.update_one({'unique_id': match['unique_id']},{'$set': summary},upsert = True)
      matches.update_one({'unique_id': match['unique_id']},{'$set':{'match_status': 'Started'}})

  elif match['match_status'] == "Started":
    request_string = 'http://cricapi.com/api/fantasySummary?apikey='+ api_key + '&unique_id=' + match['unique_id']
    request = requests.get(request_string)
    summary = request.json()                                                        
    summary['unique_id'] = match['unique_id']                                       

    match_data.update_one({'unique_id': match['unique_id']},{'$set': summary},upsert = True)

    if summary['data']['man-of-the-match'] == "":
      print("match in progress")
    else:
      matches.update_one({'unique_id': match['unique_id']},{'$set':{'match_status': 'Finished'}})
