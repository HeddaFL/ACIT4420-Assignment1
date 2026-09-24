import unittest # from Python lib
from Observation import Observation
from Analysis import ( 
    classify_intensity, 
    detect_recovery, 
    generate_session_summary
)
from sample_data import build_session_from_scenario

# This class will test different observations that are invalid (except one valid control).
# I have manually added the numbers to ensure that the observations will be invaild for different reasons. 
class TestValidation(unittest.TestCase): 

    def test_valid_observation_is_usable(self): # This one is a valid control to ensure that it also tests true.
        obs = Observation(0, 90, 1.8, 32.5, 0.4, 0.95)
        self.assertTrue(obs.is_usable)

    def test_missing_value_is_rejected(self):
        obs = Observation(0, None, 1.8, 32.5, 0.4, 0.95)
        self.assertFalse(obs.is_valid)

    def test_impossible_value_is_rejected(self):
        obs = Observation(0, 999, 1.8, 32.5, 0.4, 0.95)
        self.assertFalse(obs.is_valid)

    def test_low_signal_quality_is_excluded_even_if_technically_valid(self):
        obs = Observation(0, 90, 1.8, 32.5, 0.4, 0.10)
        self.assertTrue(obs.is_valid)
        self.assertFalse(obs.is_usable)

# This class will test the different scenarios with a seed of 1. 
# All of the scenarios are representet to ensure that they are all testet. 
# It draws data from data_generator.py. 
class TestFiveRequiredScenarios(unittest.TestCase):

    def test_resting(self):
        session = build_session_from_scenario("P001", "resting", seed=1, number_of_windows=12)
        self.assertEqual(classify_intensity(session), "resting")

    def test_moderate_activity(self):
        session = build_session_from_scenario("P001", "moderate_activity", seed=1, number_of_windows=12)
        self.assertEqual(classify_intensity(session), "moderate activity")

    def test_high_activity(self):
        session = build_session_from_scenario("P001", "high_activity", seed=1, number_of_windows=12)
        self.assertEqual(classify_intensity(session), "high activity")

    def test_recovery_is_detected(self):
        session = build_session_from_scenario("P001", "recovery", seed=1, number_of_windows=12)
        is_recovering, _ = detect_recovery(session)
        self.assertTrue(is_recovering)

    def test_poor_quality_data_gets_rejected(self):
        session = build_session_from_scenario("P001", "poor_quality", seed=1, number_of_windows=12)
        self.assertGreater(session.rejected_count(), 0)

# This class will test the report to ensure that it 
# contains the key ("classification", "recovery_detected", "usable_observations", "heart_rate") for each report.
class TestStructuredReport(unittest.TestCase):

    def test_report_has_key_fields(self):
        session = build_session_from_scenario("P001", "moderate_activity", seed=1, number_of_windows=12)
        report = generate_session_summary(session)
        for key in ("classification", "recovery_detected", "usable_observations", "heart_rate"):
            self.assertIn(key, report)

if __name__ == "__main__":
    unittest.main()