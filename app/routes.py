import os
import sys
import csv
from datetime import datetime
import io
from flask import Blueprint, render_template, redirect, url_for, request, session, send_file
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from datetime import datetime, timedelta

from app.services import (
    load_projects,
    load_project_info,
    create_project,
    delete_project,
    save_project_info,
    load_team_members,
    save_team_members,
    load_risks,
    save_risks,
    load_users,
    get_user_by_id,
    update_user,
    load_effort_logs_by_project,
    save_effort_log,
    load_requirements_by_project,
    save_requirement,
    get_requirement_by_id,
    update_requirement,
    delete_requirement,
    build_report_data,
)

from .calculations import (
    calculate_total_hours,
    calculate_total_requirements,
    calculate_completed_requirements,
    calculate_open_risk_count,
    calculate_hours_by_phase,
    build_project_summary,
)

main = Blueprint("main", __name__)


# =========================
# Helpers
# =========================

def _require_login():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return user_id


def _require_current_project():
    selected_project_id = session.get("project_id")

    if selected_project_id:
        project = load_project_info(selected_project_id)
        if project:
            return project

    projects = load_projects()

    if not projects:
        return None

    first_project = projects[0]
    session["project_id"] = first_project["project_id"]

    return first_project


# =========================
# Auth / Navigation
# =========================

@main.route("/")
def home():
    return redirect(url_for("main.login"))


@main.route("/login", methods=["GET", "POST"])
def login():
    users = load_users()

    if request.method == "POST":
        selected_user_id = request.form.get("user_id")
        user = get_user_by_id(selected_user_id)

        if user:
            session["user_id"] = user["user_id"]
            return redirect(url_for("main.dashboard"))

    return render_template("login/login.html", users=users)


@main.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.login"))


@main.route("/projects/select", methods=["POST"])
def select_project():
    user_id = _require_login()
    if not user_id:
        return redirect(url_for("main.login"))

    selected_project_id = request.form.get("project_id")

    if selected_project_id:
        session["project_id"] = selected_project_id

    return redirect(request.referrer or url_for("main.dashboard"))


@main.route("/projects/new", methods=["POST"])
def new_project():
    user_id = _require_login()
    if not user_id:
        return redirect(url_for("main.login"))

    new_project_row = create_project(
        project_name="New Project",
        owner="Unassigned",
        description=""
    )

    session["project_id"] = new_project_row["project_id"]

    return redirect(url_for("main.project_info"))


# =========================
# User Profile
# =========================

@main.route("/user", methods=["GET", "POST"])
def user_profile():
    user_id = _require_login()
    if not user_id:
        return redirect(url_for("main.login"))

    user = get_user_by_id(user_id)
    if not user:
        session.pop("user_id", None)
        return redirect(url_for("main.login"))

    if request.method == "POST":
        updated_user = {
            "user_id": user_id,
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "email": request.form.get("email"),
            "phone_number": request.form.get("phone_number"),
            "job_title": request.form.get("job_title"),
            "department": request.form.get("department"),
            "bio": request.form.get("bio"),
            "profile_picture": user.get("profile_picture", ""),
        }

        update_user(updated_user)
        return redirect(url_for("main.user_profile"))

    return render_template(
        "user/user_profile.html",
        active_page="user",
        user=user,
    )


# =========================
# Dashboard
# =========================

@main.route("/dashboard")
def dashboard():
    user_id = _require_login()
    if not user_id:
        return redirect(url_for("main.login"))

    project = _require_current_project()
    project_id = project["project_id"] if project else None

    requirements_count = calculate_total_requirements(project_id)
    completed_requirements = calculate_completed_requirements(project_id)
    total_hours = calculate_total_hours(project_id)
    open_risks = calculate_open_risk_count(project_id)
    hours_by_phase = calculate_hours_by_phase(project_id)

    return render_template(
        "dashboard/dashboard.html",
        active_page="dashboard",
        requirements_count=requirements_count,
        completed_requirements=completed_requirements,
        total_hours=total_hours,
        open_risks=open_risks,
        hours_by_phase=hours_by_phase,
        project=project,
    )


# =========================
# Project Info
# =========================

