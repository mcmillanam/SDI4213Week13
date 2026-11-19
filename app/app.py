import os
import time
from flask import Flask, render_template, request, redirect, url_for, jsonify
import psycopg

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "helpdesk")
DB_USER = os.getenv("DB_USER", "helpdesk")
DB_PASSWORD = os.getenv("DB_PASSWORD", "helpdesk")
APP_TITLE = os.getenv("APP_TITLE", "Kubernetes Help Desk")


def db_connect():
    return psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        connect_timeout=3,
    )


def init_db(retries=30, delay=2):
    for attempt in range(retries):
        try:
            with db_connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        CREATE TABLE IF NOT EXISTS tickets (
                            id SERIAL PRIMARY KEY,
                            title TEXT NOT NULL,
                            priority TEXT NOT NULL,
                            status TEXT NOT NULL DEFAULT 'Open'
                        )
                        """
                    )
                conn.commit()
            return
        except Exception:
            if attempt == retries - 1:
                raise
            time.sleep(delay)


@app.route("/")
def index():
    tickets = []
    error = None
    try:
        with db_connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, title, priority, status FROM tickets ORDER BY id DESC")
                tickets = cur.fetchall()
    except Exception as exc:
        error = str(exc)
    return render_template("index.html", title=APP_TITLE, tickets=tickets, error=error)


@app.post("/tickets")
def add_ticket():
    title = request.form.get("title", "").strip()
    priority = request.form.get("priority", "Medium").strip()
    if title:
        with db_connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO tickets (title, priority, status) VALUES (%s, %s, 'Open')",
                    (title, priority),
                )
            conn.commit()
    return redirect(url_for("index"))


@app.get("/healthz")
def healthz():
    return jsonify(status="alive"), 200


@app.get("/ready")
def ready():
    try:
        with db_connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
        return jsonify(status="ready", database="reachable"), 200
    except Exception as exc:
        return jsonify(status="not-ready", database="unreachable", error=str(exc)), 503


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8080)
