/* ============================================
   API.JS — Connects Frontend to Backend
   ⭐ THIS IS THE BRIDGE FILE
   ============================================ */

// Backend server URL (change when deploying)
const API_BASE_URL = "http://localhost:5000";

/**
 * Sends a URL to the backend for phishing analysis
 * 
 * @param {string} url - The URL to scan
 * @returns {Promise<object>} - Scan result from backend
 * 
 * Expected response:
 * {
 *   success: true,
 *   url: "http://evil-site.com",
 *   phishing_score: 85,
 *   risk_level: "PHISHING",
 *   reasons: ["reason 1", "reason 2", ...]
 * }
 */
async function scanURL(url) {

    try {
        // Send POST request to backend
        const response = await fetch(`${API_BASE_URL}/api/scan`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ url: url }),
        });

        // Parse JSON response
        const data = await response.json();

        // Check if backend returned an error
        if (!response.ok) {
            throw new Error(data.error || "Failed to scan URL");
        }

        // Return successful result
        return data;

    } catch (error) {

        // Check if backend is not running
        if (error.message === "Failed to fetch") {
            throw new Error(
                "Cannot connect to server. Make sure the backend is running on " + 
                API_BASE_URL
            );
        }

        // Re-throw other errors
        throw error;
    }
}


/**
 * Check if backend server is running
 * @returns {Promise<boolean>}
 */
async function checkBackendHealth() {

    try {
        const response = await fetch(`${API_BASE_URL}/`, {
            method: "GET",
        });
        return response.ok;
    } catch (error) {
        return false;
    }
}