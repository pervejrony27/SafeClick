"""
============================================
FEATURE_EXTRACTOR.PY
Extracts 30+ features from a URL for
phishing detection model
============================================
"""

import re
from urllib.parse import urlparse, parse_qs
import config


def extract_features(url):
    """
    Extract all features from a URL

    Args:
        url (str): The URL to analyze

    Returns:
        dict: Dictionary of feature names and values
    """

    # Add scheme if missing (so urlparse works properly)
    if not url.startswith(("http://", "https://", "ftp://")):
        url_to_parse = "http://" + url
    else:
        url_to_parse = url

    # Parse the URL
    parsed = urlparse(url_to_parse)

    # Extract components
    scheme = parsed.scheme          # http or https
    domain = parsed.netloc          # www.example.com
    path = parsed.path              # /login/page
    query = parsed.query            # id=123&name=abc
    fragment = parsed.fragment      # section1

    # Build feature dictionary
    features = {}

    # ── 1. Length-Based Features ──
    features["url_length"] = len(url)
    features["domain_length"] = len(domain)
    features["path_length"] = len(path)
    features["query_length"] = len(query)
    features["fragment_length"] = len(fragment)

    # ── 2. Count-Based Features ──
    features["num_dots"] = url.count(".")
    features["num_hyphens"] = url.count("-")
    features["num_underscores"] = url.count("_")
    features["num_slashes"] = url.count("/")
    features["num_question_marks"] = url.count("?")
    features["num_equal_signs"] = url.count("=")
    features["num_at_symbols"] = url.count("@")
    features["num_ampersands"] = url.count("&")
    features["num_exclamation"] = url.count("!")
    features["num_spaces"] = url.count(" ") + url.count("%20")
    features["num_tilde"] = url.count("~")
    features["num_commas"] = url.count(",")
    features["num_plus"] = url.count("+")
    features["num_asterisks"] = url.count("*")
    features["num_hash"] = url.count("#")
    features["num_dollar"] = url.count("$")
    features["num_percent"] = url.count("%")

    # ── 3. Digit Features ──
    num_digits = sum(1 for c in url if c.isdigit())
    num_letters = sum(1 for c in url if c.isalpha())
    num_special = len(url) - num_digits - num_letters

    features["num_digits"] = num_digits
    features["digit_ratio"] = round(num_digits / max(len(url), 1), 4)
    features["letter_ratio"] = round(num_letters / max(len(url), 1), 4)
    features["special_char_ratio"] = round(num_special / max(len(url), 1), 4)

    # ── 4. Domain Features ──
    features["num_subdomains"] = _count_subdomains(domain)
    features["has_ip_address"] = _has_ip_address(url)
    features["domain_has_digits"] = 1 if any(c.isdigit() for c in domain) else 0

    # ── 5. Protocol Features ──
    features["has_https"] = 1 if scheme == "https" else 0

    # ── 6. Special Pattern Features ──
    features["has_at_symbol"] = 1 if "@" in url else 0
    features["url_depth"] = path.count("/") - 1 if path else 0
    features["url_depth"] = max(features["url_depth"], 0)

    # ── 7. Suspicious Word Features ──
    url_lower = url.lower()
    suspicious_count = sum(1 for word in config.SUSPICIOUS_WORDS if word in url_lower)
    features["has_suspicious_words"] = 1 if suspicious_count > 0 else 0
    features["suspicious_word_count"] = suspicious_count

    # ── 8. Suspicious TLD Feature ──
    features["has_suspicious_tld"] = _has_suspicious_tld(domain)

    # ── 9. URL Shortener Feature ──
    features["is_shortened_url"] = _is_shortened_url(domain)

    return features


# ──────────────────────────────────────
# Helper Functions
# ──────────────────────────────────────

def _count_subdomains(domain):
    """Count number of subdomains (www.sub.example.com → 2)"""

    # Remove port number if exists
    domain = domain.split(":")[0]

    parts = domain.split(".")
    if len(parts) <= 2:
        return 0
    else:
        # Subtract 2 for domain and TLD
        return len(parts) - 2


def _has_ip_address(url):
    """Check if URL contains an IP address"""

    # IPv4 pattern
    ipv4_pattern = r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"

    # Hex IP pattern
    hex_pattern = r"0x[0-9a-fA-F]{1,2}\.0x[0-9a-fA-F]{1,2}\.0x[0-9a-fA-F]{1,2}\.0x[0-9a-fA-F]{1,2}"

    if re.search(ipv4_pattern, url) or re.search(hex_pattern, url):
        return 1
    return 0


def _has_suspicious_tld(domain):
    """Check if domain uses a suspicious TLD"""

    domain = domain.lower().split(":")[0]  # remove port
    parts = domain.split(".")

    if len(parts) >= 2:
        tld = parts[-1]
        if tld in config.SUSPICIOUS_TLDS:
            return 1
    return 0


def _is_shortened_url(domain):
    """Check if URL uses a URL shortening service"""

    domain = domain.lower().split(":")[0]

    for shortener in config.SHORTENER_DOMAINS:
        if shortener in domain:
            return 1
    return 0


def get_feature_values_as_list(features):
    """
    Convert feature dict to a list in correct order
    (Used for model prediction)

    Args:
        features (dict): Feature dictionary

    Returns:
        list: Feature values in correct order
    """

    feature_order = config.FEATURE_NAMES
    values = []

    for name in feature_order:
        if name in features:
            values.append(features[name])
        else:
            values.append(0)

    return values