
import os
import pandas as pd
from . import services

# =========================
# Hours Calculations
# =========================

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

def calculate_hours_by_phase():
    df = pd.read_csv("data/effort_logs.csv")

    valid_phases = ["Planning", "Design", "Implementation", "Testing", "Documentation"]

    df["hours_logged"] = pd.to_numeric(df["hours_logged"], errors="coerce").fillna(0)
    df = df[df["project_phase"].isin(valid_phases)]

    grouped = df.groupby("project_phase")["hours_logged"].sum().to_dict()

    ordered_result = {}
    for phase in valid_phases:
        ordered_result[phase] = grouped.get(phase, 0)

    return ordered_result


# =========================
# Requirements Calculations
# =========================

def calculate_total_requirements():
    file_path = os.path.join("data", "requirements.csv")
    requirements_count = 0

    if os.path.exists(file_path):
        req_data = pd.read_csv(file_path)
        req_data.columns = req_data.columns.str.strip()

        if not req_data.empty and "requirement_id" in req_data.columns:
            req_data["requirement_id"] = req_data["requirement_id"].astype(str).str.strip()

            requirements_count = req_data["requirement_id"].nunique()

    return requirements_count

def calculate_completed_requirements():
    file_path = os.path.join("data", "requirements.csv")

    if not os.path.exists(file_path):
        return 0

    try:
        req_data = pd.read_csv(file_path)
        req_data.columns = req_data.columns.str.strip()

        if req_data.empty or "status" not in req_data.columns:
            return 0

        # Normalize status values (handles "completed", "Completed ", etc.)
        req_data["status"] = req_data["status"].astype(str).str.strip().str.lower()

        completed_count = len(req_data[req_data["status"] == "completed"])

        return completed_count

    except Exception as e:
        print("Error reading requirements:", e)
        return 0

# =========================
# Risk Calculations
# =========================

def calculate_open_risk_count():
    file_path = os.path.join("data", "risks.csv")

    if not os.path.exists(file_path):
        return 0

    try:
        risk_data = pd.read_csv(file_path)
        risk_data.columns = risk_data.columns.str.strip()

        if risk_data.empty or "risk_status" not in risk_data.columns:
            return 0

        # Normalize status values
        risk_data["risk_status"] = risk_data["risk_status"].astype(str).str.strip().str.lower()

        open_risks_count = len(risk_data[risk_data["risk_status"] == "open"])

        return open_risks_count

    except Exception as e:
        print("Error reading risks:", e)
        return 0