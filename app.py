from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Verification is online."

@app.route("/verify")
def verify():
    return """
    <h1>Verification</h1>
    <p>Verification system is online.</p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
