import os.path

import pandas as pd
from flask import Blueprint, render_template, redirect, url_for, request
from app.services import (
    save_project_info,
    save_team_members,
    save_risks,
    load_project_info,
    load_team_members,
    load_risks
)

from .calculations import calculate_total_hours, calculate_total_requirements, calculate_completed_requirements, \
    calculate_open_risk_count, calculate_hours_by_phase

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return redirect(url_for("main.dashboard"))

@main.route("/user", methods=["GET", "POST"])
def user_profile():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        job_title = request.form.get("job_title")
        department = request.form.get("department")
        bio = request.form.get("bio")
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_new_password = request.form.get("confirm_new_password")

        print("user profile submitted:")
        print(first_name, last_name, email, phone, job_title, department, bio)

        return redirect(url_for("main.user_profile"))

    return render_template(
        "user/user_profile.html",
        active_page="user",
        user={
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.smith@company.com",
            "phone": "+1 (555) 123-4567",
            "job_title": "Product Owner",
            "department": "Product Management",
            "bio": "Experienced product owner with 8+ years in agile project management and software development."
        }
    )


@main.route("/dashboard")
def dashboard():
    requirements_count = calculate_total_requirements()
    completed_requirements = calculate_completed_requirements()
    total_hours = calculate_total_hours()
    open_risks = calculate_open_risk_count()
    hours_by_phase = calculate_hours_by_phase()

    return render_template(
        "dashboard/dashboard.html",
        active_page = "dashboard",
        requirements_count=requirements_count,
        completed_requirements = completed_requirements,
        total_hours = total_hours,
        open_risks = open_risks,
        hours_by_phase = hours_by_phase

    )


@main.route("/project-info", methods=["GET", "POST"])
def project_info():
    if request.method == "POST":
        project_name = request.form.get("project_name", "").strip()
        owner = request.form.get("owner", "").strip()
        description = request.form.get("description", "").strip()

        member_names = request.form.getlist("member_name[]")
        member_roles = request.form.getlist("member_role[]")
        member_emails = request.form.getlist("member_email[]")

        risk_names = request.form.getlist("risk_name[]")
        risk_priorities = request.form.getlist("risk_priority[]")
        risk_statuses = request.form.getlist("risk_status[]")

        project_id = save_project_info(
            project_name=project_name,
            owner=owner,
            description=description
        )

        save_team_members(
            project_id=project_id,
            member_names=member_names,
            member_roles=member_roles,
            member_emails=member_emails
        )

        save_risks(
            project_id=project_id,
            risk_names=risk_names,
            risk_priorities=risk_priorities,
            risk_statuses=risk_statuses
        )

    project = load_project_info()

    if project:
        members = load_team_members(project["id"])
        risks = load_risks(project["id"])
    else:
        members = []
        risks = []

    return render_template(
        "project_info/project_info.html",
        active_page="project_info",
        project=project,
        members=members,
        risks=risks
    )

@main.route("/effort_logs", methods=["GET", "POST"])
def effort_logs():
    if request.method == "POST":
        date = request.form.get("date")
        member = request.form.get("member")
        phase = request.form.get("phase")
        hours = request.form.get("hours")
        task = request.form.get("task")

        ### save to CSV here ###

        # TEMP FOR TESTING
        print("Effort log submitted:")
        print("Date:", date)
        print("Member:", member)
        print("Phase:", phase)
        print("Hours:", hours)
        print("Task:", task)

        return redirect(url_for("main.effort_logs"))

    total_hours = calculate_total_hours()

    return render_template(
        "effort_logs/effort_logs.html",
        active_page="effort_logs",
        total_hours=total_hours
    )

