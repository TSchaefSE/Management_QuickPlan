from typing import Any, Dict, List, Optional
from datetime import datetime
from . import models


# =========================
# Generic Helpers
# =========================

def _clean_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _clean_int_like(value: Any) -> Optional[int]:
    cleaned = _clean_string(value)
    if not cleaned:
        return None

    try:
        return int(cleaned)
    except (TypeError, ValueError):
        return None


def _clean_float_like(value: Any) -> Optional[float]:
    cleaned = _clean_string(value)
    if not cleaned:
        return None

    try:
        return float(cleaned)
    except (TypeError, ValueError):
        return None


def _normalize_row_values(row: Dict[str, Any]) -> Dict[str, str]:
    normalized: Dict[str, str] = {}

    for key, value in row.items():
        normalized[key] = _clean_string(value)

    return normalized


def _rows_match_on_keys(
    row_a: Dict[str, Any],
    row_b: Dict[str, Any],
    keys: List[str],
) -> bool:
    for key in keys:
        if _clean_string(row_a.get(key)) != _clean_string(row_b.get(key)):
            return False
    return True


def _record_exists_by_id(
    records: List[Dict[str, Any]],
    id_field: str,
    id_value: Any,
) -> bool:
    normalized_id = _clean_string(id_value)

    if not normalized_id:
        return False

    for record in records:
        if _clean_string(record.get(id_field)) == normalized_id:
            return True

    return False


def _record_exists_by_keys(
    records: List[Dict[str, Any]],
    candidate: Dict[str, Any],
    keys: List[str],
) -> bool:
    for record in records:
        if _rows_match_on_keys(record, candidate, keys):
            return True

    return False


def ensure_all_csvs_exist() -> None:
    models.ensure_all_csvs_exist()


# =========================
# Projects
# =========================

def load_projects() -> List[Dict[str, Any]]:
    return models.get_all_projects()


def load_project_info() -> Optional[Dict[str, Any]]:
    return models.get_current_project()


def get_project_by_id(project_id: Any) -> Optional[Dict[str, Any]]:
    project_id = _clean_int_like(project_id)
    if project_id is None:
        return None

    return models.get_project_by_id(project_id)


def save_project_info(project_name: str, owner: str, description: str) -> int:
    project_name = _clean_string(project_name)
    owner = _clean_string(owner)
    description = _clean_string(description)

    if not project_name:
        raise ValueError("Project name is required.")

    if not owner:
        raise ValueError("Project owner is required.")

    existing_project = models.get_current_project()

    if existing_project:
        existing_payload = {
            "project_name": existing_project.get("project_name", ""),
            "owner": existing_project.get("owner", ""),
            "description": existing_project.get("description", ""),
        }

        incoming_payload = {
            "project_name": project_name,
            "owner": owner,
            "description": description,
        }

        if _rows_match_on_keys(
            existing_payload,
            incoming_payload,
            ["project_name", "owner", "description"],
        ):
            return int(existing_project["project_id"])

    saved_project = models.upsert_single_project(
        project_name=project_name,
        owner=owner,
        description=description,
    )
    return int(saved_project["project_id"])


# =========================
# Team Members
# =========================

def load_team_members(project_id: Any) -> List[Dict[str, Any]]:
    project_id = _clean_int_like(project_id)
    if project_id is None:
        return []

    return models.get_team_members_by_project(project_id)


def get_team_member_by_id(team_member_id: Any) -> Optional[Dict[str, Any]]:
    team_member_id = _clean_int_like(team_member_id)
    if team_member_id is None:
        return None

    return models.get_team_member_by_id(team_member_id)


def save_team_members(
    project_id: Any,
    member_names: List[str],
    member_roles: List[str],
    member_emails: List[str],
) -> List[Dict[str, Any]]:
    project_id = _clean_int_like(project_id)
    if project_id is None:
        raise ValueError("A valid project_id is required to save team members.")

    cleaned_rows: List[Dict[str, str]] = []
    seen_keys: List[Dict[str, str]] = []

    for name, role, email in zip(member_names, member_roles, member_emails):
        candidate = {
            "project_id": str(project_id),
            "member_name": _clean_string(name),
            "member_role": _clean_string(role),
            "member_email": _clean_string(email),
        }

        if not (candidate["member_name"] or candidate["member_role"] or candidate["member_email"]):
            continue

        if not candidate["member_name"]:
            raise ValueError("Each team member must have a name.")

        if not candidate["member_email"]:
            raise ValueError("Each team member must have an email.")

        duplicate_keys = ["project_id", "member_name", "member_email"]

        if _record_exists_by_keys(seen_keys, candidate, duplicate_keys):
            continue

        cleaned_rows.append(candidate)
        seen_keys.append(candidate)

    member_names_clean = [row["member_name"] for row in cleaned_rows]
    member_roles_clean = [row["member_role"] for row in cleaned_rows]
    member_emails_clean = [row["member_email"] for row in cleaned_rows]

    return models.replace_team_members_for_project(
        project_id=project_id,
        member_names=member_names_clean,
        member_roles=member_roles_clean,
        member_emails=member_emails_clean,
    )


