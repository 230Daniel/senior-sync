import json
import requests

with open ("o2.json","r") as file:
    datapoints=json.load(file)

response=requests.post