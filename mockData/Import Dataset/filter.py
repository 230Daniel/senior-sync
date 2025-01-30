import json

with open ("Output.json","r") as file:
    records=json.load(file)

print("\n".join(set([record["type"] for record in records])))

datapoints=[]

for record in records:
   if record["startDate"] > "2024" and record["type"] == "HKQuantityTypeIdentifierOxygenSaturation":
       datapoint={
           "value":record["value"], 
           "timestamp":record["startDate"]
       }
       datapoints.append(datapoint)

with open("o2.json","w") as file:
    json.dump(datapoints,file, indent=4)

# HKQuantityTypeIdentifierWalkingHeartRateAverage
# HKQuantityTypeIdentifierHeartRate
# HKQuantityTypeIdentifierOxygenSaturation
# HKQuantityTypeIdentifierHeartRate
# HKQuantityTypeIdentifierRestingHeartRate
# HKQuantityTypeIdentifierRespiratoryRate
# HKQuantityTypeIdentifierVO2Max