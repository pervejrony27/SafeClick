"""
============================================
EXPLAINER.PY
Generates human-readable reasons explaining
WHY a URL is flagged as phishing
============================================
"""

import config


def get_reasons(url, features, score):
    """
    Generate list of human-readable reasons

    Args:
        url (str): The scanned URL
        features (dict): Extracted features
        score (int): Phishing score 0-100

    Returns:
        list: List of reason strings
    """

    reasons = []

    # ── Check IP Address ──
    if features.get("has_ip_address", 0) == 1:
        reasons.append(
            "🔴 URL contains an IP address instead of a domain name — "
            "legitimate websites rarely use IP addresses"
        )

    # ── Check @ Symbol ──
    if features.get("has_at_symbol", 0) == 1:
        reasons.append(
            "🔴 URL contains '@' symbol — this can be used to redirect "
            "you to a different site than what's shown"
        )

    # ── Check HTTPS ──
    if features.get("has_https", 0) == 0:
        reasons.append(
            "🟡 URL does not use HTTPS — the connection is not encrypted, "
            "which is risky for sensitive data"
        )

    # ── Check URL Length ──
    url_length = features.get("url_length", 0)
    if url_length > 100:
        reasons.append(
            f"🔴 URL is excessively long ({url_length} characters) — "
            "phishing URLs are often very long to hide the real destination"
        )
    elif url_length > 75:
        reasons.append(
            f"🟡 URL is quite long ({url_length} characters) — "
            "longer URLs can be suspicious"
        )

    # ── Check Suspicious Words ──
    suspicious_count = features.get("suspicious_word_count", 0)
    if suspicious_count > 0:
        # Find which words were detected
        url_lower = url.lower()
        found_words = [
            word for word in config.SUSPICIOUS_WORDS
            if word in url_lower
        ]
        found_display = ", ".join(found_words[:5])  # show max 5

        if suspicious_count >= 3:
            reasons.append(
                f"🔴 URL contains {suspicious_count} suspicious keywords: "
                f"{found_display} — this is a strong phishing indicator"
            )
        else:
            reasons.append(
                f"🟡 URL contains suspicious keywords: {found_display}"
            )

    # ── Check Suspicious TLD ──
    if features.get("has_suspicious_tld", 0) == 1:
        # Extract TLD
        domain = url.split("//")[-1].split("/")[0].split(":")[0]
        tld = domain.split(".")[-1] if "." in domain else ""
        reasons.append(
            f"🔴 URL uses suspicious top-level domain (.{tld}) — "
            "this TLD is commonly associated with phishing"
        )

    # ── Check Subdomains ──
    num_subdomains = features.get("num_subdomains", 0)
    if num_subdomains > 3:
        reasons.append(
            f"🔴 URL has too many subdomains ({num_subdomains}) — "
            "excessive subdomains are used to make fake URLs look real"
        )
    elif num_subdomains > 2:
        reasons.append(
            f"🟡 URL has {num_subdomains} subdomains — "
            "more than usual for legitimate websites"
        )

    # ── Check URL Depth ──
    url_depth = features.get("url_depth", 0)
    if url_depth > 5:
        reasons.append(
            f"🟡 URL has deep path structure ({url_depth} levels) — "
            "unusually deep paths can indicate phishing"
        )

    # ── Check Number of Dots ──
    num_dots = features.get("num_dots", 0)
    if num_dots > 5:
        reasons.append(
            f"🟡 URL contains many dots ({num_dots}) — "
            "excessive dots can indicate subdomain abuse"
        )

    # ── Check Hyphens in Domain ──
    num_hyphens = features.get("num_hyphens", 0)
    if num_hyphens > 3:
        reasons.append(
            f"🟡 URL contains many hyphens ({num_hyphens}) — "
            "phishing URLs often use hyphens to mimic real domains"
        )

    # ── Check URL Shortener ──
    if features.get("is_shortened_url", 0) == 1:
        reasons.append(
            "🟡 URL uses a URL shortening service — "
            "shortened URLs can hide the real destination"
        )

    # ── Check Digits in Domain ──
    if features.get("domain_has_digits", 0) == 1:
        reasons.append(
            "🟡 Domain name contains numbers — "
            "legitimate brands rarely have digits in their domain"
        )

    # ── Check Special Character Ratio ──
    special_ratio = features.get("special_char_ratio", 0)
    if special_ratio > 0.3:
        reasons.append(
            "🟡 URL has a high ratio of special characters — "
            "this is unusual for legitimate URLs"
        )

    # ── Check Digit Ratio ──
    digit_ratio = features.get("digit_ratio", 0)
    if digit_ratio > 0.3:
        reasons.append(
            "🟡 URL contains a high percentage of numbers — "
            "this pattern is common in phishing URLs"
        )

    # ── Check Query String ──
    query_length = features.get("query_length", 0)
    if query_length > 50:
        reasons.append(
            f"🟡 URL has a long query string ({query_length} chars) — "
            "may contain encoded tracking or attack data"
        )

    # ── If No Reasons Found (Safe URL) ──
    if not reasons:
        reasons.append(
            "✅ No suspicious patterns detected in this URL"
        )
        reasons.append(
            "✅ URL structure appears normal and legitimate"
        )

        if features.get("has_https", 0) == 1:
            reasons.append(
                "✅ URL uses HTTPS (encrypted connection)"
            )

    return reasons