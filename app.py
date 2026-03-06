from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_NAME = "events.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            subject TEXT NOT NULL,
            title TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def get_events():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM events
        ORDER BY datetime(date || ' ' || time) ASC
    """)
    events = cursor.fetchall()
    conn.close()
    return events


@app.route("/")
def index():
    events = get_events()
    return render_template("index.html", events=events)


@app.route("/add", methods=["POST"])
def add_event():
    date = request.form.get("date", "").strip()
    time = request.form.get("time", "").strip()
    subject = request.form.get("subject", "").strip()
    title = request.form.get("title", "").strip()

    if not all([date, time, subject, title]):
        return "請完整填寫所有欄位", 400

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO events (date, time, subject, title)
        VALUES (?, ?, ?, ?)
    """, (date, time, subject, title))
    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/api/events")
def api_events():
    events = get_events()
    return jsonify([
        {
            "id": event["id"],
            "date": event["date"],
            "time": event["time"],
            "subject": event["subject"],
            "title": event["title"]
        }
        for event in events
    ])


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
