import os
import subprocess
import requests

HEROKU_API = "https://api.heroku.com"
HEADERS = {"Accept": "application/vnd.heroku+json; version=3"}

# Get all apps for a user
def get_apps(api_key):
    headers = HEADERS.copy()
    headers["Authorization"] = f"Bearer {api_key}"
    response = requests.get(f"{HEROKU_API}/apps", headers=headers)
    response.raise_for_status()
    return response.json()

# Get config vars of an app
def get_config_vars(api_key, app_name):
    headers = HEADERS.copy()
    headers["Authorization"] = f"Bearer {api_key}"
    response = requests.get(f"{HEROKU_API}/apps/{app_name}/config-vars", headers=headers)
    response.raise_for_status()
    return response.json()

# Rename an app
def rename_app(api_key, old_name, new_name):
    headers = HEADERS.copy()
    headers["Authorization"] = f"Bearer {api_key}"
    response = requests.patch(f"{HEROKU_API}/apps/{old_name}", headers=headers, json={"name": new_name})
    response.raise_for_status()
    return response.json()

# Create a new app
def create_app(api_key, app_name):
    headers = HEADERS.copy()
    headers["Authorization"] = f"Bearer {api_key}"
    response = requests.post(f"{HEROKU_API}/apps", headers=headers, json={"name": app_name})
    response.raise_for_status()
    return response.json()

# Push code from source app to target app
def push_code(source_app_name, target_app_name, source_key, target_key):
    subprocess.run(["git", "clone", f"https://heroku:{source_key}@git.heroku.com/{source_app_name}.git"], check=True)
    os.chdir(source_app_name)
    subprocess.run(["git", "remote", "add", "target", f"https://heroku:{target_key}@git.heroku.com/{target_app_name}.git"], check=True)
    subprocess.run(["git", "push", "target", "main", "--force"], check=True)
    os.chdir("..")
    subprocess.run(["rm", "-rf", source_app_name], check=True)

# Set config vars for an app
def set_config_vars(api_key, app_name, config_vars):
    headers = HEADERS.copy()
    headers["Authorization"] = f"Bearer {api_key}"
    response = requests.patch(f"{HEROKU_API}/apps/{app_name}/config-vars", headers=headers, json=config_vars)
    response.raise_for_status()
    return response.json()

# Transfer an app from one account to another
def transfer_app(app_name, source_key, target_key):
    config_vars = get_config_vars(source_key, app_name)
    temp_name = app_name + "-old-transfer"
    rename_app(source_key, app_name, temp_name)
    create_app(target_key, app_name)
    push_code(temp_name, app_name, source_key, target_key)
    set_config_vars(target_key, app_name, config_vars)
    return {"app": app_name, "status": "success"}

# Get the current status of an app
def get_app_status(api_key, app_name):
    headers = HEADERS.copy()
    headers["Authorization"] = f"Bearer {api_key}"
    try:
        response = requests.get(f"{HEROKU_API}/apps/{app_name}", headers=headers)
        response.raise_for_status()
        return {"app": app_name, "status": "running"}
    except requests.exceptions.HTTPError:
        return {"app": app_name, "status": "not running"}

# Delete an app
def delete_app(api_key, app_name):
    headers = HEADERS.copy()
    headers["Authorization"] = f"Bearer {api_key}"
    response = requests.delete(f"{HEROKU_API}/apps/{app_name}", headers=headers)
    if response.status_code == 202:
        return {"app": app_name, "status": "deleted"}
    else:
        return {"app": app_name, "status": "failed", "error": response.text}
