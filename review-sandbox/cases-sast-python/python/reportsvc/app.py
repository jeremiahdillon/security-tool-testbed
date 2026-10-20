"""Invoice/report service — serves generated reports and manages user accounts."""
import base64
import hashlib
import os
import pickle

from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

REPORT_ROOT = "/srv/reports"


@app.route("/reports/download")
def download_report():
    """Return a previously generated report file by name."""
    name = request.args.get("name", "")
    full_path = os.path.join(REPORT_ROOT, name)
    return send_file(full_path)


@app.route("/users/register", methods=["POST"])
def register():
    """Create a user, storing a hash of their password."""
    username = request.form["username"]
    password = request.form["password"]
    digest = hashlib.md5(password.encode("utf-8")).hexdigest()
    save_user(username, digest)
    return jsonify({"username": username})


@app.route("/session/resume", methods=["POST"])
def resume_session():
    """Restore session state from a client-provided token."""
    token = request.form["token"]
    raw = base64.b64decode(token)
    state = pickle.loads(raw)
    return jsonify({"user": state.get("user"), "roles": state.get("roles", [])})


def save_user(username, digest):
    with open(os.path.join(REPORT_ROOT, "users.tsv"), "a") as fh:
        fh.write(f"{username}\t{digest}\n")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