@main.route("/requirements", methods=["GET", "POST"])
def requirements():
    if request.method == "POST":
        requirement_id = request.form.get("requirement_id")
        requirement_type = request.form.get("requirement_type")
        priority = request.form.get("priority")
        status = request.form.get("status")
        title = request.form.get("title")
        description = request.form.get("description")

        ### save to CSV here ###

        # TEMP FOR TESTING
        print("Requirement submitted:")
        print("ID:", requirement_id)
        print("Type:", requirement_type)
        print("Priority:", priority)
        print("Status:", status)
        print("Title:", title)
        print("Description:", description)

        return redirect(url_for("main.requirements"))

    return render_template(
        "requirements/requirements.html",
        active_page="requirements",
        requirements=[]
    )

@main.route("/reports", methods=["GET"])
def reports():
    start_date = (request.args.get("start_date") or "").strip()
    end_date = (request.args.get("end_date") or "").strip()
    phase = (request.args.get("phase") or "").strip()
    member = (request.args.get("member") or "").strip()
    requirement = (request.args.get("requirement") or "").strip()

    effort_file = os.path.join("data", "effort_logs.csv")
    requirement_file = os.path.join("data", "requirements.csv")
    valid_phases = ["Planning", "Design", "Implementation", "Testing", "Documentation"]

    if os.path.exists(effort_file):
        effort_df = pd.read_csv(effort_file)
    else:
        effort_df = pd.DataFrame(columns=[
            "log_id", "team_member", "project_phase", "hours_logged", "date", "notes"
        ])

    if not effort_df.empty:
        effort_df.columns = effort_df.columns.str.strip()

        if "date" in effort_df.columns:
            effort_df["date"] = pd.to_datetime(effort_df["date"], errors="coerce")

        if "hours_logged" in effort_df.columns:
            effort_df["hours_logged"] = pd.to_numeric(
                effort_df["hours_logged"], errors="coerce"
            ).fillna(0)

        if start_date and "date" in effort_df.columns:
            effort_df = effort_df[effort_df["date"] >= pd.to_datetime(start_date)]

        if end_date and "date" in effort_df.columns:
            effort_df = effort_df[effort_df["date"] <= pd.to_datetime(end_date)]

        if phase and phase != "All Phases" and "project_phase" in effort_df.columns:
            effort_df = effort_df[effort_df["project_phase"] == phase]

        if member and member != "All Team Members" and "team_member" in effort_df.columns:
            effort_df = effort_df[effort_df["team_member"] == member]

    total_hours = round(float(effort_df["hours_logged"].sum()), 2) if "hours_logged" in effort_df.columns else 0

    if not effort_df.empty and "date" in effort_df.columns:
        unique_days = effort_df["date"].dropna().dt.date.nunique()
        avg_hours_per_day = round(total_hours / unique_days, 2) if unique_days else 0
    else:
        avg_hours_per_day = 0

    active_members = effort_df["team_member"].dropna().nunique() if "team_member" in effort_df.columns else 0

    grouped = {}
    if not effort_df.empty and {"project_phase", "hours_logged"}.issubset(effort_df.columns):
        grouped = effort_df.groupby("project_phase")["hours_logged"].sum().to_dict()

    hours_by_phase = {}
    for current_phase in valid_phases:
        hours_by_phase[current_phase] = round(float(grouped.get(current_phase, 0)), 2)

    breakdown = []

    if os.path.exists(requirement_file):
        requirements_df = pd.read_csv(requirement_file)
        requirements_df.columns = requirements_df.columns.str.strip()

    expected_columns = {"requirement_id", "description", "status"}
    if expected_columns.issubset(requirements_df.columns):
        if requirement and requirement != "All Requirements":
            requirements_df = requirements_df[
                requirements_df["requirement_id"].astype(str).str.strip() == requirement
            ]

        for _, row in requirements_df.iterrows():
            breakdown.append({
                "requirement_id": row.get("requirement_id", ""),
                "title": row.get("description", "No description"),
                "hours": 0,
                "status": row.get("status", "Unknown")
            })

    summary = {
        "total_hours": total_hours,
        "avg_hours_per_day": avg_hours_per_day,
        "active_members": int(active_members)
    }

    return render_template(
        "reports/reports.html",
        active_page="reports",
        summary=summary,
        breakdown=breakdown,
        hours_by_phase=hours_by_phase
    )