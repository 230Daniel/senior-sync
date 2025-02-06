import json
from datetime import datetime

with open ("Output.json","r") as file:
    records=json.load(file)

for sensor_type in ["HKQuantityTypeIdentifierOxygenSaturation",
                    "HKQuantityTypeIdentifierRespiratoryRate",
                    "HKQuantityTypeIdentifierHeartRate",
                    "HKQuantityTypeIdentifierRestingHeartRate",
                    ]:
    datapoints=[]

    for record in records:
        if record["startDate"] > "2015" and record["type"] == sensor_type:
            datapoint={
                "value":float(record["value"]), 
                "timestamp":datetime.strptime(record["startDate"],"%Y-%m-%d %H:%M:%S %z").isoformat()
            }
            datapoints.append(datapoint)

    with open(f"{sensor_type}.json","w") as file:
        json.dump(datapoints,file, indent=4)



   
