from flask import Blueprint, render_template, redirect, url_for, request
from app.services import (
    save_project_info,
    save_team_members,
    save_risks,
    load_project_info,
    load_team_members,
    load_risks
)

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return redirect(url_for("main.dashboard"))


@main.route("/dashboard")
def dashboard():
    return render_template(
        "dashboard/dashboard.html",
        active_page="dashboard"
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

        #TEMP FOR TESTING
        print("Effort log submitted:")
        print("Date:", date)
        print("Member:", member)
        print("Phase:", phase)
        print("Hours:", hours)
        print("Task:", task)

        return redirect(url_for("main.effort_logs"))

    return render_template(
        "effort_logs/effort_logs.html",
        active_page="effort_logs",
        logs=[]
    )