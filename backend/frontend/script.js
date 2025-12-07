
let selectedApps = [];

function fetchApps() {
    const sourceKey = document.getElementById("sourceKey").value;
    fetch("/apps", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ source_api_key: sourceKey })
    })
    .then(res => res.json())
    .then(data => {
        const appsList = document.getElementById("appsList");
        appsList.innerHTML = "";
        selectedApps = [];
        data.forEach(app => {
            const div = document.createElement("div");
            div.innerHTML = `<input type="checkbox" value="${app}" onchange="toggleApp(this)"> ${app}`;
            appsList.appendChild(div);
        });
    })
    .catch(err => alert("Failed to fetch apps"));
}

function toggleApp(checkbox) {
    if (checkbox.checked) selectedApps.push(checkbox.value);
    else selectedApps = selectedApps.filter(a => a !== checkbox.value);
}

function transferApps() {
    const sourceKey = document.getElementById("sourceKey").value;
    const targetKey = document.getElementById("targetKey").value;
    fetch("/transfer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ source_api_key: sourceKey, target_api_key: targetKey, apps: selectedApps })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("logs").textContent = JSON.stringify(data, null, 2);
    })
    .catch(err => alert("Transfer failed"));
              }
