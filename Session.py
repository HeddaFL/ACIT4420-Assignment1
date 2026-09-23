from Participant import Participant
from Observation import Observation

class Session:
    # Represent one session for one participant. 

    def __init__(self, session_id, participant):

        if not isinstance(participant, Participant):
            raise TypeError("participant must be a Participant object")
        if not isinstance(session_id, str) or not session_id.strip():
            raise ValueError("session_id must be a non-empty string")

        self.__session_id = session_id
        self.__participant = participant
        self.__observations = []

    def add_observation(self, observation):
        # Add an Observation object to the session. 

        if not isinstance(observation, Observation):
            raise TypeError("observation must be an Observation object")
        self.__observations.append(observation)

    @classmethod
    def from_observations(cls, session_id, participant, raw_observations):
        session = cls(session_id, participant)
        for raw in raw_observations:
            session.add_observation(Observation.from_dict(raw))
        return session
    
    @property 
    def session_id(self):
        return self.__session_id

    @property
    def participant(self):
        return self.__participant

    # ensure no one can modify the observations list directly, only through add_observation
    @property 
    def observations(self):
        return list(self.__observations)  # Return a copy to prevent external modification

    @property
    def usable_observations(self):
        return [obs for obs in self.__observations if obs.is_usable]

    @property
    def rejected_observations(self):
        return [obs for obs in self.__observations if not obs.is_usable] # list comprehensions

    def total_count(self):
        return len(self.__observations)

    def usable_count(self):
        return len(self.usable_observations)

    def rejected_count(self):
        return len(self.rejected_observations)

    def __len__(self):
        return len(self.__observations)

    def __str__(self):
        return (f"Session ID {self.__session_id} for {self.__participant.participant_id}"
                f" ({self.usable_count()}/{self.total_count()} usable observations)")

    
    
    