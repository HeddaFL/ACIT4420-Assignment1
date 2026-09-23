'''
Profile fields 
| Field | Description | Unit |
|---|---|---|
| `participant_id` | Simulated participant identifier | none |
| `baseline_heart_rate` | Personal resting reference | beats/minute |
| `baseline_skin_response` | Personal reference skin response | simulated units |
| `baseline_temperature` | Personal skin-temperature reference | degrees Celsius |

'''

class Participant:
    # Represent a participant and their personal baseline measurements.

    def __init__(
        self, 
        participant_id, 
        baseline_heart_rate,
        baseline_skin_response,
        baseline_temperature):

        if not isinstance(participant_id, str) or not participant_id.strip():
            raise ValueError("participant_id must be a non-empty string")

        self.__participant_id = participant_id
        self.__baseline_heart_rate = baseline_heart_rate
        self.__baseline_skin_response = baseline_skin_response
        self.__baseline_temperature = baseline_temperature

    @property
    def participant_id(self):
        # return the particioant identifier
        return self.__participant_id

    @property
    def baseline_heart_rate(self):
        # return the baseline heart rate
        return self.__baseline_heart_rate

    @property
    def baseline_skin_response(self):
        # return the baseline skin response
        return self.__baseline_skin_response

    @property
    def baseline_temperature(self):
        # return the baseline temperature
        return self.__baseline_temperature

    @classmethod
    def from_profile(cls, profile):
        # Create a Participant from a profile dictionary.
        # Convert generated dictionary data into a Participant object.

        return cls(
            participant_id=profile["participant_id"],
            baseline_heart_rate=profile["baseline_heart_rate"],
            baseline_skin_response=profile["baseline_skin_response"],
            baseline_temperature=profile["baseline_temperature"]
        )

    def __str__(self):
        return (f"Participant: ({self.participant_id}, "
                f"Heart Rate = {self.baseline_heart_rate}, "
                f"Skin Response = {self.baseline_skin_response}, "
                f"Temperature = {self.baseline_temperature})")

    def __eq__(self, other):
        if not isinstance(other, Participant):
            return NotImplemented
        return (
            self.__participant_id == other.__participant_id)
    