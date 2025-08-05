from flask import Flask, request, jsonify, render_template
import json, os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

RESPONSES_FILE = "responses.json"
SESSION_FILE = "session_data.json"

def load_responses():
    with open(RESPONSES_FILE, "r") as f:
        return json.load(f)

def save_responses(data):
    with open(RESPONSES_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_sessions():
    if not os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "w") as f: json.dump({}, f)
    with open(SESSION_FILE, "r") as f:
        return json.load(f)

def save_sessions(data):
    with open(SESSION_FILE, "w") as f:
        json.dump(data, f, indent=2)

responses = load_responses()

def get_bot_response(user_input):
    user_input = user_input.lower()
    for entry in responses:
        for keyword in entry["keywords"]:
            if keyword in user_input:
                return entry["response"]
    return next((r["response"] for r in responses if r["keywords"] == ["default"]), "Sorry, I don't understand.")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/admin/data")
def admin_data():
    return jsonify(load_responses())

@app.route("/admin/save", methods=["POST"])
def admin_save():
    updated = request.json
    save_responses(updated)
    return jsonify({"status": "success"})

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")
    bot_msg = get_bot_response(user_msg)

    sessions = load_sessions()
    sessions.setdefault("user1", []).append({"user": user_msg, "bot": bot_msg})
    save_sessions(sessions)

    return jsonify({"response": bot_msg})

if __name__ == "__main__":
    app.run(debug=True)
