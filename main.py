import os
from pathlib import Path

from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename

from extract_files import extract_zip
from analytics import SalesAnalytics, show_report_in_console


app = Flask(__name__)


app.secret_key = "secret-key"

UPLOAD_FOLDER = "transactions"
ALLOWED_EXTENSIONS = {"zip"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def format_currency(value):
    return f"₦{value:,.2f}"


@app.template_filter("format_hour")
def format_hour(hour):
    return f"{int(hour):02d}:00"


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)

        file = request.files["file"]
        name_of_file_without_extension = file.filename.rsplit(".")[0]

        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            extract_zip(
                os.path.join(UPLOAD_FOLDER, filename),
                Path(f"./transactions/{name_of_file_without_extension}"),
            )
            flash("File uploaded successfully")
            return redirect(url_for("dashboard", data=name_of_file_without_extension))
        else:
            flash("Invalid file type. Please upload a ZIP file.")
            return redirect(request.url)

    return render_template("home.html")


@app.route("/analytics")
def dashboard():
    try:
        data = request.args.get("data")
        analytics = SalesAnalytics()
        analytics.process_directory(f"./transactions/{data}/")
        report = analytics.generate_report()

        show_report_in_console(report)

        return render_template(
            "dashboard.html", report=report, format_currency=format_currency
        )
    except Exception:
        return "Such data does not exist or please input valid data"
