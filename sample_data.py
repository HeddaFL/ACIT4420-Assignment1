from option_a_fitness.data_generator import generate_fitness_data
from Participant import Participant
from Session import Session

SCENARIOS = ("resting", "moderate_activity", "high_activity", "recovery", "poor_quality")

def build_session_from_scenario(participant_id, scenario, seed=42, number_of_windows=12):
    profile, raw_observations = generate_fitness_data(
        participant_id=participant_id,
        scenario=scenario,
        seed=seed,
        number_of_windows=number_of_windows,
    )
    participant = Participant.from_profile(profile)
    session = Session.from_observations(
        session_id=f"{participant_id}-{scenario}",
        participant=participant,
        raw_observations=raw_observations,
    )
    return session


def build_all_scenarios(participant_id="P001", seed=42, number_of_windows=12):
    return {
        scenario: build_session_from_scenario(participant_id, scenario, seed=seed,
                                               number_of_windows=number_of_windows)
        for scenario in SCENARIOS
    }
