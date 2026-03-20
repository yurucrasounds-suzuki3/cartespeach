from flask import Flask, render_template, request, jsonify
import sqlite3
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
DB_PATH = Path("karte.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS karte (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            customer_name TEXT,
            menu TEXT,
            color TEXT,
            length TEXT,
            concerns TEXT,
            caution TEXT,
            next_plan TEXT,
            memo TEXT,
            transcript TEXT
        )
        """
    )
    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM karte ORDER BY id DESC LIMIT 50"
    ).fetchall()
    conn.close()
    return render_template("index.html", records=rows)


@app.route("/save", methods=["POST"])
def save():
    data = request.get_json()

    customer_name = data.get("customerName", "").strip()
    menu = data.get("menu", "").strip()
    color = data.get("color", "").strip()
    length = data.get("length", "").strip()
    concerns = data.get("concerns", "").strip()
    caution = data.get("caution", "").strip()
    next_plan = data.get("next", "").strip()
    memo = data.get("memo", "").strip()
    transcript = data.get("transcript", "").strip()

    if not customer_name:
        return jsonify({"status": "error", "message": "顧客名を入れてください"}), 400

    conn = get_conn()
    conn.execute(
        """
        INSERT INTO karte (
            created_at, customer_name, menu, color, length,
            concerns, caution, next_plan, memo, transcript
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            customer_name,
            menu,
            color,
            length,
            concerns,
            caution,
            next_plan,
            memo,
            transcript,
        ),
    )
    conn.commit()
    conn.close()

    return jsonify({"status": "ok", "message": "保存しました"})


if __name__ == "__main__":
    init_db()
    app.run(debug=True)