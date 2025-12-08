// Elements
const sourceInput = document.getElementById("sourceKey");
const targetInput = document.getElementById("targetKey");
const fetchBtn = document.getElementById("fetchApps");
const appsContainer = document.getElementById("appsContainer");
const transferBtn = document.getElementById("transferApps");
const statusContainer = document.getElementById("statusContainer");

// Store fetched apps
let fetchedApps = [];

// Fetch apps from source account
fetchBtn.addEventListener("click", async () => {
    const sourceKey = sourceInput.value.trim();
    if (!sourceKey) {
        alert("Please enter the source API key");
        return;
    }

    appsContainer.innerHTML = "Loading apps...";
    statusContainer.innerHTML = "";

    try {
        const response = await fetch("/apps", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ source_api_key: sourceKey })
        });
        const data = await response.json();

        if (data.error) {
            appsContainer.innerHTML = `<span class="fail">${data.error}</span>`;
            return;
        }

        fetchedApps = data;
        renderApps(fetchedApps);

    } catch (error) {
        appsContainer.innerHTML = `<span class="fail">Error: ${error.message}</span>`;
    }
});

// Render list of apps with checkboxes
function renderApps(apps) {
    if (!apps.length) {
        appsContainer.innerHTML = "No apps found.";
        return;
    }

    appsContainer.innerHTML = apps.map(app => `
        <li>
            <label>
                <input type="checkbox" value="${app}"> ${app}
            </label>
        </li>
    `).join("");
}

// Transfer selected apps
transferBtn.addEventListener("click", async () => {
    const sourceKey = sourceInput.value.trim();
    const targetKey = targetInput.value.trim();
    const selectedApps = Array.from(appsContainer.querySelectorAll("input[type=checkbox]:checked"))
        .map(cb => cb.value);

    if (!sourceKey || !targetKey) {
        alert("Please enter both API keys");
        return;
    }
    if (!selectedApps.length) {
        alert("Select at least one app to transfer");
        return;
    }

    statusContainer.innerHTML = "Transferring apps...";
    
    try {
        const response = await fetch("/transfer", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                source_api_key: sourceKey,
                target_api_key: targetKey,
                apps: selectedApps
            })
        });
        const results = await response.json();

        renderTransferResults(results);

    } catch (error) {
        statusContainer.innerHTML = `<span class="fail">Transfer failed: ${error.message}</span>`;
    }
});

// Render transfer results
function renderTransferResults(results) {
    statusContainer.innerHTML = results.map(res => {
        const statusClass = res.status === "success" ? "success" : "fail";
        return `<div class="${statusClass}">${res.app}: ${res.status}${res.error ? " - " + res.error : ""}</div>`;
    }).join("");
}
