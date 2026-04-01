
from flask import Blueprint, render_template, redirect, url_for

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
