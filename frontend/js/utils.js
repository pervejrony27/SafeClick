/* ============================================
   UTILS.JS — Helper / Utility Functions
   ============================================ */

/**
 * Get color based on risk level
 * @param {string} riskLevel - "SAFE", "SUSPICIOUS", or "PHISHING"
 * @returns {string} - CSS color code
 */
function getRiskColor(riskLevel) {

    switch (riskLevel) {
        case "SAFE":
            return "#27ae60";       // Green
        case "SUSPICIOUS":
            return "#f39c12";       // Orange
        case "PHISHING":
            return "#e74c3c";       // Red
        default:
            return "#888888";       // Gray
    }
}


/**
 * Get CSS class based on risk level
 * @param {string} riskLevel 
 * @returns {string} - CSS class name
 */
function getRiskClass(riskLevel) {

    switch (riskLevel) {
        case "SAFE":
            return "safe";
        case "SUSPICIOUS":
            return "suspicious";
        case "PHISHING":
            return "phishing";
        default:
            return "safe";
    }
}


/**
 * Get description text based on risk level
 * @param {string} riskLevel 
 * @returns {string}
 */
function getRiskDescription(riskLevel) {

    switch (riskLevel) {
        case "SAFE":
            return "This URL appears to be safe. No major phishing indicators were detected.";
        case "SUSPICIOUS":
            return "This URL shows some suspicious patterns. Proceed with caution and verify the source.";
        case "PHISHING":
            return "⚠️ This URL is highly likely to be a phishing link. Do NOT enter any personal information!";
        default:
            return "";
    }
}


/**
 * Get emoji icon based on risk level
 * @param {string} riskLevel 
 * @returns {string}
 */
function getRiskEmoji(riskLevel) {

    switch (riskLevel) {
        case "SAFE":
            return "✅";
        case "SUSPICIOUS":
            return "⚡";
        case "PHISHING":
            return "🚨";
        default:
            return "❓";
    }
}


/**
 * Determine reason severity class from reason text
 * @param {string} reason 
 * @returns {string} - CSS class
 */
function getReasonClass(reason) {

    if (reason.includes("🔴") || reason.includes("high") || reason.includes("phishing")) {
        return "reason-danger";
    } else if (reason.includes("🟡") || reason.includes("suspicious") || reason.includes("caution")) {
        return "reason-warning";
    } else if (reason.includes("✅") || reason.includes("safe") || reason.includes("No suspicious")) {
        return "reason-safe";
    }
    return "";
}


/**
 * Basic URL format validation (client-side)
 * @param {string} url 
 * @returns {boolean}
 */
function isValidURLFormat(url) {

    // Check if it at least looks like a URL
    if (url.length < 4) return false;

    // Must contain at least one dot or be an IP-based URL
    if (!url.includes(".") && !url.includes("://")) return false;

    return true;
}


/**
 * Fill example URL into the scanner input
 * Called from onclick in index.html
 * @param {string} url 
 */
function fillExample(url) {
    
    const input = document.getElementById("url-input");
    if (input) {
        input.value = url;
        input.focus();
    }
}