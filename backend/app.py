from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from heroku_transfer import get_apps, transfer_app, get_config_vars, delete_app
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Needed for flash messages

# Home route
@app.route("/", methods=["GET", "POST"])
def home():
    apps_data = []
    if request.method == "POST":
        api_key = request.form.get("api_key")
        if api_key:
            try:
                apps = get_apps(api_key)
                # Add status for each app (assume we treat running apps as "Active")
                for a in apps:
                    apps_data.append({
                        "name": a["name"],
                        "id": a["id"],
                        "status": "Active"  # placeholder, can implement real status check later
                    })
            except Exception as e:
                flash(f"Error fetching apps: {str(e)}", "danger")
    return render_template("index.html", apps=apps_data)

# Delete apps route
@app.route("/delete_apps", methods=["POST"])
def delete_apps_route():
    api_key = request.form.get("api_key")
    selected_apps = request.form.getlist("selected_apps")
    if not selected_apps or not api_key:
        flash("No apps selected or API key missing.", "warning")
        return redirect(url_for("home"))

    for app_name in selected_apps:
        try:
            delete_app(api_key, app_name)
            flash(f"Deleted {app_name}", "success")
        except Exception as e:
            flash(f"Error deleting {app_name}: {str(e)}", "danger")
    return redirect(url_for("home"))

# Real-time JSON API to fetch apps (for AJAX)
@app.route("/fetch_apps_json", methods=["POST"])
def fetch_apps_json():
    api_key = request.json.get("api_key")
    if not api_key:
        return jsonify({"error": "API key missing"}), 400
    try:
        apps = get_apps(api_key)
        data = [{"name": a["name"], "status": "Active"} for a in apps]
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
