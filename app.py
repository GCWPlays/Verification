from flask import Flask, redirect, request
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

import requests
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

    oauth_url = (
        f"https://discord.com/oauth2/authorize"
        f"?client_id={CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=identify guilds.join"
    )

    return redirect(oauth_url)

@app.route("/callback")
def callback():

    code = request.args.get("code")

    if not code:
        return "No code received."

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }

    token = requests.post(
        "https://discord.com/api/oauth2/token",
        data=data,
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    ).json()

    access_token = token.get("access_token")
    refresh_token = token.get("refresh_token")

    if not access_token:
        return f"OAuth Error:<br><pre>{token}</pre>"

    user = requests.get(
        "https://discord.com/api/users/@me",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    ).json()

    user_id = user["id"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO verified_users
        (user_id, refresh_token)
        VALUES (?, ?)
        """,
        (user_id, refresh_token)
    )

    conn.commit()
    conn.close()

    return """
    <h1>Verification Successful</h1>
    <p>You may now return to Discord.</p>
    """

@app.route("/stats")
def stats():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM verified_users"
    )

    count = cursor.fetchone()[0]

    conn.close()

    return f"Verified Users: {count}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
