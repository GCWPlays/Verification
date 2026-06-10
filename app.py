from flask import Flask
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS verified_users (
        user_id TEXT PRIMARY KEY,
        refresh_token TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return "Verification is online."

@app.route("/verify")
def verify():
    return "OAuth setup coming next."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
