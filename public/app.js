const demoQuestions = [
    "How many patients do we have?",
    "List all doctors and their specializations",
    "Show me appointments for last month",
    "Which doctor has the most appointments?",
    "What is the total revenue?",
    "Show revenue by doctor",
    "How many cancelled appointments last quarter?",
    "Top 5 patients by spending",
    "Average treatment cost by specialization",
    "Show monthly appointment count for the past 6 months",
    "Which city has the most patients?",
    "List patients who visited more than 3 times",
    "Show unpaid invoices",
    "What percentage of appointments are no-shows?",
    "Show the busiest day of the week for appointments",
    "Revenue trend by month",
    "Average appointment duration by doctor",
    "List patients with overdue invoices",
    "Compare revenue between departments",
    "Show patient registration trend by month"
];

// UI DOM Variables
const modeBatch = document.getElementById("modeBatch");
const modeCustom = document.getElementById("modeCustom");
const batchView = document.getElementById("batchView");
const customView = document.getElementById("customView");
const rateLimitGroup = document.getElementById("rateLimitGroup");
const startBatchBtn = document.getElementById("startBatchBtn");

const modelSelect = document.getElementById("modelSelect");
const rateLimitSlider = document.getElementById("rateLimitSlider");
const rateLimitValue = document.getElementById("rateLimitValue");

// Batch UI
const batchStatusIndicator = document.getElementById("batchStatusIndicator");
const batchStatusText = document.getElementById("batchStatusText");
const batchProgress = document.getElementById("batchProgress");
const progressText = document.getElementById("progressText");
const batchTableBody = document.getElementById("batchTableBody");
const latestDataBox = document.getElementById("latestDataBox");
const latestDataContainer = document.getElementById("latestDataContainer");
const haltBtn = document.getElementById("haltBtn");

// Custom UI
const chatHistory = document.getElementById("chatHistory");
const customPrompt = document.getElementById("customPrompt");
const sendCustomBtn = document.getElementById("sendCustomBtn");

// SaaS UI
const shutdownBtn = document.getElementById("shutdownBtn");
const dbFileInput = document.getElementById("dbFileInput");
const uploadLabel = document.getElementById("uploadLabel");
const activeDbName = document.getElementById("activeDbName");
const schemaList = document.getElementById("schemaList");
const schemaCount = document.getElementById("schemaCount");

let isBatchRunning = false;
let isBatchCancelled = false; // Halt functionality

// Feature: Load DB Schema
async function loadSchema() {
    try {
        const res = await fetch("/api/schema");
        const data = await res.json();
        if(data && data.tables) {
            schemaList.innerHTML = "";
            schemaCount.innerText = `(${data.tables.length} Tables)`;
            activeDbName.innerText = data.db_name;
            
            data.tables.forEach(t => {
                let dom = `<div class="schema-table"><strong>${t.name}</strong><div class="schema-cols">${t.columns.join(", ")}</div></div>`;
                schemaList.innerHTML += dom;
            });
        }
    } catch(e) {
        console.error("Failed to load schema", e);
    }
}
// Init schema load
loadSchema();

// Feature: DB Upload
dbFileInput.addEventListener("change", async (e) => {
    const file = e.target.files[0];
    if(!file) return;
    
    uploadLabel.innerText = "Uploading...";
    const formData = new FormData();
    formData.append("file", file);
    
    try {
        const res = await fetch("/api/upload_db", { method: "POST", body: formData });
        if(res.ok) {
            uploadLabel.innerText = "Upload Complete!";
            setTimeout(() => uploadLabel.innerText = "Drag & Drop or Click to Upload .DB", 3000);
            loadSchema(); // regenerate Explorer
        } else {
            uploadLabel.innerText = "Error uploading.";
        }
    } catch(err) {
        uploadLabel.innerText = "Upload Failed.";
    }
});

// Feature: Shutdown
shutdownBtn.addEventListener("click", () => {
    if(confirm("Are you sure you want to shut down the NeuroSQL backend? You will need to restart from the terminal.")) {
        fetch("/shutdown", { method: "POST" });
        document.body.innerHTML = "<h2 style='text-align:center; margin-top:100px;'>Backend Server Offline</h2><p style='text-align:center'>You may close this tab.</p>";
    }
});

// Event Listeners
rateLimitSlider.addEventListener("input", (e) => {
    rateLimitValue.innerText = e.target.value;
});

modeBatch.addEventListener("click", () => {
    if (isBatchRunning) return; // locked
    modeBatch.classList.add("active");
    modeCustom.classList.remove("active");
    batchView.classList.add("active");
    customView.classList.remove("active");
    
    // Show components meant for batch
    rateLimitGroup.style.display = "flex";
    if(!isBatchRunning) startBatchBtn.style.display = "block";
});

modeCustom.addEventListener("click", () => {
    if (isBatchRunning) return; // locked
    modeCustom.classList.add("active");
    modeBatch.classList.remove("active");
    customView.classList.add("active");
    batchView.classList.remove("active");
    
    // Hide components not meant for interactive mode
    rateLimitGroup.style.display = "none";
    startBatchBtn.style.display = "none";
});

// API Caller
async function performQuery(question, modelChoice) {
    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: question, model_choice: modelChoice })
        });
        return await response.json();
    } catch (e) {
        return { error: e.message };
    }
}

function generateHTMLTable(columns, rows) {
    if (!columns || !rows || rows.length === 0) return "<p style='color: var(--text-secondary);'>No datatable returned.</p>";
    
    let html = "<table class='data-table'><thead><tr>";
    columns.forEach(c => { html += `<th>${c}</th>`; });
    html += "</tr></thead><tbody>";
    
    rows.slice(0, 15).forEach(row => {
        html += "<tr>";
        row.forEach(cell => { html += `<td>${cell === null ? 'NULL' : cell}</td>`; });
        html += "</tr>";
    });
    
    if (rows.length > 15) {
        html += `<tr><td colspan="${columns.length}"><em>... and ${rows.length - 15} more rows</em></td></tr>`;
    }
    
    html += "</tbody></table>";
    return html;
}