# =========================
# Effort Logs
# =========================

def load_effort_logs() -> List[Dict[str, Any]]:
    return models.get_all_effort_logs()


def load_effort_logs_by_project(project_id: Any) -> List[Dict[str, Any]]:
    project_id = _clean_int_like(project_id)
    if project_id is None:
        return []

    return models.get_effort_logs_by_project(project_id)


def save_effort_log(log_data: Dict[str, Any]) -> Dict[str, Any]:
    project_id = _clean_int_like(log_data.get("project_id"))
    team_member_id = _clean_int_like(log_data.get("team_member_id"))
    project_phase = _clean_string(log_data.get("project_phase"))
    hours_logged = _clean_float_like(log_data.get("hours_logged"))
    date = _clean_string(log_data.get("date"))
    notes = _clean_string(log_data.get("notes"))
    effort_log_id = _clean_int_like(log_data.get("effort_log_id"))

    if project_id is None:
        raise ValueError("A valid project_id is required for an effort log.")

    if team_member_id is None:
        raise ValueError("A valid team_member_id is required for an effort log.")

    if not project_phase:
        raise ValueError("Project phase is required for an effort log.")

    if hours_logged is None:
        raise ValueError("Hours logged must be a valid number.")

    if hours_logged < 0:
        raise ValueError("Hours logged cannot be negative.")

    if not date:
        raise ValueError("Date is required for an effort log.")

    existing_logs = models.get_all_effort_logs()

    if effort_log_id is not None and _record_exists_by_id(existing_logs, "effort_log_id", effort_log_id):
        raise ValueError(f"Effort log with effort_log_id {effort_log_id} already exists.")

    candidate = {
        "project_id": project_id,
        "team_member_id": team_member_id,
        "project_phase": project_phase,
        "hours_logged": hours_logged,
        "date": date,
        "notes": notes,
    }

    duplicate_keys = [
        "project_id",
        "team_member_id",
        "project_phase",
        "hours_logged",
        "date",
        "notes",
    ]

    if _record_exists_by_keys(existing_logs, candidate, duplicate_keys):
        raise ValueError("Duplicate effort log detected. The same log entry already exists.")

    return models.insert_effort_log(
        project_id=project_id,
        team_member_id=team_member_id,
        project_phase=project_phase,
        hours_logged=hours_logged,
        date=date,
        notes=notes,
    )


# =========================
# Requirements
# =========================
def get_requirement_by_id(requirement_id: Any) -> Optional[Dict[str, Any]]:
    requirement_id = _clean_int_like(requirement_id)
    if requirement_id is None:
        return None

    return models.get_requirement_by_id(requirement_id)


