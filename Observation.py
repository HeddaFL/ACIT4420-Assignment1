'''
Observation fields from data_generator.py
| Field | Description | Expected range |
|---|---|---|
| `timestamp` | Ordered observation number | integer, 0 or greater |
| `heart_rate` | Measured heart rate | normally 35-205 bpm |
| `skin_response` | Simulated sensor value | normally 0 or greater |
| `temperature` | Simulated skin temperature | normally 25-42 C |
| `activity_level` | Normalized movement level | 0-1 |
| `signal_quality` | Measurement reliability indicator | 0-1 |

'''

from abc import ABC, abstractmethod

class SensorReading(ABC):
    # Abstract class that Observation can inherit from.

    def __init__(self, timestamp):
        self.timestamp = timestamp
        self._validation_errors = []

    @property
    def is_valid(self):
        return len(self._validation_errors) == 0

    # ensure that validate() will raise an error. 
    @abstractmethod
    def validate(self):
        raise NotImplementedError("ERROR: validate method not implemented.")


class Observation(SensorReading):
    # Measurement observation window. 

    def __init__(
            self, 
            timestamp,
            heart_rate,
            skin_response,
            temperature,
            activity_level,
            signal_quality,):

        super().__init__(timestamp)

        # not private attributes. 
        self.timestamp = timestamp
        self.heart_rate = heart_rate
        self.skin_response = skin_response
        self.temperature = temperature
        self.activity_level = activity_level
        self.signal_quality = signal_quality
        self.validate()

    # validate() checks if the fields are valid.
    def validate(self):
        self._validation_errors = []

        if not self.is_within_range(self.heart_rate, 35, 205):
            self._validation_errors.append("Heart rate out of range (35-205 bpm).")

        if not self.is_within_range(self.skin_response, 0, float('inf')):
            self._validation_errors.append("Skin response out of range (0 or greater).")

        if not self.is_within_range(self.temperature, 25, 42):
            self._validation_errors.append("Temperature out of range (25-42 C).")

        if not self.is_within_range(self.activity_level, 0, 1):
            self._validation_errors.append("Activity level out of range (0-1).")

        if not self.is_within_range(self.signal_quality, 0, 1):
            self._validation_errors.append("Signal quality out of range (0-1).")

    # If there is any None fields it will be rejected in the staticmethod.
    @staticmethod
    def is_within_range(value, min_value, max_value):
        if value is None:
            return False
        return min_value <= value <= max_value

    # ensure that usable observations is valid and within the signal_quality standard.
    @property
    def is_usable(self):
        return self.is_valid and self.signal_quality >= 0.5

    @classmethod
    def from_dict(cls, data):
        # Create an Observation from a dictionary. 
        
        return cls(
            data.get("timestamp"),
            data.get("heart_rate"),
            data.get("skin_response"),
            data.get("temperature"),
            data.get("activity_level"),
            data.get("signal_quality"),
        )