import os
from typing import Any, Dict, List, Optional
import pandas as pd
import sys

def get_base_path():
    if getattr(sys, "frozen", False):
        return getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))

    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


BASE_PATH = get_base_path()
DATA_FOLDER = os.path.join(BASE_PATH, "data")

PROJECTS_FILE = os.path.join(DATA_FOLDER, "projects.csv")
TEAM_MEMBERS_FILE = os.path.join(DATA_FOLDER, "team_members.csv")
EFFORT_LOGS_FILE = os.path.join(DATA_FOLDER, "effort_logs.csv")
REQUIREMENTS_FILE = os.path.join(DATA_FOLDER, "requirements.csv")
RISKS_FILE = os.path.join(DATA_FOLDER, "risks.csv")
USERS_FILE = os.path.join(DATA_FOLDER, "users.csv")

PROJECTS_COLUMNS = [
    "project_id",
    "project_name",
    "owner",
    "description",
]

TEAM_MEMBERS_COLUMNS = [
    "team_member_id",
    "project_id",
    "member_name",
    "member_role",
    "member_email",
]

EFFORT_LOGS_COLUMNS = [
    "effort_log_id",
    "project_id",
    "team_member_id",
    "project_phase",
    "hours_logged",
    "date",
    "notes",
]

REQUIREMENTS_COLUMNS = [
    "requirement_id",
    "project_id",
    "requirement_type",
    "priority",
    "status",
    "title",
    "description",
]

RISKS_COLUMNS = [
    "risk_id",
    "project_id",
    "risk_name",
    "risk_priority",
    "risk_status",
]

USERS_COLUMNS = [
    "user_id",
    "first_name",
    "last_name",
    "email",
    "phone_number",
    "job_title",
    "department",
    "bio",
    "profile_picture",
]


# =========================
# Generic CSV / DataFrame Helpers
# =========================

def ensure_data_folder_exists() -> None:
    os.makedirs(DATA_FOLDER, exist_ok=True)


def ensure_csv_exists(file_path: str, columns: List[str]) -> None:
    ensure_data_folder_exists()

    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        empty_df = pd.DataFrame(columns=columns)
        empty_df.to_csv(file_path, index=False)


def read_csv(file_path: str, columns: List[str]) -> pd.DataFrame:
    ensure_csv_exists(file_path, columns)

    try:
        df = pd.read_csv(file_path)
    except pd.errors.EmptyDataError:
        df = pd.DataFrame(columns=columns)

    if df.empty:
        return pd.DataFrame(columns=columns)

    df.columns = df.columns.str.strip()
    return df.reindex(columns=columns)


def write_csv(file_path: str, df: pd.DataFrame, columns: List[str]) -> None:
    ensure_data_folder_exists()

    safe_df = df.copy()
    safe_df = safe_df.reindex(columns=columns)
    safe_df.to_csv(file_path, index=False)


def get_next_id(df: pd.DataFrame, id_column: str) -> int:
    if df.empty or id_column not in df.columns:
        return 1

    numeric_ids = pd.to_numeric(df[id_column], errors="coerce").dropna()

    if numeric_ids.empty:
        return 1

    return int(numeric_ids.max()) + 1


def filter_by_column(df: pd.DataFrame, column_name: str, value: Any) -> pd.DataFrame:
    if df.empty or column_name not in df.columns:
        return pd.DataFrame(columns=df.columns)

    return df[df[column_name].astype(str).str.strip() == str(value).strip()].copy()


def first_row_as_dict(df: pd.DataFrame) -> Optional[Dict[str, Any]]:
    if df.empty:
        return None
    return df.iloc[0].to_dict()


# =========================
# File Initialization
# =========================

def ensure_projects_csv_exists() -> None:
    ensure_csv_exists(PROJECTS_FILE, PROJECTS_COLUMNS)


def ensure_team_members_csv_exists() -> None:
    ensure_csv_exists(TEAM_MEMBERS_FILE, TEAM_MEMBERS_COLUMNS)


def ensure_effort_logs_csv_exists() -> None:
    ensure_csv_exists(EFFORT_LOGS_FILE, EFFORT_LOGS_COLUMNS)


def ensure_requirements_csv_exists() -> None:
    ensure_csv_exists(REQUIREMENTS_FILE, REQUIREMENTS_COLUMNS)


def ensure_risks_csv_exists() -> None:
    ensure_csv_exists(RISKS_FILE, RISKS_COLUMNS)


def ensure_users_csv_exists() -> None:
    ensure_csv_exists(USERS_FILE, USERS_COLUMNS)


def ensure_all_csvs_exist() -> None:
    ensure_projects_csv_exists()
    ensure_team_members_csv_exists()
    ensure_effort_logs_csv_exists()
    ensure_requirements_csv_exists()
    ensure_risks_csv_exists()
    ensure_users_csv_exists()


# =========================
# Projects
# =========================

def load_projects_df() -> pd.DataFrame:
    return read_csv(PROJECTS_FILE, PROJECTS_COLUMNS)