@main.route("/project-info", methods=["GET", "POST"])
def project_info():
    user_id = _require_login()
    if not user_id:
        return redirect(url_for("main.login"))

    if request.method == "POST":
        project_name = request.form.get("project_name")
        owner = request.form.get("owner")
        description = request.form.get("description")

        member_names = request.form.getlist("member_name[]")
        member_roles = request.form.getlist("member_role[]")
        member_emails = request.form.getlist("member_email[]")

        risk_names = request.form.getlist("risk_name[]")
        risk_priorities = request.form.getlist("risk_priority[]")
        risk_statuses = request.form.getlist("risk_status[]")

        project = _require_current_project()

        project_id = save_project_info(
            project_id=project["project_id"],
            project_name=project_name,
            owner=owner,
            description=description,
        )

        save_team_members(
            project_id=project_id,
            member_names=member_names,
            member_roles=member_roles,
            member_emails=member_emails,
        )

        save_risks(
            project_id=project_id,
            risk_names=risk_names,
            risk_priorities=risk_priorities,
            risk_statuses=risk_statuses,
        )

        return redirect(url_for("main.project_info"))

    project = _require_current_project()

    if project:
        project_id = project["project_id"]
        members = load_team_members(project_id)
        risks = load_risks(project_id)
    else:
        members = []
        risks = []

    return render_template(
        "project_info/project_info.html",
        active_page="project_info",
        project=project,
        members=members,
        risks=risks,
    )

@main.route("/projects/delete", methods=["POST"])
def delete_current_project():
    user_id = _require_login()
    if not user_id:
        return redirect(url_for("main.login"))

    project = _require_current_project()
    projects = load_projects()

    if not project:
        return redirect(url_for("main.dashboard"))

    if len(projects) <= 1:
        return redirect(url_for("main.dashboard"))

    delete_project(project["project_id"])

    remaining_projects = load_projects()

    if remaining_projects:
        session["project_id"] = remaining_projects[0]["project_id"]
    else:
        session.pop("project_id", None)

    return redirect(url_for("main.dashboard"))


# =========================
# Effort Logs
# =========================

@main.route("/effort_logs", methods=["GET", "POST"])
def effort_logs():
    user_id = _require_login()
    if not user_id:
        return redirect(url_for("main.login"))

    project = _require_current_project()

    if request.method == "POST":
        if project:
            new_log = {
                "project_id": project["project_id"],
                "team_member_id": request.form.get("team_member_id"),
                "project_phase": request.form.get("phase"),
                "hours_logged": request.form.get("hours"),
                "date": request.form.get("date"),
                "notes": request.form.get("task"),
            }

            print("NEW LOG:", new_log)
            save_effort_log(new_log)

        return redirect(url_for("main.effort_logs"))

    if project:
        project_id = project["project_id"]
        logs = load_effort_logs_by_project(project_id)
        members = load_team_members(project_id)
    else:
        logs = []
        members = []

    total_hours = calculate_total_hours(project["project_id"]) if project else 0.0

    return render_template(
        "effort_logs/effort_logs.html",
        active_page="effort_logs",
        total_hours=total_hours,
        logs=logs,
        members=members,
        project=project,
    )


# =========================
# Requirements
# =========================

@main.route("/requirements", methods=["GET", "POST"])
def requirements():
    user_id = _require_login()
    if not user_id:
        return redirect(url_for("main.login"))

    project = _require_current_project()
    editing_requirement = None

    if request.method == "POST":
        if project:
            editing_requirement_id = request.form.get("editing_requirement_id")

            requirement_payload = {
                "project_id": project["project_id"],
                "requirement_type": request.form.get("requirement_type"),
                "priority": request.form.get("priority"),
                "status": request.form.get("status"),
                "title": request.form.get("title"),
                "description": request.form.get("description"),
            }

            if editing_requirement_id:
                requirement_payload["requirement_id"] = editing_requirement_id
                update_requirement(requirement_payload)
            else:
                save_requirement(requirement_payload)

        return redirect(url_for("main.requirements"))

    edit_id = request.args.get("edit_id")
    if edit_id:
        editing_requirement = get_requirement_by_id(edit_id)

    if project:
        requirements_list = load_requirements_by_project(project["project_id"])
    else:
        requirements_list = []

    return render_template(
        "requirements/requirements.html",
        active_page="requirements",
        requirements=requirements_list,
        project=project,
        editing_requirement=editing_requirement,
    )

@main.route("/requirements/delete/<int:requirement_id>", methods=["POST"])
def delete_requirement_route(requirement_id):
    user_id = _require_login()
    if not user_id:
        return redirect(url_for("main.login"))

    delete_requirement(requirement_id)
    return redirect(url_for("main.requirements"))


# =========================
# Reports
# =========================

