import json
import requests

with open ("HKQuantityTypeIdentifierOxygenSaturation.json","r") as file:
    datapoints=json.load(file)
response=requests.post("http://localhost:8000/metrics/o2/mass",json=datapoints)
print(response.text)

with open ("HKQuantityTypeIdentifierRespiratoryRate.json","r") as file:
    datapoints=json.load(file)
response=requests.post("http://localhost:8000/metrics/o2/mass",json=datapoints)
print(response.text)