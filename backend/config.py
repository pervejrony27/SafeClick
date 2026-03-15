"""
============================================
CONFIG.PY — All project settings in one place
============================================
"""

import os

# ── Paths ──
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
DATA_PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
MODELS_DIR = os.path.join(BASE_DIR, "models")

# ── Model Files ──
MODEL_PATH = os.path.join(MODELS_DIR, "phishing_model.pkl")
SCALER_PATH = os.path.join(MODELS_DIR, "scaler.pkl")
MODEL_INFO_PATH = os.path.join(MODELS_DIR, "model_info.json")

# ── Dataset Files ──
RAW_PHISHING_CSV = os.path.join(DATA_RAW_DIR, "phishing_urls.csv")
RAW_LEGITIMATE_CSV = os.path.join(DATA_RAW_DIR, "legitimate_urls.csv")
FINAL_DATASET_CSV = os.path.join(DATA_PROCESSED_DIR, "final_dataset.csv")

# ── Server Settings ──
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5000
DEBUG_MODE = True

# ── Score Thresholds ──
PHISHING_THRESHOLD = 70      # score >= 70 = PHISHING
SUSPICIOUS_THRESHOLD = 40    # score >= 40 = SUSPICIOUS
                              # score < 40  = SAFE

# ── Feature Names (must match training order) ──
FEATURE_NAMES = [
    "url_length",
    "domain_length",
    "num_dots",
    "num_hyphens",
    "num_underscores",
    "num_slashes",
    "num_question_marks",
    "num_equal_signs",
    "num_at_symbols",
    "num_ampersands",
    "num_exclamation",
    "num_spaces",
    "num_tilde",
    "num_commas",
    "num_plus",
    "num_asterisks",
    "num_hash",
    "num_dollar",
    "num_percent",
    "num_digits",
    "num_subdomains",
    "has_ip_address",
    "has_https",
    "has_at_symbol",
    "url_depth",
    "has_suspicious_words",
    "suspicious_word_count",
    "has_suspicious_tld",
    "domain_has_digits",
    "is_shortened_url",
    "path_length",
    "query_length",
    "fragment_length",
    "digit_ratio",
    "letter_ratio",
    "special_char_ratio",
]

# ── Suspicious Keywords ──
SUSPICIOUS_WORDS = [
    "login", "signin", "sign-in", "log-in",
    "bank", "banking", "secure", "security",
    "update", "verify", "verification",
    "account", "password", "passwd",
    "confirm", "suspend", "restrict",
    "alert", "notification", "urgent",
    "paypal", "ebay", "amazon", "apple",
    "microsoft", "google", "facebook",
    "netflix", "instagram", "whatsapp",
    "wallet", "credit", "debit",
    "ssn", "social-security",
    "free", "winner", "prize", "reward",
    "claim", "bonus", "offer", "gift",
    "lucky", "congratulations",
]

# ── Suspicious TLDs ──
SUSPICIOUS_TLDS = [
    "tk", "ml", "ga", "cf", "gq",
    "xyz", "top", "work", "click",
    "link", "buzz", "surf", "rest",
    "fit", "cam", "bid", "loan",
    "racing", "win", "review",
    "country", "stream", "download",
    "cricket", "science", "party",
    "gdn", "accountant", "faith",
]

# ── URL Shortener Domains ──
SHORTENER_DOMAINS = [
    "bit.ly", "tinyurl.com", "t.co",
    "goo.gl", "ow.ly", "is.gd",
    "buff.ly", "adf.ly", "tiny.cc",
    "lnkd.in", "db.tt", "qr.ae",
    "rebrand.ly", "shorturl.at",
    "cutt.ly", "rb.gy",
]