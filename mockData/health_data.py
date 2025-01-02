import random

class HealthData:
    def __init__(self):
        pass
        
    def normal_heart_rate():
        """Generate a random heart rate value between 60 and 100 bpm."""
        return random.randint(60, 100)
    
    def heart_attack():
        """Generate a random heart rate value between 150 and 200 bpm."""
        return random.randint(150, 200)
    
    def flat_line():
        """Generate a random heart rate value between 0 and 0 bpm."""
        return 0

    def normal_O2_level():
        """Generate a random heart rate value between 60 and 100 levels."""
        return random.randint(95, 100)
    
    def low_O2_level():
        return random.randint(80, 92)