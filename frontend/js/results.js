/* ============================================
   RESULTS.JS — Display Scan Results
   ============================================ */

/**
 * Display the scan results on the page
 * @param {object} result - Response from backend API
 * result = {
 *   url: "...",
 *   phishing_score: 85,
 *   risk_level: "PHISHING",
 *   reasons: ["reason1", "reason2"]
 * }
 */
function displayResults(result) {

    // Get elements
    const resultsSection = document.getElementById("results");
    const scannedUrlText = document.getElementById("scanned-url-text");
    const scoreNumber = document.getElementById("score-number");
    const scoreCircle = document.getElementById("score-circle");
    const riskBadge = document.getElementById("risk-badge");
    const riskDescription = document.getElementById("risk-description");
    const reasonsList = document.getElementById("reasons-list");

    // Show results section
    resultsSection.style.display = "block";

    // Scroll to results smoothly
    resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });

    // ── Update Scanned URL ──
    scannedUrlText.textContent = result.url;

    // ── Animate Score Number (count up effect) ──
    animateScore(scoreNumber, result.phishing_score);

    // ── Update Score Circle ──
    const riskClass = getRiskClass(result.risk_level);
    scoreCircle.className = "score-circle " + riskClass;

    // ── Update Risk Badge ──
    const emoji = getRiskEmoji(result.risk_level);
    riskBadge.className = "risk-badge " + riskClass;
    riskBadge.textContent = emoji + " " + result.risk_level;

    // ── Update Risk Description ──
    riskDescription.textContent = getRiskDescription(result.risk_level);

    // ── Update Reasons List ──
    reasonsList.innerHTML = "";

    if (result.reasons && result.reasons.length > 0) {
        result.reasons.forEach(function (reason) {
            const li = document.createElement("li");
            li.textContent = reason;

            // Add color class based on reason severity
            const reasonClass = getReasonClass(reason);
            if (reasonClass) {
                li.classList.add(reasonClass);
            }

            reasonsList.appendChild(li);
        });
    } else {
        const li = document.createElement("li");
        li.textContent = "✅ No suspicious patterns detected.";
        li.classList.add("reason-safe");
        reasonsList.appendChild(li);
    }
}


/**
 * Animate the score number (count up from 0)
 * @param {HTMLElement} element - The score number element
 * @param {number} target - Target score value
 */
function animateScore(element, target) {

    let current = 0;
    const duration = 1000;  // 1 second
    const steps = 50;
    const increment = target / steps;
    const stepTime = duration / steps;

    const timer = setInterval(function () {
        current += increment;

        if (current >= target) {
            current = target;
            clearInterval(timer);
        }

        element.textContent = Math.round(current);
    }, stepTime);
}


/**
 * Reset the scanner to initial state
 * Called from "Scan Another URL" button
 */
function resetScanner() {

    // Hide results
    document.getElementById("results").style.display = "none";

    // Clear input
    const input = document.getElementById("url-input");
    input.value = "";
    input.focus();

    // Scroll to top
    window.scrollTo({ top: 0, behavior: "smooth" });
}