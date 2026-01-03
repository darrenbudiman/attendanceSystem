from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "local-dev-key"

PEOPLE_CSV = "people.csv"
ATTENDANCE_CSV = "attendance.csv"


def ensure_people_csv_exists():
    """Create people.csv with header if it doesn't exist yet."""
    if not os.path.exists(PEOPLE_CSV):
        with open(PEOPLE_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["full_name"])
            writer.writeheader()


def load_people():
    ensure_people_csv_exists()
    people = []
    with open(PEOPLE_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = (row.get("full_name") or "").strip()
            if name:
                people.append(name)
    people.sort(key=lambda s: s.lower())
    return people


def append_attendance(event_date, full_name):
    file_exists = os.path.exists(ATTENDANCE_CSV)

    with open(ATTENDANCE_CSV, "a", newline="", encoding="utf-8") as f:
        fieldnames = ["event_date", "full_name", "timestamp"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "event_date": event_date,
            "full_name": full_name,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        })


def normalize_name(name: str) -> str:
    # Normalize whitespace: "  Juan   Dela  Cruz " -> "Juan Dela Cruz"
    return " ".join(name.strip().split())


def add_person_to_people_csv(full_name: str) -> bool:
    """
    Adds a new person if not already present (case-insensitive).
    Returns True if added, False if duplicate.
    """
    ensure_people_csv_exists()

    new_name = normalize_name(full_name)
    if not new_name:
        return False

    existing = load_people()
    existing_lower = {n.lower() for n in existing}
    if new_name.lower() in existing_lower:
        return False

    with open(PEOPLE_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["full_name"])
        writer.writerow({"full_name": new_name})

    return True


@app.route("/", methods=["GET"])
def index():
    people = load_people()
    return render_template("index.html", people=people)


@app.route("/submit", methods=["POST"])
def submit():
    event_date = request.form.get("event_date", "").strip()
    full_name = request.form.get("full_name", "").strip()

    if not event_date or not full_name:
        flash("Please select a name and fill event name/date.")
        return redirect(url_for("index"))

    append_attendance(event_date, full_name)
    flash(f"Recorded attendance for: {full_name}")
    return redirect(url_for("index"))


@app.route("/add_person", methods=["POST"])
def add_person():
    full_name = request.form.get("new_full_name", "")
    new_name = normalize_name(full_name)

    if len(new_name) < 2:
        flash("Name is too short. Please enter a full name.")
        return redirect(url_for("index"))

    added = add_person_to_people_csv(new_name)
    if added:
        flash(f"Added new person: {new_name}")
    else:
        flash(f"'{new_name}' is already in the list (or invalid).")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)