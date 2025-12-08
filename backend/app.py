from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from heroku_transfer import get_apps, transfer_app, get_app_status, delete_app
import os

app = Flask(__name__, static_folder="frontend")
CORS(app)

@app.route("/apps", methods=["POST"])
def list_apps():
    source_key = request.json.get("source_api_key")
    try:
        apps = get_apps(source_key)
        return jsonify([app["name"] for app in apps])
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/status", methods=["POST"])
def app_status():
    data = request.json
    app_name = data.get("app_name")
    api_key = data.get("api_key")
    try:
        running = get_app_status(app_name, api_key)
        return jsonify({"running": running})
    except Exception as e:
        return jsonify({"running": False, "error": str(e)}), 400

@app.route("/transfer", methods=["POST"])
def transfer_selected_apps():
    data = request.json
    source_key = data.get("source_api_key")
    target_key = data.get("target_api_key")
    selected_apps = data.get("apps", [])
    results = []
    for app_name in selected_apps:
        try:
            result = transfer_app(app_name, source_key, target_key)
            results.append(result)
        except Exception as e:
            results.append({"app": app_name, "status": "failed", "error": str(e)})
    return jsonify(results)

@app.route("/delete", methods=["POST"])
def delete_selected_apps():
    data = request.json
    api_key = data.get("api_key")
    selected_apps = data.get("apps", [])
    results = []
    for app_name in selected_apps:
        try:
            result = delete_app(app_name, api_key)
            results.append(result)
        except Exception as e:
            results.append({"app": app_name, "status": "failed", "error": str(e)})
    return jsonify(results)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
