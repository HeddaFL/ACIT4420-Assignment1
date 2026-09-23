import statistics # pythonlib

def summarize_values(values):
    clean = [v for v in values if v is not None]
    if not clean:
        return {"average": None, "min": None, "max": None, "count": 0}
    return {
        "average": round(statistics.mean(clean), 2),
        "min": min(clean),
        "max": max(clean),
        "count": len(clean),
    }

def compare_baseline(value, baseline):
    if value is None or baseline is None:
        return None
    return round(value - baseline, 2)

def detect_recovery(session):
    usable = sorted(session.usable_observations, key=lambda obs: obs.timestamp) # lambda sort it in order of timestamp
    if len(usable) < 4:
        return False, "not enough usable observations to evaluate recovery"
    
    middle = len(usable) // 2
    first_half, second_half = usable[:middle], usable[middle:]

    hr_first = statistics.mean([obs.heart_rate for obs in first_half])
    hr_second = statistics.mean([obs.heart_rate for obs in second_half])
    activity_first = statistics.mean([obs.activity_level for obs in first_half])
    activity_second = statistics.mean([obs.activity_level for obs in second_half])

    heart_rate_declining = hr_second < hr_first - 3
    activity_declining = activity_second < activity_first - 0.05 

    if heart_rate_declining and activity_declining:
        explanation = (f"Heart rate fell from {hr_first:.1f} to {hr_second:.1f} bpm "
                       f"and activity fell from {activity_first:.2f} to {activity_second:.2f} "
                       "over the second half of the session")
        return True, explanation
    return False, "no significant decline in heart rate and activity toward the end of the session"

def classify_intensity(session):
    usable = session.usable_observations
    if len(usable) < 3:
        return "insufficient data"

    is_recovering, _ = detect_recovery(session)
    if is_recovering:
        return "recovering"

    avg_hr = statistics.mean(obs.heart_rate for obs in usable)
    avg_activity = statistics.mean(obs.activity_level for obs in usable)
    hr_deviation = compare_baseline(avg_hr, session.participant.baseline_heart_rate)

    if avg_activity < 0.25 and hr_deviation is not None and hr_deviation < 12:
        return "resting"
    if avg_activity < 0.68 and hr_deviation is not None and hr_deviation < 45:
        return "moderate activity"
    return "high activity"

def generate_session_summary(session):
    usable = session.usable_observations
    participant = session.participant

    heart_rates_summary = summarize_values([obs.heart_rate for obs in usable])
    skin_response_summary = summarize_values([obs.skin_response for obs in usable])
    temperature_summary = summarize_values([obs.temperature for obs in usable])
    activity_summary = summarize_values([obs.activity_level for obs in usable])

    is_recovering, recovery_explanation = detect_recovery(session)
    classification = classify_intensity(session)

    return {
        "participant_id": participant.participant_id,
        "session_id": session.session_id,
        "total_observations": session.total_count(),
        "usable_observations": session.usable_count(),
        "rejected_observations": session.rejected_count(),
        "heart_rate": heart_rates_summary,
        "heart_rate_vs_baseline": compare_baseline(heart_rates_summary["average"], participant.baseline_heart_rate),
        "skin_response": skin_response_summary,
        "temperature": temperature_summary,
        "activity_level": activity_summary,
        "classification": classification,
        "recovery_detected": is_recovering,
        "recovery_explanation": recovery_explanation,
    }


def build_console_report(report): # make the report format, how it looks in the console.
    lines = []
    lines.append("=" * 60)
    lines.append(f"Session report: {report['session_id']} (participant {report['participant_id']})")
    lines.append("=" * 60)
    lines.append(f"Observations used: {report['usable_observations']}/"
                 f"{report['total_observations']} "
                 f"({report['rejected_observations']} rejected as missing/impossible/low-quality)")
    lines.append(f"Classification: {report['classification'].upper()}")
    lines.append(f"Recovery detected: {'yes' if report['recovery_detected'] else 'no'} "
                 f"- {report['recovery_explanation']}")
    lines.append("-" * 60)

    for label, key in (
        ("Heart rate (bpm)", "heart_rate"),
        ("Skin response", "skin_response"),
        ("Temperature (C)", "temperature"),
        ("Activity level", "activity_level"),
    ):
        summary = report[key]
        if summary["count"] == 0:
            lines.append(f"{label:<18}: no usable data")
        else:
            lines.append(f"{label:<18}: avg={summary['average']}, "
                         f"min={summary['min']}, max={summary['max']} "
                         f"(n={summary['count']})")

    if report["heart_rate_vs_baseline"] is not None:
        lines.append(f"Avg heart rate vs. baseline: {report['heart_rate_vs_baseline']:+.2f} bpm")


    return "\n".join(lines)