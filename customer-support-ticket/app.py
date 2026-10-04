"""
Customer Support Ticket Priority Prediction and Automated Assignment System
Demo website for the Salesforce / Agentforce project (Naan Mudhalvan).

This Flask app only DEMONSTRATES the documented priority logic.
It does not use a machine learning model and does not use a database.
"""

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ---------------------------------------------------------------
# Documented priority keywords (same as the Salesforce Flow logic)
# ---------------------------------------------------------------
HIGH_KEYWORDS = ["urgent", "not working", "failure"]
MEDIUM_KEYWORDS = ["issue", "slow", "delay"]


def find_priority(description):
    """Check the ticket description for keywords and return the priority."""
    text = description.lower()

    # Step 1: High priority keywords are checked first
    for word in HIGH_KEYWORDS:
        if word in text:
            return "High", word

    # Step 2: Medium priority keywords
    for word in MEDIUM_KEYWORDS:
        if word in text:
            return "Medium", word

    # Step 3: Default priority
    return "Low", None


def build_result(priority):
    """Decide the assigned agent, action message and urgent task status."""
    if priority == "High":
        return {
            "assigned_agent": "Senior Support Agent",
            "action_message": "High priority ticket detected. Assigned to senior agent.",
            "urgent_task_status": "Urgent Ticket Handling Task Created",
        }
    if priority == "Medium":
        return {
            "assigned_agent": "Support Agent",
            "action_message": "Ticket marked as medium priority. Will be handled shortly.",
            "urgent_task_status": "No urgent task required",
        }
    return {
        "assigned_agent": "Support Agent",
        "action_message": "Ticket is low priority and queued for processing.",
        "urgent_task_status": "No urgent task required",
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True) or {}

    account_name = (data.get("account_name") or "").strip()
    issue_type = (data.get("issue_type") or "").strip()
    description = (data.get("description") or "").strip()

    if not account_name or not description:
        return jsonify({"error": "Please enter the account name and ticket description."}), 400

    priority, matched_keyword = find_priority(description)
    result = build_result(priority)

    result["priority"] = priority
    result["matched_keyword"] = matched_keyword
    result["account_name"] = account_name
    result["issue_type"] = issue_type
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
