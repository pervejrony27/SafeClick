/* ============================================
   SCANNER.JS — Scanner Form Logic
   This file handles the scan button click
   and coordinates everything
   ============================================ */

// ── Get DOM Elements ──
const urlInput = document.getElementById("url-input");
const scanBtn = document.getElementById("scan-btn");
const loadingDiv = document.getElementById("loading");
const resultsDiv = document.getElementById("results");
const errorMsgDiv = document.getElementById("error-msg");

// ── Event Listeners ──

// Click scan button
scanBtn.addEventListener("click", handleScan);

// Press Enter key in input
urlInput.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        handleScan();
    }
});

// Clear error when user starts typing
urlInput.addEventListener("input", function () {
    hideError();
});


/**
 * Main scan handler — called when user clicks Scan
 */
async function handleScan() {

    // Get the URL from input
    const url = urlInput.value.trim();

    // Reset previous state
    hideError();
    hideResults();

    // ── Validate Input ──
    if (!url) {
        showError("⚠️ Please enter a URL to scan!");
        return;
    }

    if (!isValidURLFormat(url)) {
        showError("⚠️ Please enter a valid URL format (e.g., http://example.com)");
        return;
    }

    // ── Show Loading State ──
    showLoading();

    try {
        // ⭐ Call Backend API
        const result = await scanURL(url);

        // ── Hide Loading ──
        hideLoading();

        // ── Display Results ──
        if (result.success) {
            displayResults(result);
        } else {
            showError("❌ " + (result.error || "Unknown error occurred"));
        }

    } catch (error) {
        // ── Handle Errors ──
        hideLoading();
        showError("❌ " + error.message);
    }
}


/* ── Helper Functions ── */

function showLoading() {
    loadingDiv.style.display = "block";
    scanBtn.disabled = true;
    scanBtn.textContent = "⏳ Scanning...";
}

function hideLoading() {
    loadingDiv.style.display = "none";
    scanBtn.disabled = false;
    scanBtn.textContent = "🔍 Scan Now";
}

function showError(message) {
    errorMsgDiv.textContent = message;
    errorMsgDiv.style.display = "block";
}

function hideError() {
    errorMsgDiv.style.display = "none";
    errorMsgDiv.textContent = "";
}

function hideResults() {
    resultsDiv.style.display = "none";
}


/* ── Check Backend on Page Load ── */

window.addEventListener("load", async function () {

    const isBackendRunning = await checkBackendHealth();

    if (!isBackendRunning) {
        console.warn("⚠️ Backend is not running on " + API_BASE_URL);
        console.warn("Start the backend: cd backend → python run.py");
    } else {
        console.log("✅ Backend is connected at " + API_BASE_URL);
    }
});