def save_projects_df(df: pd.DataFrame) -> None:
    write_csv(PROJECTS_FILE, df, PROJECTS_COLUMNS)


def get_all_projects() -> List[Dict[str, Any]]:
    return load_projects_df().to_dict(orient="records")


def get_project_by_id(project_id: Any) -> Optional[Dict[str, Any]]:
    df = load_projects_df()
    matches = filter_by_column(df, "project_id", project_id)
    return first_row_as_dict(matches)


def get_current_project() -> Optional[Dict[str, Any]]:
    df = load_projects_df()
    return first_row_as_dict(df)


def upsert_single_project(project_name: str, owner: str, description: str) -> Dict[str, Any]:
    df = load_projects_df()
    existing_project = get_current_project()

    if existing_project:
        project_id = int(existing_project["project_id"])
    else:
        project_id = 1

    updated_df = pd.DataFrame([
        {
            "project_id": project_id,
            "project_name": project_name.strip(),
            "owner": owner.strip(),
            "description": description.strip(),
        }
    ])

    save_projects_df(updated_df)
    return updated_df.iloc[0].to_dict()


# =========================
# Team Members
# =========================

def load_team_members_df() -> pd.DataFrame:
    return read_csv(TEAM_MEMBERS_FILE, TEAM_MEMBERS_COLUMNS)


def save_team_members_df(df: pd.DataFrame) -> None:
    write_csv(TEAM_MEMBERS_FILE, df, TEAM_MEMBERS_COLUMNS)


def get_team_members_by_project(project_id: Any) -> List[Dict[str, Any]]:
    df = load_team_members_df()
    matches = filter_by_column(df, "project_id", project_id)
    return matches.to_dict(orient="records")


def get_team_member_by_id(team_member_id: Any) -> Optional[Dict[str, Any]]:
    df = load_team_members_df()
    matches = filter_by_column(df, "team_member_id", team_member_id)
    return first_row_as_dict(matches)


def replace_team_members_for_project(
    project_id: Any,
    member_names: List[str],
    member_roles: List[str],
    member_emails: List[str],
) -> List[Dict[str, Any]]:
    df = load_team_members_df()

    kept_df = df[df["project_id"].astype(str).str.strip() != str(project_id).strip()].copy()

    next_id = get_next_id(df, "team_member_id")
    new_rows: List[Dict[str, Any]] = []

    for name, role, email in zip(member_names, member_roles, member_emails):
        clean_name = str(name).strip()
        clean_role = str(role).strip()
        clean_email = str(email).strip()

        if not (clean_name or clean_role or clean_email):
            continue

        new_rows.append(
            {
                "team_member_id": next_id,
                "project_id": project_id,
                "member_name": clean_name,
                "member_role": clean_role,
                "member_email": clean_email,
            }
        )
        next_id += 1

    new_rows_df = pd.DataFrame(new_rows, columns=TEAM_MEMBERS_COLUMNS)
    result_df = pd.concat([kept_df, new_rows_df], ignore_index=True)

    save_team_members_df(result_df)
    return new_rows


# =========================
# Effort Logs
# =========================

def load_effort_logs_df() -> pd.DataFrame:
    df = read_csv(EFFORT_LOGS_FILE, EFFORT_LOGS_COLUMNS)

    if "hours_logged" in df.columns and not df.empty:
        df["hours_logged"] = pd.to_numeric(df["hours_logged"], errors="coerce")

    return df


def save_effort_logs_df(df: pd.DataFrame) -> None:
    write_csv(EFFORT_LOGS_FILE, df, EFFORT_LOGS_COLUMNS)


def get_all_effort_logs() -> List[Dict[str, Any]]:
    return load_effort_logs_df().to_dict(orient="records")


def get_effort_logs_by_project(project_id: Any) -> List[Dict[str, Any]]:
    df = load_effort_logs_df()
    matches = filter_by_column(df, "project_id", project_id)
    return matches.to_dict(orient="records")


def insert_effort_log(
    project_id: Any,
    team_member_id: Any,
    project_phase: str,
    hours_logged: Any,
    date: str,
    notes: str,
) -> Dict[str, Any]:
    df = load_effort_logs_df()

    new_row = {
        "effort_log_id": get_next_id(df, "effort_log_id"),
        "project_id": project_id,
        "team_member_id": team_member_id,
        "project_phase": str(project_phase).strip(),
        "hours_logged": pd.to_numeric(hours_logged, errors="coerce"),
        "date": str(date).strip(),
        "notes": str(notes).strip(),
    }

    new_df = pd.DataFrame([new_row], columns=EFFORT_LOGS_COLUMNS)
    updated_df = pd.concat([df, new_df], ignore_index=True)

    save_effort_logs_df(updated_df)
    return new_row


# =========================
# Requirements
# =========================
def get_requirement_by_id(requirement_id: Any) -> Optional[Dict[str, Any]]:
    df = load_requirements_df()
    matches = filter_by_column(df, "requirement_id", requirement_id)
    return first_row_as_dict(matches)


