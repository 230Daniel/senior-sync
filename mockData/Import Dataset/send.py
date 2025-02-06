import json
import requests

with open ("HKQuantityTypeIdentifierOxygenSaturation.json","r") as file:
    datapoints=json.load(file)
response=requests.post("https://utili.xyz:8443/api/metrics/o2/mass",json=datapoints)
print(response.text)

with open ("HKQuantityTypeIdentifierHeartRate.json","r") as file:
    datapoints=json.load(file)
response=requests.post("https://utili.xyz:8443/api/metrics/HKQuantityTypeIdentifierHeartRate/mass",json=datapoints)
print(response.text)

with open ("HKQuantityTypeIdentifierRespiratoryRate.json","r") as file:
    datapoints=json.load(file)
response=requests.post("https://utili.xyz:8443/api/metrics/HKQuantityTypeIdentifierRespiratoryRate/mass",json=datapoints)
print(response.text)

with open ("HKQuantityTypeIdentifierRestingHeartRate.json","r") as file:
    datapoints=json.load(file)
response=requests.post("https://utili.xyz:8443/api/metrics/HKQuantityTypeIdentifierRestingHeartRate/mass",json=datapoints)
print(response.text)