// BATCH RUN LOGIC
haltBtn.addEventListener("click", () => {
    if(isBatchRunning) {
        isBatchCancelled = true;
        haltBtn.innerText = "Halting...";
        batchStatusText.innerText = "Interrupted by user.";
    }
});

startBatchBtn.addEventListener("click", async () => {
    if (isBatchRunning) return;
    
    // Reset UI
    isBatchRunning = true;
    isBatchCancelled = false;
    startBatchBtn.style.display = "none";
    haltBtn.style.display = "block";
    haltBtn.innerText = "Halt Execution";
    modelSelect.disabled = true;
    batchTableBody.innerHTML = "";
    latestDataBox.style.display = "none";
    
    batchStatusIndicator.className = "pulse-dot running";
    batchStatusText.innerText = "Automated Sequence Running...";
    
    const delay = parseInt(rateLimitSlider.value) * 1000;
    const model = modelSelect.value;
    
    for (let i = 0; i < demoQuestions.length; i++) {
        if(isBatchCancelled) {
            batchStatusIndicator.className = "pulse-dot error";
            batchStatusText.innerText = "Sequence Halted Early.";
            break;
        }
        // UI pre-update pending row
        const q = demoQuestions[i];
        
        batchProgress.style.width = `${((i) / demoQuestions.length) * 100}%`;
        progressText.innerText = `${i} / 20 Executed`;
        
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${i + 1}</td>
            <td>${q}</td>
            <td><span class="status-badge pending">Querying AI...</span></td>
            <td><code class="sql-blob">...</code></td>
        `;
        batchTableBody.prepend(tr);
        
        // Execute request
        const res = await performQuery(q, model);
        
        let statusBadge = "";
        if (res.error) {
            statusBadge = `<span class="status-badge error">Failed: ${res.error}</span>`;
        } else if (res.rows) {
            statusBadge = `<span class="status-badge success">Success (${res.rows.length} rows)</span>`;
        } else {
            statusBadge = `<span class="status-badge success">Success (0 rows)</span>`;
        }
        
        const generatedSQL = res.sql_query || "None";
        
        tr.innerHTML = `
            <td>${i + 1}</td>
            <td>${q}</td>
            <td>${statusBadge}</td>
            <td><code class="sql-blob">${generatedSQL.trim()}</code></td>
        `;
        
        // Populate specific dataview
        if (!res.error && res.rows && res.rows.length > 0) {
            latestDataBox.style.display = "block";
            latestDataBox.innerHTML = `<h3>Data Instance #${i+1}: ${q}</h3><div class="data-table-wrapper">${generateHTMLTable(res.columns, res.rows)}</div>`;
        }
        
        batchProgress.style.width = `${((i + 1) / demoQuestions.length) * 100}%`;
        progressText.innerText = `${i + 1} / 20 Executed`;
        
        if (i < demoQuestions.length - 1 && delay > 0 && !isBatchCancelled) {
            batchStatusText.innerText = `Rate Limit Cooldown... (${delay/1000}s)`;
            await new Promise(r => setTimeout(r, delay));
            if(!isBatchCancelled) batchStatusText.innerText = "Automated Sequence Running...";
        }
    }
    
    isBatchRunning = false;
    startBatchBtn.style.display = "block";
    haltBtn.style.display = "none";
    modelSelect.disabled = false;
    
    if(!isBatchCancelled) {
        batchStatusIndicator.className = "pulse-dot complete";
        batchStatusText.innerText = "Sequence Complete. All Targets Queried.";
    }
});

// INTERACTIVE CHAT LOGIC
async function sendChatMessage() {
    const text = customPrompt.value.trim();
    if (!text) return;
    
    const model = modelSelect.value;
    
    // append user text
    const userDiv = document.createElement("div");
    userDiv.className = "chat-message user";
    userDiv.innerHTML = `<div class="bubble">${text}</div>`;
    chatHistory.appendChild(userDiv);
    
    customPrompt.value = "";
    customPrompt.disabled = true;
    sendCustomBtn.disabled = true;
    
    // append pending system block
    const sysDiv = document.createElement("div");
    sysDiv.className = "chat-message system";
    sysDiv.innerHTML = `<div class="bubble"><span class="pulse-dot running" style="display:inline-block; margin-right:8px;"></span> Analyzing and querying databank...</div>`;
    chatHistory.appendChild(sysDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;
    
    const res = await performQuery(text, model);
    
    let sysOutput = "";
    if (res.error) {
        sysOutput = `<strong>Operation Failed</strong><div style="color:var(--error); margin-top:8px;">${res.error}</div>`;
    } else {
        sysOutput = `<strong>Executed Query:</strong><div class="sql-output">${res.sql_query}</div>`;
        if (res.rows) {
            sysOutput += `<div class="data-table-wrapper">${generateHTMLTable(res.columns, res.rows)}</div>`;
        } else {
            sysOutput += `<div style="margin-top:10px;">Operation Succeeded (No raw data returned).</div>`;
        }
    }
    
    sysDiv.innerHTML = `<div class="bubble">${sysOutput}</div>`;
    chatHistory.scrollTop = chatHistory.scrollHeight;
    
    customPrompt.disabled = false;
    sendCustomBtn.disabled = false;
    customPrompt.focus();
}

sendCustomBtn.addEventListener("click", sendChatMessage);
customPrompt.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendChatMessage();
});
