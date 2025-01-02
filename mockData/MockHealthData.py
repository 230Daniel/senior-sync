import random
import time
import keyboard
import requests

class HealthData:
    def __init__(self):
        pass
        
    def heart_rate():
        """Generate a random heart rate value between 60 and 100 bpm."""
        return random.randint(60, 100)
    
    def heart_attack():
        """Generate a random heart rate value between 150 and 200 bpm."""
        return random.randint(150, 200)
    
    def flat_line():
        """Generate a random heart rate value between 0 and 0 bpm."""
        return 0

    # def O2_levels():
    #     """Generate a random heart rate value between 60 and 100 levels."""
    #     return random.randint(60, 100)
    
def main():
    print("\nMock Heart Rate Monitor\n")
    mode = "normal"
    try:
        while True:
            if keyboard.is_pressed("n"):
                mode = "normal"
                print("\nSwitched to NORMAL heart rate mode.", end="\n")
                time.sleep(2)  # Prevent multiple immediate detections

            elif keyboard.is_pressed("h"):
                mode = "high"
                print("\nSwitched to HIGH heart rate mode.", end="\n")
                time.sleep(2)

            if mode == "normal":
                heart_rate = HealthData.heart_rate()
            if mode == "high":
                heart_rate = HealthData.heart_attack()
            elif mode == "death":
                heart_rate = HealthData.flat_line()

            response = requests.post("http://localhost:8000/metrics/heart_rate/now", json=heart_rate)
            response.raise_for_status()
            print(f"Current Heart Rate: {heart_rate} bpm", end="\r")
            time.sleep(2)  # Wait for 2 second before refreshing
    except KeyboardInterrupt:
        print("\nHeart rate monitoring stopped.")

if __name__ == "__main__":
        main()