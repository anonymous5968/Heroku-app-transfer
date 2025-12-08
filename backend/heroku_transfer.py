import os
import subprocess
import requests

HEROKU_API = "https://api.heroku.com"
HEADERS = {"Accept": "application/vnd.heroku+json; version=3"}


def get_apps(api_key):
    """Fetch all apps for a given API key."""
    headers = HEADERS.copy()
    headers["Authorization"] = f"Bearer {api_key}"
    try:
        response = requests.get(f"{HEROKU_API}/apps", headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch apps: {e}")
        return []


def get_config_vars(api_key, app_name):
    """Get config vars for a given app."""
    headers = HEADERS.copy()
    headers["Authorization"] = f"Bearer {api_key}"
    try:
        response = requests.get(f"{HEROKU_API}/apps/{app_name}/config-vars", headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch config vars for {app_name}: {e}")
        return {}


def rename_app(api_key, old_name, new_name):
    """Rename an existing app."""
    headers = HEADERS.copy()
    headers["Authorization"] = f"Bearer {api_key}"
    try:
        response = requests.patch(f"{HEROKU_API}/apps/{old_name}", headers=headers, json={"name": new_name})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"[ERROR] Failed to rename {old_name} to {new_name}: {e}")
        return {}


def create_app(api_key, app_name):
    """Create a new Heroku app."""
    headers = HEADERS.copy()
    headers["Authorization"] = f"Bearer {api_key}"
    try:
        response = requests.post(f"{HEROKU_API}/apps", headers=headers, json={"name": app_name})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"[ERROR] Failed to create app {app_name}: {e}")
        return {}


def push_code(source_app_name, target_app_name, source_key, target_key):
    """Clone a source app and push its code to a target app."""
    try:
        subprocess.run(
            ["git", "clone", f"https://heroku:{source_key}@git.heroku.com/{source_app_name}.git"],
            check=True,
        )
        os.chdir(source_app_name)
        subprocess.run(
            ["git", "remote", "add", "target", f"https://heroku:{target_key}@git.heroku.com/{target_app_name}.git"],
            check=True,
        )
        subprocess.run(["git", "push", "target", "main", "--force"], check=True)
        os.chdir("..")
        subprocess.run(["rm", "-rf", source_app_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Git operation failed: {e}")


def set_config_vars(api_key, app_name, config_vars):
    """Set config vars for a Heroku app."""
    headers = HEADERS.copy()
    headers["Authorization"] = f"Bearer {api_key}"
    try:
        response = requests.patch(f"{HEROKU_API}/apps/{app_name}/config-vars", headers=headers, json=config_vars)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"[ERROR] Failed to set config vars for {app_name}: {e}")
        return {}


def transfer_app(app_name, source_key, target_key):
    """Transfer an app from source account to target account."""
    try:
        config_vars = get_config_vars(source_key, app_name)
        temp_name = app_name + "-old-transfer"
        rename_app(source_key, app_name, temp_name)
        create_app(target_key, app_name)
        push_code(temp_name, app_name, source_key, target_key)
        set_config_vars(target_key, app_name, config_vars)
        return {"app": app_name, "status": "success"}
    except Exception as e:
        print(f"[ERROR] Failed to transfer {app_name}: {e}")
        return {"app": app_name, "status": "failed"}


def get_app_status(api_key, app_name):
    """Get the status of a Heroku app (running or not)."""
    headers = HEADERS.copy()
    headers["Authorization"] = f"Bearer {api_key}"
    try:
        response = requests.get(f"{HEROKU_API}/apps/{app_name}", headers=headers)
        response.raise_for_status()
        data = response.json()
        return "active" if data.get("released_at") else "inactive"
    except requests.RequestException as e:
        print(f"[ERROR] Failed to get app status for {app_name}: {e}")
        return "unknown"


def delete_app(api_key, app_name):
    """Delete a Heroku app."""
    headers = HEADERS.copy()
    headers["Authorization"] = f"Bearer {api_key}"
    try:
        response = requests.delete(f"{HEROKU_API}/apps/{app_name}", headers=headers)
        response.raise_for_status()
        return {"app": app_name, "status": "deleted"}
    except requests.RequestException as e:
        print(f"[ERROR] Failed to delete {app_name}: {e}")
        return {"app": app_name, "status": "failed"}
