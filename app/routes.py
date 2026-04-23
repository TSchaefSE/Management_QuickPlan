import os.path

import pandas as pd
from flask import Blueprint, render_template, redirect, url_for, request, session
from app.services import (
    save_project_info,
    save_team_members,
    save_risks,
    load_project_info,
    load_team_members,
    load_risks,
    load_users,
    update_user,
    get_user_by_id,
    save_effort_log,
    load_effort_logs
)

from .calculations import calculate_total_hours, calculate_total_requirements, calculate_completed_requirements, \
    calculate_open_risk_count, calculate_hours_by_phase

main = Blueprint("main", __name__)


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

@main.route("/user", methods=["GET", "POST"])
def user_profile():
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("main.login"))

    user = get_user_by_id(user_id)

    if not user:
        session.pop("user_id", None)
        return redirect(url_for("main.login"))

    if request.method == "POST":
        updated_user = {
            "user_id": user_id,
            "first_name": request.form.get("first_name", "").strip(),
            "last_name": request.form.get("last_name", "").strip(),
            "email": request.form.get("email", "").strip(),
            "phone_number": request.form.get("phone_number", "").strip(),
            "job_title": request.form.get("job_title", "").strip(),
            "department": request.form.get("department", "").strip(),
            "bio": request.form.get("bio", "").strip(),
            "profile_picture": user["profile_picture"]
        }

        update_user(updated_user)

        return redirect(url_for("main.user_profile"))

    return render_template(
        "user/user_profile.html",
        active_page="user",
        user=user
    )


@main.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    requirements_count = calculate_total_requirements()
    completed_requirements = calculate_completed_requirements()
    total_hours = calculate_total_hours()
    open_risks = calculate_open_risk_count()
    hours_by_phase = calculate_hours_by_phase()

    return render_template(
        "dashboard/dashboard.html",
        active_page="dashboard",
        requirements_count=requirements_count,
        completed_requirements=completed_requirements,
        total_hours=total_hours,
        open_risks=open_risks,
        hours_by_phase=hours_by_phase
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
        new_log = {
            "date": request.form.get("date"),
            "team_member": request.form.get("member"),
            "project_phase": request.form.get("phase"),
            "hours_logged": request.form.get("hours"),
            "notes": request.form.get("task")
        }

        save_effort_log(new_log)

        return redirect(url_for("main.effort_logs"))
    
    logs = load_effort_logs()
    total_hours = calculate_total_hours()

    return render_template(
        "effort_logs/effort_logs.html",
        active_page="effort_logs",
        total_hours=total_hours,
        logs=logs
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
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    phase = request.args.get("phase")
    member = request.args.get("member")
    requirement = request.args.get("requirement")
    hours_by_phase = calculate_hours_by_phase()

    print("Reports filters:")
    print("Start Date:", start_date)
    print("End Date:", end_date)
    print("Phase:", phase)
    print("Member:", member)
    print("Requirement:", requirement)

    return render_template(
        "reports/reports.html",
        active_page="reports",
        summary={...},
        breakdown=[],
        hours_by_phase=hours_by_phase
    )