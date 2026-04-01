import csv
import os

DATA_FOLDER = "data"
PROJECTS_FILE = os.path.join(DATA_FOLDER, "projects.csv")
TEAM_MEMBERS_FILE = os.path.join(DATA_FOLDER, "team_members.csv")
RISKS_FILE = os.path.join(DATA_FOLDER, "risks.csv")


# =========================
# Ensure Files Exist
# =========================
def ensure_projects_csv_exists():
    os.makedirs(DATA_FOLDER, exist_ok=True)

    if not os.path.exists(PROJECTS_FILE) or os.path.getsize(PROJECTS_FILE) == 0:
        with open(PROJECTS_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "id",
                "project_name",
                "owner",
                "description"
            ])


def ensure_team_members_csv_exists():
    os.makedirs(DATA_FOLDER, exist_ok=True)

    if not os.path.exists(TEAM_MEMBERS_FILE) or os.path.getsize(TEAM_MEMBERS_FILE) == 0:
        with open(TEAM_MEMBERS_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "id",
                "project_id",
                "member_name",
                "member_role",
                "member_email"
            ])


def ensure_risks_csv_exists():
    os.makedirs(DATA_FOLDER, exist_ok=True)

    if not os.path.exists(RISKS_FILE) or os.path.getsize(RISKS_FILE) == 0:
        with open(RISKS_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "id",
                "project_id",
                "risk_name",
                "risk_priority",
                "risk_status"
            ])


# =========================
# Load Current Project Data
# =========================
def load_project_info():
    ensure_projects_csv_exists()

    with open(PROJECTS_FILE, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            return row

    return None


def load_team_members(project_id):
    ensure_team_members_csv_exists()
    members = []

    with open(TEAM_MEMBERS_FILE, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["project_id"] == str(project_id):
                members.append(row)

    return members


def load_risks(project_id):
    ensure_risks_csv_exists()
    risks = []

    with open(RISKS_FILE, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["project_id"] == str(project_id):
                risks.append(row)

    return risks


# =========================
# Save Current Project Data
# =========================
def save_project_info(project_name, owner, description):
    ensure_projects_csv_exists()

    existing_project = load_project_info()

    if existing_project:
        project_id = int(existing_project["id"])
    else:
        project_id = 1

    with open(PROJECTS_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "id",
            "project_name",
            "owner",
            "description"
        ])
        writer.writerow([
            project_id,
            project_name,
            owner,
            description
        ])

    return project_id


def save_team_members(project_id, member_names, member_roles, member_emails):
    ensure_team_members_csv_exists()

    with open(TEAM_MEMBERS_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "id",
            "project_id",
            "member_name",
            "member_role",
            "member_email"
        ])

        next_id = 1
        for name, role, email in zip(member_names, member_roles, member_emails):
            if name.strip() or role.strip() or email.strip():
                writer.writerow([
                    next_id,
                    project_id,
                    name.strip(),
                    role.strip(),
                    email.strip()
                ])
                next_id += 1


def save_risks(project_id, risk_names, risk_priorities, risk_statuses):
    ensure_risks_csv_exists()

    with open(RISKS_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "id",
            "project_id",
            "risk_name",
            "risk_priority",
            "risk_status"
        ])

        next_id = 1
        for name, priority, status in zip(risk_names, risk_priorities, risk_statuses):
            if name.strip() or priority.strip() or status.strip():
                writer.writerow([
                    next_id,
                    project_id,
                    name.strip(),
                    priority.strip(),
                    status.strip()
                ])
                next_id += 1