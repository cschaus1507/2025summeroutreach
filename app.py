from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DATABASE = "responses.db"

EVENTS = [
    {
        "name": "STEM Day @ Niagara Cty Fair",
        "date": "Friday, August 1, 2025",
        "time": "12:00 PM – 6:00 PM",
        "location": "NC Fairgrounds",
        "link_html": '<a href="https://docs.google.com/spreadsheets/d/1-1bjIfMdGE5gYfaER2hgGOoLTGiUx2KVMdD8M9r2IC0/edit?usp=sharing" target="_blank" style="color:#FFD700; font-weight:bold;">Further details</a>'
    },
    {
        "name": "Until the Wheels Fall Off",
        "date": "Saturday, August 2, 2025",
        "time": "",
        "location": "Railyard Skate Park"
    },
    {
        "name": "Read with a Warlock",
        "date": "Tuesday, August 5, 2025",
        "time": "12:30 PM – 1:30 PM",
        "location": "Lock City Books"
    },
    {
        "name": "Food Fest",
        "date": "Sunday, August 10, 2025",
        "time": "",
        "location": "Main Street"
    },
    {
        "name": "UAW/GM Buy America Day",
        "date": "Saturday, August 16, 2025",
        "time": "",
        "location": "Delphi Plant"
    },
    {
        "name": "CCFCU Community Day",
        "date": "Saturday, August 23, 2025",
        "time": "",
        "location": "Kenan Center"
    },
    {
        "name": "Canal Cleanup",
        "date": "Date TBD",
        "time": "",
        "location": ""
    }
]

def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                event TEXT
            )
        """)
        conn.commit()
        conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name").strip()
        selected_events = request.form.getlist("events")
        if name and selected_events:
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            for event in selected_events:
                c.execute("INSERT INTO responses (name, event) VALUES (?, ?)", (name, event))
            conn.commit()
            conn.close()
        return redirect(url_for("index"))
    return render_template("index.html", events=EVENTS)

@app.route("/summary")
def summary():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT event, name FROM responses")
    rows = c.fetchall()
    conn.close()

    summary_data = {event["name"]: [] for event in EVENTS}
    for event, name in rows:
        summary_data[event].append(name)

    return render_template("summary.html", summary=summary_data)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)

