import pandas as pd

from . import models

VALID_PROJECT_PHASES = [
    "Planning",
    "Design",
    "Implementation",
    "Testing",
    "Documentation",
]


# =========================
# Hours Calculations
# =========================

def calculate_total_hours(project_id=None) -> float:
    effort_df = models.load_effort_logs_df()

    if project_id is not None:
        effort_df = _filter_by_project_id(effort_df, project_id)

    if effort_df.empty or "hours_logged" not in effort_df.columns:
        return 0.0

    effort_df = effort_df.copy()
    effort_df["hours_logged"] = pd.to_numeric(
        effort_df["hours_logged"],
        errors="coerce"
    ).fillna(0)

    return round(float(effort_df["hours_logged"].sum()), 2)


def calculate_hours_by_phase(project_id=None) -> dict:
    effort_df = models.load_effort_logs_df()

    if project_id is not None:
        effort_df = _filter_by_project_id(effort_df, project_id)

    if effort_df.empty:
        return {phase: 0.0 for phase in VALID_PROJECT_PHASES}

    effort_df = effort_df.copy()
    effort_df["hours_logged"] = pd.to_numeric(
        effort_df["hours_logged"],
        errors="coerce"
    ).fillna(0)

    effort_df = effort_df[effort_df["project_phase"].isin(VALID_PROJECT_PHASES)]

    grouped = effort_df.groupby("project_phase")["hours_logged"].sum().to_dict()

    ordered_result = {}
    for phase in VALID_PROJECT_PHASES:
        ordered_result[phase] = round(float(grouped.get(phase, 0)), 2)

    return ordered_result


def calculate_active_team_member_count(project_id=None) -> int:
    effort_df = models.load_effort_logs_df()

    if project_id is not None:
        effort_df = _filter_by_project_id(effort_df, project_id)

    if effort_df.empty or "team_member_id" not in effort_df.columns:
        return 0

    return int(
        effort_df["team_member_id"]
        .dropna()
        .astype(str)
        .str.strip()
        .replace("", pd.NA)
        .dropna()
        .nunique()
    )


def calculate_average_hours_per_day(project_id=None) -> float:
    effort_df = models.load_effort_logs_df()

    if project_id is not None:
        effort_df = _filter_by_project_id(effort_df, project_id)

    if effort_df.empty or "date" not in effort_df.columns or "hours_logged" not in effort_df.columns:
        return 0.0

    effort_df = effort_df.copy()
    effort_df["date"] = pd.to_datetime(effort_df["date"], errors="coerce")
    effort_df["hours_logged"] = pd.to_numeric(
        effort_df["hours_logged"],
        errors="coerce"
    ).fillna(0)

    unique_days = effort_df["date"].dropna().dt.date.nunique()
    if unique_days == 0:
        return 0.0

    total_hours = float(effort_df["hours_logged"].sum())
    return round(total_hours / unique_days, 2)


# =========================
# Requirements Calculations
# =========================

def calculate_total_requirements(project_id=None) -> int:
    requirements_df = models.load_requirements_df()

    if project_id is not None:
        requirements_df = _filter_by_project_id(requirements_df, project_id)

    if requirements_df.empty or "requirement_id" not in requirements_df.columns:
        return 0

    return int(
        requirements_df["requirement_id"]
        .dropna()
        .astype(str)
        .str.strip()
        .replace("", pd.NA)
        .dropna()
        .nunique()
    )


def calculate_completed_requirements(project_id=None) -> int:
    requirements_df = models.load_requirements_df()

    if project_id is not None:
        requirements_df = _filter_by_project_id(requirements_df, project_id)

    if requirements_df.empty or "status" not in requirements_df.columns:
        return 0

    requirements_df = requirements_df.copy()
    requirements_df["status"] = (
        requirements_df["status"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    return int((requirements_df["status"] == "completed").sum())


# =========================
# Risk Calculations
# =========================

def calculate_open_risk_count(project_id=None) -> int:
    risks_df = models.load_risks_df()

    if project_id is not None:
        risks_df = _filter_by_project_id(risks_df, project_id)

    if risks_df.empty or "risk_status" not in risks_df.columns:
        return 0

    risks_df = risks_df.copy()
    risks_df["risk_status"] = (
        risks_df["risk_status"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    return int((risks_df["risk_status"] == "open").sum())


# =========================
# Report Helpers
# =========================

def build_project_summary(project_id=None) -> dict:
    return {
        "total_hours": calculate_total_hours(project_id),
        "avg_hours_per_day": calculate_average_hours_per_day(project_id),
        "active_members": calculate_active_team_member_count(project_id),
        "requirements_count": calculate_total_requirements(project_id),
        "completed_requirements": calculate_completed_requirements(project_id),
        "open_risks": calculate_open_risk_count(project_id),
        "hours_by_phase": calculate_hours_by_phase(project_id),
    }


# =========================
# Internal Helpers
# =========================

def _filter_by_project_id(df: pd.DataFrame, project_id) -> pd.DataFrame:
    if df.empty or "project_id" not in df.columns:
        return df.iloc[0:0].copy()

    return df[
        df["project_id"].astype(str).str.strip() == str(project_id).strip()
    ].copy()