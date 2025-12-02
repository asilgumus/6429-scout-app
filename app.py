from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json, os

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app) 

TEAMS_FILE = "./static/teams.json"

def load_matches(name=TEAMS_FILE):
    if not os.path.exists(name):
        return []
    with open(name, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_matches(matches, name=TEAMS_FILE):
    with open(name, "w", encoding="utf-8") as f:
        json.dump(matches, f, ensure_ascii=False, indent=2)

@app.route("/")
def mainPage():
    return render_template("index.html")

@app.route("/detail.html")
def detailPage():
    return render_template("detail.html")

@app.route("/scout")
def scoutPage():
    return render_template("scout.html")

@app.route("/scout/getmatches", methods=["GET"])
def get_matches():
    matches = load_matches()
    return jsonify(matches)

@app.route("/detail_info", methods=["GET"])
def return_matchInfo():
    team_id = request.args.get("team_id", type=int)
    matches = load_matches()
    team_matches = [m for m in matches if m.get("team_number") == team_id]
    return jsonify(team_matches)




@app.route("/scout/creatematch", methods=["POST"])
def create_match():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON or empty body"}), 400

    try:
        entry = {
            "team_number": int(data.get("team_number") or 0),
            "match_id": str(data.get("match_id") or ""),
            "alliance": str(data.get("alliance") or ""),
            "auto_score": int(data.get("auto_score") or 0),
            "teleop_score": int(data.get("teleop_score") or 0),
            "notes": str(data.get("notes") or "")
        }
    except (ValueError, TypeError) as e:
        return jsonify({"error": "Invalid field types", "detail": str(e)}), 400

    try:
        matches = load_matches()
        matches.append(entry)
        save_matches(matches)
    except Exception as e:
        return jsonify({"error": "Could not save data", "detail": str(e)}), 500

    return jsonify({"message": "OK", "entry": entry}), 200

if __name__ == "__main__":
    app.run(debug=True)