def update_requirement(
    requirement_id: Any,
    project_id: Any,
    requirement_type: str,
    priority: str,
    status: str,
    title: str,
    description: str,
) -> Optional[Dict[str, Any]]:
    df = load_requirements_df()

    if df.empty:
        return None

    mask = df["requirement_id"].astype(str).str.strip() == str(requirement_id).strip()
    if not mask.any():
        return None

    df.loc[mask, "project_id"] = project_id
    df.loc[mask, "requirement_type"] = requirement_type
    df.loc[mask, "priority"] = priority
    df.loc[mask, "status"] = status
    df.loc[mask, "title"] = title
    df.loc[mask, "description"] = description

    save_requirements_df(df)
    return first_row_as_dict(df[mask])


def delete_requirement(requirement_id: Any) -> bool:
    df = load_requirements_df()

    if df.empty:
        return False

    original_count = len(df)
    df = df[df["requirement_id"].astype(str).str.strip() != str(requirement_id).strip()].copy()

    if len(df) == original_count:
        return False

    save_requirements_df(df)
    return True

def load_requirements_df() -> pd.DataFrame:
    return read_csv(REQUIREMENTS_FILE, REQUIREMENTS_COLUMNS)


def save_requirements_df(df: pd.DataFrame) -> None:
    write_csv(REQUIREMENTS_FILE, df, REQUIREMENTS_COLUMNS)


def get_all_requirements() -> List[Dict[str, Any]]:
    return load_requirements_df().to_dict(orient="records")


def get_requirements_by_project(project_id: Any) -> List[Dict[str, Any]]:
    df = load_requirements_df()
    matches = filter_by_column(df, "project_id", project_id)
    return matches.to_dict(orient="records")


def insert_requirement(
    project_id: Any,
    requirement_type: str,
    priority: str,
    status: str,
    title: str,
    description: str,
) -> Dict[str, Any]:
    df = load_requirements_df()

    new_row = {
        "requirement_id": get_next_id(df, "requirement_id"),
        "project_id": project_id,
        "requirement_type": str(requirement_type).strip(),
        "priority": str(priority).strip(),
        "status": str(status).strip(),
        "title": str(title).strip(),
        "description": str(description).strip(),
    }

    new_df = pd.DataFrame([new_row], columns=REQUIREMENTS_COLUMNS)
    updated_df = pd.concat([df, new_df], ignore_index=True)

    save_requirements_df(updated_df)
    return new_row


# =========================
# Risks
# =========================

def load_risks_df() -> pd.DataFrame:
    return read_csv(RISKS_FILE, RISKS_COLUMNS)


def save_risks_df(df: pd.DataFrame) -> None:
    write_csv(RISKS_FILE, df, RISKS_COLUMNS)


def get_risks_by_project(project_id: Any) -> List[Dict[str, Any]]:
    df = load_risks_df()
    matches = filter_by_column(df, "project_id", project_id)
    return matches.to_dict(orient="records")


def get_all_risks() -> List[Dict[str, Any]]:
    return load_risks_df().to_dict(orient="records")


def replace_risks_for_project(
    project_id: Any,
    risk_names: List[str],
    risk_priorities: List[str],
    risk_statuses: List[str],
) -> List[Dict[str, Any]]:
    df = load_risks_df()

    kept_df = df[df["project_id"].astype(str).str.strip() != str(project_id).strip()].copy()

    next_id = get_next_id(df, "risk_id")
    new_rows: List[Dict[str, Any]] = []

    for name, priority, status in zip(risk_names, risk_priorities, risk_statuses):
        clean_name = str(name).strip()
        clean_priority = str(priority).strip()
        clean_status = str(status).strip()

        if not (clean_name or clean_priority or clean_status):
            continue

        new_rows.append(
            {
                "risk_id": next_id,
                "project_id": project_id,
                "risk_name": clean_name,
                "risk_priority": clean_priority,
                "risk_status": clean_status,
            }
        )
        next_id += 1

    new_rows_df = pd.DataFrame(new_rows, columns=RISKS_COLUMNS)
    result_df = pd.concat([kept_df, new_rows_df], ignore_index=True)

    save_risks_df(result_df)
    return new_rows


# =========================
# Users
# =========================

def load_users_df() -> pd.DataFrame:
    return read_csv(USERS_FILE, USERS_COLUMNS)


def save_users_df(df: pd.DataFrame) -> None:
    write_csv(USERS_FILE, df, USERS_COLUMNS)


def get_all_users() -> List[Dict[str, Any]]:
    return load_users_df().to_dict(orient="records")


def get_user_by_id(user_id: Any) -> Optional[Dict[str, Any]]:
    df = load_users_df()
    matches = filter_by_column(df, "user_id", user_id)
    return first_row_as_dict(matches)


def update_user(updated_user: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    df = load_users_df()

    if df.empty:
        return None

    target_mask = df["user_id"].astype(str).str.strip() == str(updated_user["user_id"]).strip()

    if not target_mask.any():
        return None

    for column in USERS_COLUMNS:
        if column in updated_user:
            df.loc[target_mask, column] = updated_user[column]

    save_users_df(df)
    return first_row_as_dict(df[target_mask])