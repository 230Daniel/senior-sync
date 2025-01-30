from datetime import datetime
from health_data import HealthData
import time
import keyboard
import requests

def main():
    print("\nStarting Health Simulator\n")
    mode = "normal"
    api_post_data_endpoint = ""
    api_post_sensor_endpoint = "http://localhost:8000/api/sensors"
    id = ""
    friendly_name = ""
    unit = ""
    value_type = int

    while True:
        sensor = input("Type 'O2' for Blood Oxygen level sensor or type 'heart' for Heart Rate monitor\n")
        if sensor == 'O2':
            print("\nMock Blood Oxygen level sensor\n")
            break
        elif sensor == 'heart':
            print("\nMock Heart Rate Monitor\n")
            break
        else:
            print("Invalid input. Try again.")

    match sensor:
        case 'O2':
            api_post_data_endpoint = "http://localhost:8000/api/metrics/o2_level"
            id = "o2_level"
            friendly_name = "O2 Level"
            unit = "%"
            value_type = "int"

        case 'heart':
            api_post_data_endpoint = "http://localhost:8000/api/metrics/heart_rate"
            id = "heart_rate"
            friendly_name = "Heart Rate"
            unit = "bpm"
            value_type = "int"

    try:
        response = requests.post(api_post_sensor_endpoint, json={
  "_id": id,
  "friendly_name": friendly_name,
  "unit": unit,
  "value_type": value_type
})
        response.raise_for_status()
    except:
        pass

    try:
        while True:
            if keyboard.is_pressed("n"):
                mode = "normal"
                print("\nSwitched to NORMAL mode.", end="\n")
                time.sleep(2)  # Prevent multiple immediate detections

            if keyboard.is_pressed("d"):
                mode = "dangerous"
                print("\nSwitched to DANGEROUS mode.", end="\n")
                time.sleep(2)

            elif keyboard.is_pressed("x"):
                mode = "death"
                print("\nSwitched to DEAD mode.", end="\n")
                time.sleep(2)

            if mode == "normal":
                match sensor:
                    case 'O2':
                        value = HealthData.normal_O2_level()
                    case 'heart':
                        value = HealthData.normal_heart_rate()
            if mode == "dangerous":
                match sensor:
                    case 'O2':
                        value = HealthData.low_O2_level()
                    case 'heart':
                        value = HealthData.heart_attack()
            elif mode == "death":
                value = HealthData.flat_line()

            match sensor:
                case 'O2':
                    print(f"Current Blood Oxygen Level: {value} %", end="\r")
                case 'heart':
                    print(f"Current Heart Rate: {value} bpm", end="\r")

            response = requests.post(api_post_data_endpoint, json={
                "timestamp": datetime.now().isoformat(),
                "value": value
            })
            response.raise_for_status()
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nHeart rate monitoring stopped.")

if __name__ == "__main__":
        main()
