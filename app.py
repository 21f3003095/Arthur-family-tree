"""
app.py
Flask web server for the Family Tree UI.
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from seeder import build_arthur_family
from family_tree import CHILD_ADDED, CHILD_ADDITION_FAILED, PERSON_NOT_FOUND, NONE_RESULT
import os

app = Flask(__name__, static_folder="static")
CORS(app)

tree = build_arthur_family()


def tree_to_json():
    """Serialise the entire tree into a JSON-friendly structure."""
    members = []
    for name, person in tree._members.items():
        members.append({
            "name":     person.name,
            "gender":   person.gender.value,
            "mother":   person.mother.name if person.mother else None,
            "father":   person.father.name if person.father else None,
            "spouse":   person.spouse.name if person.spouse else None,
            "children": [c.name for c in person.children],
        })
    return members

# Routes

@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/api/tree", methods=["GET"])
def get_tree():
    return jsonify({"members": tree_to_json()})


@app.route("/api/add_child", methods=["POST"])
def add_child():
    data        = request.get_json()
    mother_name = data.get("mother", "").strip()
    child_name  = data.get("child", "").strip()
    gender      = data.get("gender", "").strip()

    if not mother_name or not child_name or not gender:
        return jsonify({"result": CHILD_ADDITION_FAILED, "message": "All fields are required."}), 400

    result = tree.add_child(mother_name, child_name, gender)

    messages = {
        CHILD_ADDED:           f"{child_name} was successfully added to the family tree.",
        CHILD_ADDITION_FAILED: f"Could not add child — '{mother_name}' is either male or the name already exists.",
        PERSON_NOT_FOUND:      f"'{mother_name}' was not found in the family tree.",
    }

    status = 200 if result == CHILD_ADDED else 400
    return jsonify({
        "result":  result,
        "message": messages.get(result, result),
        "members": tree_to_json() if result == CHILD_ADDED else None,
    }), status


@app.route("/api/get_relationship", methods=["POST"])
def get_relationship():
    """Used by the webpage search form."""
    data         = request.get_json()
    name         = data.get("name", "").strip()
    relationship = data.get("relationship", "").strip()

    if not name or not relationship:
        return jsonify({"result": NONE_RESULT, "message": "Name and relationship are required."}), 400

    result = tree.get_relationship(name, relationship)

    if result == PERSON_NOT_FOUND:
        message = f"'{name}' was not found in the family tree."
        names   = []
    elif result == NONE_RESULT:
        message = f"{name} has no {relationship}."
        names   = []
    else:
        names   = result.split()
        message = f"Found {len(names)} result(s) for {name}'s {relationship}."

    return jsonify({
        "result":  result,
        "message": message,
        "names":   names,
    })


@app.route("/api/command", methods=["POST"])
def run_command():

    from main import process_command

    data   = request.get_json()
    line   = data.get("command", "").strip()

    if not line:
        return jsonify({"result": "ERROR", "message": "No command provided."}), 400

    result = process_command(tree, line)

    if result is None:
        return jsonify({"result": "IGNORED", "message": "Blank or comment line."})

    return jsonify({
        "result":  result,
        "message": result,
        "members": tree_to_json() if result == CHILD_ADDED else None,
    })


@app.route("/api/reset", methods=["POST"])
def reset():
    global tree
    tree = build_arthur_family()
    return jsonify({"message": "Family tree reset to original.", "members": tree_to_json()})


@app.route("/api/members", methods=["GET"])
def get_members():
    return jsonify({"names": list(tree._members.keys())})


if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    app.run(debug=True, port=5000)