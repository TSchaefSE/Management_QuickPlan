
from . import services

def calculate_total_hours():
    logs = services.load_effort_logs()
    total = 0.0

    for log in logs:
        if not log:
            continue

        hours = log.get("hours_logged")

        if hours and str(hours).strip():
            total += float(hours)

    return total

