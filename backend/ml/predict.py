"""
============================================
PREDICT.PY
Loads trained model and makes predictions
Falls back to rule-based scoring if no model
============================================
"""

import os
import numpy as np
import joblib
import config
from ml.feature_extractor import get_feature_values_as_list


def get_prediction(features):
    """
    Predict phishing score for given features

    Args:
        features (dict): Extracted URL features

    Returns:
        int: Phishing score between 0-100
             0 = definitely safe
             100 = definitely phishing
    """

    # Check if trained model exists
    if os.path.exists(config.MODEL_PATH) and os.path.exists(config.SCALER_PATH):
        score = _predict_with_model(features)
    else:
        # No trained model yet — use rule-based scoring
        print("⚠️ No trained model found. Using rule-based scoring.")
        print(f"   Train a model by running: python -m ml.train_model")
        score = _predict_with_rules(features)

    return score


def _predict_with_model(features):
    """
    Predict using the trained ML model

    Args:
        features (dict): URL features

    Returns:
        int: Score 0-100
    """

    try:
        # Load model and scaler
        model = joblib.load(config.MODEL_PATH)
        scaler = joblib.load(config.SCALER_PATH)

        # Convert features dict to ordered list
        feature_values = get_feature_values_as_list(features)

        # Convert to numpy array and reshape for single prediction
        feature_array = np.array(feature_values).reshape(1, -1)

        # Scale features
        feature_scaled = scaler.transform(feature_array)

        # Get prediction probability
        # predict_proba returns [[prob_safe, prob_phishing]]
        probabilities = model.predict_proba(feature_scaled)
        phishing_probability = probabilities[0][1]  # probability of phishing

        # Convert to 0-100 score
        score = int(round(phishing_probability * 100))

        # Clamp between 0 and 100
        score = max(0, min(100, score))

        return score

    except Exception as e:
        print(f"❌ Model prediction failed: {e}")
        print("   Falling back to rule-based scoring.")
        return _predict_with_rules(features)


def _predict_with_rules(features):
    """
    Rule-based scoring (fallback when model is not trained yet)

    This gives reasonable results based on known phishing patterns.
    Replace this with the ML model after training.

    Args:
        features (dict): URL features

    Returns:
        int: Score 0-100
    """

    score = 0

    # ── High Risk Indicators (add more points) ──

    # IP address in URL (+25)
    if features.get("has_ip_address", 0) == 1:
        score += 25

    # @ symbol in URL (+20)
    if features.get("has_at_symbol", 0) == 1:
        score += 20

    # Suspicious TLD (+20)
    if features.get("has_suspicious_tld", 0) == 1:
        score += 20

    # Many suspicious words (+5 per word, max 20)
    suspicious_count = features.get("suspicious_word_count", 0)
    score += min(suspicious_count * 5, 20)

    # ── Medium Risk Indicators ──

    # No HTTPS (+10)
    if features.get("has_https", 0) == 0:
        score += 10

    # Very long URL (+10-15)
    url_length = features.get("url_length", 0)
    if url_length > 100:
        score += 15
    elif url_length > 75:
        score += 10
    elif url_length > 54:
        score += 5

    # Many subdomains (+5-15)
    num_subdomains = features.get("num_subdomains", 0)
    if num_subdomains > 3:
        score += 15
    elif num_subdomains > 2:
        score += 10
    elif num_subdomains > 1:
        score += 5

    # Many dots (+5-10)
    num_dots = features.get("num_dots", 0)
    if num_dots > 5:
        score += 10
    elif num_dots > 3:
        score += 5

    # ── Low Risk Indicators ──

    # URL shortener (+8)
    if features.get("is_shortened_url", 0) == 1:
        score += 8

    # Digits in domain (+5)
    if features.get("domain_has_digits", 0) == 1:
        score += 5

    # Many hyphens (+5)
    if features.get("num_hyphens", 0) > 3:
        score += 5

    # Deep URL path (+5)
    if features.get("url_depth", 0) > 5:
        score += 5

    # High special character ratio (+5)
    if features.get("special_char_ratio", 0) > 0.3:
        score += 5

    # High digit ratio (+5)
    if features.get("digit_ratio", 0) > 0.3:
        score += 5

    # ── Safe Indicators (subtract points) ──

    # HTTPS (-5)
    if features.get("has_https", 0) == 1:
        score -= 5

    # Short, clean URL (-5)
    if url_length < 30 and num_dots <= 2:
        score -= 5

    # Clamp between 0 and 100
    score = max(0, min(100, score))

    return score