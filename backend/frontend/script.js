let appsList = [];

document.getElementById("fetchApps").addEventListener("click", async () => {
    const sourceKey = document.getElementById("sourceKey").value.trim();
    if (!sourceKey) return alert("Enter Source API Key");

    try {
        const res = await fetch("/apps", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ source_api_key: sourceKey })
        });
        const apps = await res.json();
        appsList = apps;
        displayApps(apps);
        updateSummary();
    } catch (err) {
        alert("Failed to fetch apps: " + err);
    }
});

function displayApps(apps) {
    const container = document.getElementById("appsContainer");
    container.innerHTML = "";
    apps.forEach(appName => {
        const card = document.createElement("div");
        card.classList.add("app-card");
        card.innerHTML = `
            <input type="checkbox" id="check-${appName}" />
            <h3>${appName}</h3>
            <div>Status: <span id="status-${appName}">Fetching...</span></div>
        `;
        container.appendChild(card);
        fetchAppStatus(appName);
    });
}

function updateSummary() {
    const total = appsList.length;
    let running = 0, stopped = 0;

    appsList.forEach(appName => {
        const statusEl = document.getElementById(`status-${appName}`);
        if (statusEl) {
            if (statusEl.innerText === "Running") running++;
            else if (statusEl.innerText === "Stopped") stopped++;
        }
    });

    document.getElementById("totalApps").innerText = total;
    document.getElementById("runningApps").innerText = running;
    document.getElementById("stoppedApps").innerText = stopped;
}

async function fetchAppStatus(appName) {
    const sourceKey = document.getElementById("sourceKey").value.trim();
    try {
        const res = await fetch("/status", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ app_name: appName, api_key: sourceKey })
        });
        const data = await res.json();
        const statusEl = document.getElementById(`status-${appName}`);
        if (data.running) {
            statusEl.innerText = "Running";
            statusEl.classList.add("status-running");
            statusEl.classList.remove("status-stopped");
        } else {
            statusEl.innerText = "Stopped";
            statusEl.classList.add("status-stopped");
            statusEl.classList.remove("status-running");
        }
        updateSummary();
    } catch {
        const statusEl = document.getElementById(`status-${appName}`);
        statusEl.innerText = "Error";
        statusEl.classList.add("status-stopped");
        updateSummary();
    }
}

document.getElementById("transferSelected").addEventListener("click", async () => {
    const selectedApps = appsList.filter(appName => document.getElementById(`check-${appName}`).checked);
    const sourceKey = document.getElementById("sourceKey").value.trim();
    const targetKey = document.getElementById("targetKey").value.trim();
    if (!sourceKey || !targetKey || selectedApps.length === 0) return alert("Select apps and enter both API keys");

    const res = await fetch("/transfer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ source_api_key: sourceKey, target_api_key: targetKey, apps: selectedApps })
    });

    const results = await res.json();
    document.getElementById("results").innerText = JSON.stringify(results, null, 2);
});

document.getElementById("deleteSelected").addEventListener("click", async () => {
    const selectedApps = appsList.filter(appName => document.getElementById(`check-${appName}`).checked);
    const sourceKey = document.getElementById("sourceKey").value.trim();
    if (!sourceKey || selectedApps.length === 0) return alert("Select apps to delete and enter API key");

    const res = await fetch("/delete", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ api_key: sourceKey, apps: selectedApps })
    });

    const results = await res.json();
    document.getElementById("results").innerText = JSON.stringify(results, null, 2);
    // Refresh list after deletion
    document.getElementById("fetchApps").click();
});
