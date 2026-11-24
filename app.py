"""Flask backend for the Password Strength and Breach Checker."""
import requests
from flask import Flask, jsonify, render_template, request

from breach import check_breach
from scorer import get_feedback, get_rating, score_password

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/tips")
def tips():
    return render_template("tips.html")


@app.route("/api/strength", methods=["POST"])
def api_strength():
    data = request.get_json(silent=True) or {}
    password = data.get("password", "")
    score = score_password(password)
    return jsonify({
        "score": score,
        "max_score": 6,
        "rating": get_rating(score),
        "feedback": get_feedback(password),
    })


@app.route("/api/breach", methods=["POST"])
def api_breach():
    data = request.get_json(silent=True) or {}
    password = data.get("password", "")
    if not password:
        return jsonify({"error": "Please enter a password."}), 400
    try:
        count = check_breach(password)
    except requests.RequestException:
        return jsonify({"error": "Could not reach the breach service."}), 503
    return jsonify({"breached": count > 0, "count": count})


if __name__ == "__main__":
    app.run(debug=True)
