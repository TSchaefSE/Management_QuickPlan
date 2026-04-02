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

    print("Reports filters:")
    print("Start Date:", start_date)
    print("End Date:", end_date)
    print("Phase:", phase)
    print("Member:", member)
    print("Requirement:", requirement)

    return render_template(
        "reports/reports.html",
        active_page="reports",
        summary={
            "total_hours": 127.5,
            "avg_hours_per_day": 8.5,
            "active_members": 4
        },
        breakdown=[],
        chart_data=[]
    )