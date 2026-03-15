"""
============================================
TEST_FEATURES.PY
Test the feature extraction module

Run:
    cd backend
    python -m tests.test_features
============================================
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.feature_extractor import extract_features, get_feature_values_as_list


def test_safe_url():
    """Test feature extraction on a safe URL"""

    print("\n🧪 Test 1: Safe URL")
    print("-" * 40)

    url = "https://www.google.com"
    features = extract_features(url)

    print(f"   URL: {url}")
    print(f"   Features extracted: {len(features)}")

    assert features["has_https"] == 1, "Should detect HTTPS"
    assert features["has_ip_address"] == 0, "Should not have IP"
    assert features["has_at_symbol"] == 0, "Should not have @"
    assert features["has_suspicious_tld"] == 0, "Should not have suspicious TLD"

    print("   ✅ All assertions passed!")
    return features


def test_phishing_url():
    """Test feature extraction on a phishing URL"""

    print("\n🧪 Test 2: Phishing URL")
    print("-" * 40)

    url = "http://192.168.1.1/login/bank-secure/verify.php"
    features = extract_features(url)

    print(f"   URL: {url}")
    print(f"   Features extracted: {len(features)}")

    assert features["has_https"] == 0, "Should not have HTTPS"
    assert features["has_ip_address"] == 1, "Should detect IP address"
    assert features["has_suspicious_words"] == 1, "Should detect suspicious words"

    print("   ✅ All assertions passed!")
    return features


def test_suspicious_url():
    """Test feature extraction on a suspicious URL"""

    print("\n🧪 Test 3: Suspicious URL")
    print("-" * 40)

    url = "http://free-prize-winner.tk/claim-now?user=you@email.com"
    features = extract_features(url)

    print(f"   URL: {url}")
    print(f"   Features extracted: {len(features)}")

    assert features["has_https"] == 0, "Should not have HTTPS"
    assert features["has_suspicious_tld"] == 1, "Should detect .tk TLD"
    assert features["has_at_symbol"] == 1, "Should detect @ symbol"
    assert features["has_suspicious_words"] == 1, "Should detect suspicious words"

    print("   ✅ All assertions passed!")
    return features


def test_feature_values_list():
    """Test converting features dict to ordered list"""

    print("\n🧪 Test 4: Feature Values List")
    print("-" * 40)

    url = "https://www.example.com"
    features = extract_features(url)
    values = get_feature_values_as_list(features)

    print(f"   Number of values: {len(values)}")
    assert len(values) > 0, "Should return non-empty list"
    assert all(isinstance(v, (int, float)) for v in values), "All values should be numeric"

    print("   ✅ All assertions passed!")


def test_print_all_features():
    """Print all features for a URL (for debugging)"""

    print("\n🧪 Test 5: Print All Features")
    print("-" * 40)

    url = "http://192.168.1.1/login/bank-secure/verify.php?id=123&token=abc"
    features = extract_features(url)

    print(f"   URL: {url}\n")
    for name, value in features.items():
        print(f"   {name:30s} = {value}")


if __name__ == "__main__":
    print("=" * 50)
    print("🧪 Running Feature Extraction Tests")
    print("=" * 50)

    test_safe_url()
    test_phishing_url()
    test_suspicious_url()
    test_feature_values_list()
    test_print_all_features()

    print("\n" + "=" * 50)
    print("✅ All tests passed!")
    print("=" * 50)