"""
============================================
ROUTES.PY — API Endpoints
Handles all incoming requests from frontend
============================================
"""

from flask import Blueprint, request, jsonify
from ml.feature_extractor import extract_features
from ml.predict import get_prediction
from ml.explainer import get_reasons
import config

# Create Blueprint
scanner_bp = Blueprint("scanner", __name__)


# ──────────────────────────────────────────
# ENDPOINT: POST /api/scan
# This is what the frontend calls
# ──────────────────────────────────────────
@scanner_bp.route("/api/scan", methods=["POST"])
def scan_url():
    """
    Scan a URL for phishing

    Request Body (JSON):
        { "url": "http://example.com" }

    Response (JSON):
        {
            "success": true,
            "url": "http://example.com",
            "phishing_score": 85,
            "risk_level": "PHISHING",
            "reasons": ["reason 1", "reason 2"]
        }
    """

    # ── Step 1: Get request data ──
    data = request.get_json()

    # Validate: check if JSON body exists
    if not data:
        return jsonify({
            "success": False,
            "error": "No data provided. Send JSON with 'url' field."
        }), 400

    # Validate: check if 'url' field exists
    if "url" not in data:
        return jsonify({
            "success": False,
            "error": "Missing 'url' field in request body."
        }), 400

    url = data["url"].strip()

    # Validate: check if URL is not empty
    if not url:
        return jsonify({
            "success": False,
            "error": "URL cannot be empty."
        }), 400

    # Validate: basic URL check
    if len(url) < 4:
        return jsonify({
            "success": False,
            "error": "URL is too short to analyze."
        }), 400

    try:
        # ── Step 2: Extract features from URL ──
        features = extract_features(url)

        # ── Step 3: Get phishing score (0-100) ──
        score = get_prediction(features)

        # ── Step 4: Determine risk level ──
        if score >= config.PHISHING_THRESHOLD:
            risk_level = "PHISHING"
        elif score >= config.SUSPICIOUS_THRESHOLD:
            risk_level = "SUSPICIOUS"
        else:
            risk_level = "SAFE"

        # ── Step 5: Get human-readable reasons ──
        reasons = get_reasons(url, features, score)

        # ── Step 6: Return response ──
        return jsonify({
            "success": True,
            "url": url,
            "phishing_score": score,
            "risk_level": risk_level,
            "reasons": reasons,
            "features_analyzed": len(features),
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Analysis failed: {str(e)}"
        }), 500


# ──────────────────────────────────────────
# ENDPOINT: GET /api/health
# Check if API is working
# ──────────────────────────────────────────
@scanner_bp.route("/api/health", methods=["GET"])
def health():
    """Check if the API and model are working"""

    import os
    model_loaded = os.path.exists(config.MODEL_PATH)

    return jsonify({
        "status": "healthy",
        "model_loaded": model_loaded,
        "message": " SafeClick  API is ready!"
    })


# ──────────────────────────────────────────
# ENDPOINT: POST /api/scan/batch
# Scan multiple URLs at once (bonus feature)
# ──────────────────────────────────────────
@scanner_bp.route("/api/scan/batch", methods=["POST"])
def scan_batch():
    """
    Scan multiple URLs at once

    Request Body:
        { "urls": ["url1", "url2", "url3"] }
    """

    data = request.get_json()

    if not data or "urls" not in data:
        return jsonify({
            "success": False,
            "error": "Provide a list of URLs in 'urls' field."
        }), 400

    urls = data["urls"]

    if not isinstance(urls, list) or len(urls) == 0:
        return jsonify({
            "success": False,
            "error": "'urls' must be a non-empty list."
        }), 400

    # Limit batch size
    if len(urls) > 10:
        return jsonify({
            "success": False,
            "error": "Maximum 10 URLs per batch."
        }), 400

    results = []

    for url in urls:
        try:
            url = url.strip()
            features = extract_features(url)
            score = get_prediction(features)

            if score >= config.PHISHING_THRESHOLD:
                risk_level = "PHISHING"
            elif score >= config.SUSPICIOUS_THRESHOLD:
                risk_level = "SUSPICIOUS"
            else:
                risk_level = "SAFE"

            reasons = get_reasons(url, features, score)

            results.append({
                "url": url,
                "phishing_score": score,
                "risk_level": risk_level,
                "reasons": reasons,
            })

        except Exception as e:
            results.append({
                "url": url,
                "error": str(e),
            })

    return jsonify({
        "success": True,
        "count": len(results),
        "results": results,
    })