@main.route("/reports", methods=["GET"])
def reports():
    user_id = _require_login()
    if not user_id:
        return redirect(url_for("main.login"))

    project = _require_current_project()
    project_id = project["project_id"] if project else None

    today = datetime.today()
    default_start_date = today - timedelta(days=30)
    
    start_date = request.args.get("start_date", default_start_date.strftime("%Y-%m-%d")).strip()
    end_date = request.args.get("end_date", today.strftime("%Y-%m-%d")).strip()

    if start_date and end_date and end_date < start_date:
        end_date = start_date
        
    phase = request.args.get("phase", "").strip()
    member = request.args.get("member", "").strip()

    report_data = build_report_data(
        project_id=project_id,
        start_date=start_date,
        end_date=end_date,
        phase=phase,
        member=member,
        requirement="",
    )

    return render_template(
        "reports/reports.html",
        active_page="reports",
        summary=report_data["summary"],
        breakdown=report_data["breakdown"],
        hours_by_phase=report_data["hours_by_phase"],
        project=project,
        members=report_data["members"],
        selected_start_date=start_date,
        selected_end_date=end_date,
        selected_phase=phase,
        selected_member=member,
    )

@main.route("/reports/export/csv", methods=["GET"])
def export_reports_csv():
    user_id = _require_login()
    if not user_id:
        return redirect(url_for("main.login"))

    project = _require_current_project()
    project_id = project["project_id"] if project else None

    report_data = build_report_data(
        project_id=project_id,
        start_date=request.args.get("start_date", "").strip(),
        end_date=request.args.get("end_date", "").strip(),
        phase=request.args.get("phase", "").strip(),
        member=request.args.get("member", "").strip(),
        requirement=request.args.get("requirement", "").strip(),
    )

    export_folder = _get_export_folder()
    file_path = os.path.join(
        export_folder,
        f"quickplan_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )

    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Team Member", "Phase", "Hours", "Notes"])

        for row in report_data["breakdown"]:
            writer.writerow([
                row.get("date", ""),
                row.get("member_name", ""),
                row.get("project_phase", ""),
                row.get("hours_logged", ""),
                row.get("notes", ""),
            ])

    os.startfile(file_path)
    return redirect(url_for("main.reports"))


@main.route("/reports/export/pdf", methods=["GET"])
def export_reports_pdf():
    user_id = _require_login()
    if not user_id:
        return redirect(url_for("main.login"))

    project = _require_current_project()
    project_id = project["project_id"] if project else None

    start_date = request.args.get("start_date", "").strip()
    end_date = request.args.get("end_date", "").strip()
    phase = request.args.get("phase", "").strip()
    member = request.args.get("member", "").strip()

    report_data = build_report_data(
        project_id=project_id,
        start_date=start_date,
        end_date=end_date,
        phase=phase,
        member=member,
        requirement="",
    )

    export_folder = _get_export_folder()
    file_path = os.path.join(
        export_folder,
        f"quickplan_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    )

    doc = SimpleDocTemplate(
        file_path,
        pagesize=landscape(letter),
        leftMargin=30,
        rightMargin=30,
        topMargin=30,
        bottomMargin=30,
    )

    styles = getSampleStyleSheet()
    elements = []

    project_name = project["project_name"] if project else "No Project"
    elements.append(Paragraph(f"Management QuickPlan Report - {project_name}", styles["Title"]))
    elements.append(Spacer(1, 12))

    summary = report_data["summary"]
    summary_data = [
        ["Metric", "Value"],
        ["Total Hours", str(summary["total_hours"])],
        ["Avg Hours/Day", str(summary["avg_hours_per_day"])],
        ["Active Members", str(summary["active_members"])],
    ]

    summary_table = Table(summary_data, hAlign="LEFT")
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2f4f6f")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 18))

    details_data = [["Date", "Team Member", "Phase", "Hours", "Notes"]]

    for row in report_data["breakdown"]:
        details_data.append([
            str(row.get("date", "")),
            str(row.get("member_name", "")),
            str(row.get("project_phase", "")),
            str(row.get("hours_logged", "")),
            str(row.get("notes", "")),
        ])

    if len(details_data) == 1:
        details_data.append(["No data", "", "", "", ""])

    details_table = Table(
        details_data,
        repeatRows=1,
        colWidths=[90, 120, 120, 70, 320],
        hAlign="LEFT",
    )
    details_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2f4f6f")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("PADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))

    elements.append(Paragraph("Effort Log Breakdown", styles["Heading2"]))
    elements.append(Spacer(1, 8))
    elements.append(details_table)

    doc.build(elements)

    try:
        os.startfile(file_path)
    except Exception:
        pass

    return redirect(url_for("main.reports"))

def _get_export_folder():
    if getattr(sys, "frozen", False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    export_folder = os.path.join(base_path, "exports")
    os.makedirs(export_folder, exist_ok=True)
    return export_folder

@main.app_context_processor
def inject_projects():
    projects = load_projects()
    selected_project = None

    selected_project_id = session.get("project_id")

    if selected_project_id:
        selected_project = load_project_info(selected_project_id)

    if not selected_project and projects:
        selected_project = projects[0]

    return {
        "available_projects": projects,
        "selected_project": selected_project,
    }