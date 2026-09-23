from sample_data import build_all_scenarios
from Analysis import generate_session_summary, build_console_report

def main():
    # Build and print a report for each required scenario.
    sessions = build_all_scenarios(participant_id="P001", seed=42, number_of_windows=12)

    for scenario_name, session in sessions.items():
        print(f"\nScenario: {scenario_name} ")
        report = generate_session_summary(session)
        print(build_console_report(report))

if __name__ == "__main__":
    main()