def update_requirement(requirement_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    requirement_id = _clean_int_like(requirement_data.get("requirement_id"))
    project_id = _clean_int_like(requirement_data.get("project_id"))
    requirement_type = _clean_string(requirement_data.get("requirement_type"))
    priority = _clean_string(requirement_data.get("priority"))
    status = _clean_string(requirement_data.get("status"))
    title = _clean_string(requirement_data.get("title"))
    description = _clean_string(requirement_data.get("description"))

    if requirement_id is None:
        raise ValueError("A valid requirement_id is required for update.")
    if project_id is None:
        raise ValueError("A valid project_id is required for update.")
    if not requirement_type:
        raise ValueError("Requirement type is required.")
    if not priority:
        raise ValueError("Requirement priority is required.")
    if not status:
        raise ValueError("Requirement status is required.")
    if not title:
        raise ValueError("Requirement title is required.")

    existing_requirement = models.get_requirement_by_id(requirement_id)
    if not existing_requirement:
        raise ValueError(f"Requirement with requirement_id {requirement_id} does not exist.")

    existing_requirements = models.get_all_requirements()
    candidate = {
        "project_id": project_id,
        "requirement_type": requirement_type,
        "priority": priority,
        "status": status,
        "title": title,
        "description": description,
    }

    duplicate_keys = [
        "project_id",
        "requirement_type",
        "priority",
        "status",
        "title",
        "description",
    ]

    for record in existing_requirements:
        if _clean_string(record.get("requirement_id")) == str(requirement_id):
            continue
        if _rows_match_on_keys(record, candidate, duplicate_keys):
            raise ValueError("Updating this requirement would create a duplicate row.")

    return models.update_requirement(
        requirement_id=requirement_id,
        project_id=project_id,
        requirement_type=requirement_type,
        priority=priority,
        status=status,
        title=title,
        description=description,
    )


def delete_requirement(requirement_id: Any) -> bool:
    requirement_id = _clean_int_like(requirement_id)
    if requirement_id is None:
        raise ValueError("A valid requirement_id is required for delete.")

    return models.delete_requirement(requirement_id)


def load_requirements() -> List[Dict[str, Any]]:
    return models.get_all_requirements()


def load_requirements_by_project(project_id: Any) -> List[Dict[str, Any]]:
    project_id = _clean_int_like(project_id)
    if project_id is None:
        return []

    return models.get_requirements_by_project(project_id)


def save_requirement(requirement_data: Dict[str, Any]) -> Dict[str, Any]:
    project_id = _clean_int_like(requirement_data.get("project_id"))
    requirement_id = _clean_int_like(requirement_data.get("requirement_id"))
    requirement_type = _clean_string(requirement_data.get("requirement_type"))
    priority = _clean_string(requirement_data.get("priority"))
    status = _clean_string(requirement_data.get("status"))
    title = _clean_string(requirement_data.get("title"))
    description = _clean_string(requirement_data.get("description"))

    if project_id is None:
        raise ValueError("A valid project_id is required for a requirement.")

    if not requirement_type:
        raise ValueError("Requirement type is required.")

    if not priority:
        raise ValueError("Requirement priority is required.")

    if not status:
        raise ValueError("Requirement status is required.")

    if not title:
        raise ValueError("Requirement title is required.")

    existing_requirements = models.get_all_requirements()

    if requirement_id is not None and _record_exists_by_id(existing_requirements, "requirement_id", requirement_id):
        raise ValueError(f"Requirement with requirement_id {requirement_id} already exists.")

    candidate = {
        "project_id": project_id,
        "requirement_type": requirement_type,
        "priority": priority,
        "status": status,
        "title": title,
        "description": description,
    }

    duplicate_keys = [
        "project_id",
        "requirement_type",
        "priority",
        "status",
        "title",
        "description",
    ]

    if _record_exists_by_keys(existing_requirements, candidate, duplicate_keys):
        raise ValueError("Duplicate requirement detected. The same requirement already exists.")

    return models.insert_requirement(
        project_id=project_id,
        requirement_type=requirement_type,
        priority=priority,
        status=status,
        title=title,
        description=description,
    )


# =========================
# Risks
# =========================

def load_risks(project_id: Any) -> List[Dict[str, Any]]:
    project_id = _clean_int_like(project_id)
    if project_id is None:
        return []

    return models.get_risks_by_project(project_id)


def load_all_risks() -> List[Dict[str, Any]]:
    return models.get_all_risks()


def save_risks(
    project_id: Any,
    risk_names: List[str],
    risk_priorities: List[str],
    risk_statuses: List[str],
) -> List[Dict[str, Any]]:
    project_id = _clean_int_like(project_id)
    if project_id is None:
        raise ValueError("A valid project_id is required to save risks.")

    cleaned_rows: List[Dict[str, str]] = []
    seen_keys: List[Dict[str, str]] = []

    for name, priority, status in zip(risk_names, risk_priorities, risk_statuses):
        candidate = {
            "project_id": str(project_id),
            "risk_name": _clean_string(name),
            "risk_priority": _clean_string(priority),
            "risk_status": _clean_string(status),
        }

        if not (candidate["risk_name"] or candidate["risk_priority"] or candidate["risk_status"]):
            continue

        if not candidate["risk_name"]:
            raise ValueError("Each risk must have a name.")

        if not candidate["risk_priority"]:
            raise ValueError("Each risk must have a priority.")

        if not candidate["risk_status"]:
            raise ValueError("Each risk must have a status.")

        duplicate_keys = ["project_id", "risk_name", "risk_priority", "risk_status"]

        if _record_exists_by_keys(seen_keys, candidate, duplicate_keys):
            continue

        cleaned_rows.append(candidate)
        seen_keys.append(candidate)

    risk_names_clean = [row["risk_name"] for row in cleaned_rows]
    risk_priorities_clean = [row["risk_priority"] for row in cleaned_rows]
    risk_statuses_clean = [row["risk_status"] for row in cleaned_rows]

    return models.replace_risks_for_project(
        project_id=project_id,
        risk_names=risk_names_clean,
        risk_priorities=risk_priorities_clean,
        risk_statuses=risk_statuses_clean,
    )


# =========================
# Users
# =========================

def load_users() -> List[Dict[str, Any]]:
    return models.get_all_users()


def get_user_by_id(user_id: Any) -> Optional[Dict[str, Any]]:
    user_id = _clean_int_like(user_id)
    if user_id is None:
        return None

    return models.get_user_by_id(user_id)


def update_user(updated_user: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    user_id = _clean_int_like(updated_user.get("user_id"))
    if user_id is None:
        raise ValueError("A valid user_id is required to update a user.")

    existing_user = models.get_user_by_id(user_id)
    if not existing_user:
        raise ValueError(f"User with user_id {user_id} does not exist.")

    cleaned_user = {
        "user_id": user_id,
        "first_name": _clean_string(updated_user.get("first_name")),
        "last_name": _clean_string(updated_user.get("last_name")),
        "email": _clean_string(updated_user.get("email")),
        "phone_number": _clean_string(updated_user.get("phone_number")),
        "job_title": _clean_string(updated_user.get("job_title")),
        "department": _clean_string(updated_user.get("department")),
        "bio": _clean_string(updated_user.get("bio")),
        "profile_picture": _clean_string(
            updated_user.get("profile_picture", existing_user.get("profile_picture"))
        ),
    }

    if not cleaned_user["first_name"]:
        raise ValueError("User first name is required.")

    if not cleaned_user["last_name"]:
        raise ValueError("User last name is required.")

    if not cleaned_user["email"]:
        raise ValueError("User email is required.")

    unchanged_keys = [
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "job_title",
        "department",
        "bio",
        "profile_picture",
    ]

    if _rows_match_on_keys(existing_user, cleaned_user, unchanged_keys):
        return existing_user

    return models.update_user(cleaned_user)

VALID_PROJECT_PHASES = [
    "Planning",
    "Design",
    "Implementation",
    "Testing",
    "Documentation",
]


def _parse_date_safe(date_value: Any):
    if not date_value:
        return None

    cleaned = _clean_string(date_value)

    for fmt in ("%Y-%m-%d", "%m/%d/%Y"):
        try:
            return datetime.strptime(cleaned, fmt).date()
        except ValueError:
            continue

    return None


def build_report_data(
    project_id: Any,
    start_date: str = "",
    end_date: str = "",
    phase: str = "",
    member: str = "",
    requirement: str = "",
) -> Dict[str, Any]:
    project_id = _clean_int_like(project_id)

    if project_id is None:
        return {
            "summary": {
                "total_hours": 0.0,
                "avg_hours_per_day": 0.0,
                "active_members": 0,
            },
            "hours_by_phase": {phase_name: 0.0 for phase_name in VALID_PROJECT_PHASES},
            "breakdown": [],
            "members": [],
            "requirements_list": [],
        }

    all_logs = load_effort_logs_by_project(project_id)
    members = load_team_members(project_id)
    requirements_list = load_requirements_by_project(project_id)

    parsed_start_date = _parse_date_safe(start_date)
    parsed_end_date = _parse_date_safe(end_date)

    member_lookup = {
        str(member_row["team_member_id"]): member_row["member_name"]
        for member_row in members
    }

    filtered_logs = []
    for log in all_logs:
        log_member_name = member_lookup.get(str(log.get("team_member_id")), "Unknown Member")
        parsed_log_date = _parse_date_safe(log.get("date"))

        if parsed_start_date and parsed_log_date:
            if parsed_log_date < parsed_start_date:
                continue

        if parsed_end_date and parsed_log_date:
            if parsed_log_date > parsed_end_date:
                continue

        if parsed_start_date and not parsed_log_date:
            continue

        if parsed_end_date and not parsed_log_date:
            continue

        if phase and phase != "All Phases" and log.get("project_phase") != phase:
            continue

        if member and member != "All Team Members" and log_member_name != member:
            continue

        # Requirement filter is intentionally not applied yet because
        # effort logs are not linked to requirements in the current schema.

        enriched_log = dict(log)
        enriched_log["member_name"] = log_member_name
        filtered_logs.append(enriched_log)

    total_hours = round(
        sum(float(log.get("hours_logged", 0) or 0) for log in filtered_logs),
        2
    )

    unique_dates = {log.get("date") for log in filtered_logs if log.get("date")}
    avg_hours_per_day = round(total_hours / len(unique_dates), 2) if unique_dates else 0.0

    active_members = len({
        str(log.get("team_member_id"))
        for log in filtered_logs
        if log.get("team_member_id") not in (None, "")
    })

    hours_by_phase = {phase_name: 0.0 for phase_name in VALID_PROJECT_PHASES}
    for log in filtered_logs:
        current_phase = log.get("project_phase")
        if current_phase in hours_by_phase:
            hours_by_phase[current_phase] += float(log.get("hours_logged", 0) or 0)

    member_names = sorted({
        member_row["member_name"]
        for member_row in members
        if member_row.get("member_name")
    })

    return {
        "summary": {
            "total_hours": total_hours,
            "avg_hours_per_day": avg_hours_per_day,
            "active_members": active_members,
        },
        "hours_by_phase": hours_by_phase,
        "breakdown": filtered_logs,
        "members": member_names,
        "requirements_list": requirements_list,
    }