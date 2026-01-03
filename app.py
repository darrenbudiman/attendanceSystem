"""
Requirements
    - pip install openpyxl, flask
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from openpyxl import Workbook, load_workbook
import csv
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "local-dev-key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PEOPLE_CSV = os.path.join(BASE_DIR, "people.csv")
ATTENDANCE_XLSX = os.path.join(BASE_DIR, "attendance.xlsx")

def ensure_people_csv_exists():
    if not os.path.exists(PEOPLE_CSV):
        with open(PEOPLE_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["full_name", "sex"])
            writer.writeheader()

def get_sex_by_name(full_name: str) -> str:
    people = load_people()
    for p in people:
        if p["full_name"].lower() == full_name.lower():
            return p["sex"]
    return ""

def load_people():
    ensure_people_csv_exists()
    print("READING PEOPLE CSV FROM:", PEOPLE_CSV)
    people = []

    with open(PEOPLE_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = (row.get("full_name") or "").strip()
            sex = (row.get("sex") or "").strip().upper()
            if name and sex:
                people.append({
                    "full_name": name,
                    "sex": sex
                })

    people.sort(key=lambda p: p["full_name"].lower())
    return people

def ensure_attendance_excel_exists():
    if not os.path.exists(ATTENDANCE_XLSX):
        wb = Workbook()
        ws = wb.active
        ws.title = "Attendance"
        ws.append(["event_date", "full_name", "sex", "timestamp"])
        wb.save(ATTENDANCE_XLSX)

def append_attendance(event_date, full_name):
    ensure_attendance_excel_exists()

    sex = get_sex_by_name(full_name)

    wb = load_workbook(ATTENDANCE_XLSX)
    ws = wb.worksheets[0]  # FIRST SHEET ONLY

    ws.append([
        event_date,
        full_name,
        sex,
        datetime.now().isoformat(timespec="seconds")
    ])

    wb.save(ATTENDANCE_XLSX)


def normalize_name(name: str) -> str:
    # Normalize whitespace: "  Juan   Dela  Cruz " -> "Juan Dela Cruz"
    return " ".join(name.strip().split())


def add_person_to_people_csv(full_name: str, sex: str) -> bool:
    ensure_people_csv_exists()

    new_name = normalize_name(full_name)
    sex = sex.upper()

    if not new_name or sex not in {"M", "F"}:
        return False

    existing = load_people()
    existing_lower = {p["full_name"].lower() for p in existing}

    if new_name.lower() in existing_lower:
        return False

    with open(PEOPLE_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["full_name", "sex"])
        writer.writerow({
            "full_name": new_name,
            "sex": sex
        })

    return True

@app.route("/", methods=["GET"])
def index():
    people = load_people()
    return render_template("index.html", people=people)

@app.route("/submit", methods=["POST"])
def submit():
    event_date = request.form.get("event_date", "").strip()
    names_raw = request.form.get("full_names", "").strip()

    if not event_date or not names_raw:
        flash("Please select at least one name and event date.")
        return redirect(url_for("index"))

    names = [n.strip() for n in names_raw.split(",") if n.strip()]

    for full_name in names:
        append_attendance(event_date, full_name)

    flash(f"Recorded attendance for {len(names)} people.")
    return redirect(url_for("index"))


@app.route("/add_person", methods=["POST"])
def add_person():
    full_name = request.form.get("new_full_name", "")
    sex = request.form.get("sex", "")

    new_name = normalize_name(full_name)

    if len(new_name) < 2:
        flash("Name is too short.")
        return redirect(url_for("index"))

    added = add_person_to_people_csv(new_name, sex)
    if added:
        flash(f"Added new person: {new_name} ({sex})")
    else:
        flash("Person already exists or invalid sex.")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)