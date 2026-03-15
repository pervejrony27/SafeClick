"""
============================================
FILTER_DATASET.PY
Takes your large dataset (450K URLs)
Filters it down to 300,000 balanced URLs
(150,000 phishing + 150,000 legitimate)
============================================

Usage:
    cd backend
    python data/filter_dataset.py
"""

import pandas as pd
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


def filter_dataset():
    print("=" * 55)
    print("🔍 Dataset Filter — 450K → 300K URLs")
    print("=" * 55)

    # ── Step 1: Find and Load the CSV ──
    # Try multiple possible file locations
    possible_paths = [
        os.path.join(config.DATA_RAW_DIR, "dataset.csv"),
        os.path.join(config.DATA_RAW_DIR, "urls.csv"),
        os.path.join(config.DATA_RAW_DIR, "malicious_phish.csv"),
        os.path.join(config.DATA_RAW_DIR, "phishing_site_urls.csv"),
        os.path.join(config.DATA_RAW_DIR, "urldata.csv"),
        os.path.join(config.DATA_RAW_DIR, "data.csv"),
        os.path.join(config.BASE_DIR, "data", "dataset.csv"),
    ]

    df = None
    loaded_path = None

    # Try each possible path
    for path in possible_paths:
        if os.path.exists(path):
            print(f"\n📂 Found file: {path}")
            df = pd.read_csv(path)
            loaded_path = path
            break

    # If not found, ask user
    if df is None:
        print("\n❌ No dataset file found automatically.")
        print(f"   Please put your CSV file in: {config.DATA_RAW_DIR}")
        print(f"   Supported names: dataset.csv, urls.csv, data.csv")
        print(f"\n   OR enter the full path to your CSV file:")

        file_path = input("\n   File path: ").strip().strip('"')

        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            loaded_path = file_path
        else:
            print(f"   ❌ File not found: {file_path}")
            return

    # ── Step 2: Show What We Loaded ──
    print(f"\n📊 Dataset loaded from: {loaded_path}")
    print(f"   Total rows: {len(df)}")
    print(f"   Columns: {list(df.columns)}")
    print(f"\n   First 3 rows:")
    print(df.head(3).to_string())

    # ── Step 3: Detect Column Names ──
    url_col = detect_url_column(df)
    label_col = detect_label_column(df)

    if url_col is None:
        print("\n❌ Could not find URL column!")
        print(f"   Available columns: {list(df.columns)}")
        url_col = input("   Enter the URL column name: ").strip()

    if label_col is None:
        print("\n❌ Could not find label column!")
        print(f"   Available columns: {list(df.columns)}")
        label_col = input("   Enter the label column name: ").strip()

    print(f"\n   URL column: '{url_col}'")
    print(f"   Label column: '{label_col}'")

    # ── Step 4: Understand Label Values ──
    print(f"\n   Unique labels: {df[label_col].unique()}")
    print(f"\n   Label distribution:")
    print(df[label_col].value_counts().to_string())

    # ── Step 5: Normalize Labels ──
    df = normalize_labels(df, label_col)

    phishing_count = (df["label"] == 1).sum()
    legit_count = (df["label"] == 0).sum()

    print(f"\n   After normalization:")
    print(f"   Phishing (1): {phishing_count}")
    print(f"   Legitimate (0): {legit_count}")

    # ── Step 6: Clean Data ──
    print(f"\n🧹 Cleaning data...")

    # Rename URL column
    df = df.rename(columns={url_col: "url"})

    # Remove nulls
    before = len(df)
    df = df.dropna(subset=["url", "label"])
    after = len(df)
    print(f"   Removed {before - after} rows with null values")

    # Remove duplicates
    before = len(df)
    df = df.drop_duplicates(subset=["url"])
    after = len(df)
    print(f"   Removed {before - after} duplicate URLs")

    # Remove very short URLs
    before = len(df)
    df = df[df["url"].str.len() >= 8]
    after = len(df)
    print(f"   Removed {before - after} URLs shorter than 8 characters")

    # Keep only url and label columns
    df = df[["url", "label"]].reset_index(drop=True)

    phishing_count = (df["label"] == 1).sum()
    legit_count = (df["label"] == 0).sum()
    print(f"\n   After cleaning:")
    print(f"   Phishing: {phishing_count}")
    print(f"   Legitimate: {legit_count}")
    print(f"   Total: {len(df)}")

    # ── Step 7: Filter to 300K (150K each) ──

    target_total = 300000
    target_each = target_total // 2  # 150,000 each

    print(f"\n✂️  Filtering to {target_total} URLs ({target_each} each)...")

    phishing_df = df[df["label"] == 1]
    legit_df = df[df["label"] == 0]

    # If we have enough of each, sample equally
    if len(phishing_df) >= target_each and len(legit_df) >= target_each:
        phishing_sample = phishing_df.sample(n=target_each, random_state=42)
        legit_sample = legit_df.sample(n=target_each, random_state=42)
        print(f"   ✅ Sampled {target_each} phishing + {target_each} legitimate")

    # If one class has fewer, adjust
    elif len(phishing_df) < target_each:
        phishing_sample = phishing_df  # take all phishing
        legit_sample = legit_df.sample(
            n=min(target_total - len(phishing_df), len(legit_df)),
            random_state=42
        )
        print(f"   ⚠️ Only {len(phishing_sample)} phishing available")
        print(f"   Taking {len(legit_sample)} legitimate to compensate")

    else:
        legit_sample = legit_df  # take all legitimate
        phishing_sample = phishing_df.sample(
            n=min(target_total - len(legit_df), len(phishing_df)),
            random_state=42
        )
        print(f"   ⚠️ Only {len(legit_sample)} legitimate available")
        print(f"   Taking {len(phishing_sample)} phishing to compensate")

    # Combine and shuffle
    filtered_df = pd.concat([phishing_sample, legit_sample], ignore_index=True)
    filtered_df = filtered_df.sample(frac=1, random_state=42).reset_index(drop=True)

    # ── Step 8: Save ──
    os.makedirs(config.DATA_PROCESSED_DIR, exist_ok=True)
    output_path = config.FINAL_DATASET_CSV
    filtered_df.to_csv(output_path, index=False)

    # ── Step 9: Summary ──
    print(f"\n" + "=" * 55)
    print(f"✅ FILTERED DATASET SAVED!")
    print(f"=" * 55)
    print(f"   📁 Saved to: {output_path}")
    print(f"   📊 Total URLs: {len(filtered_df)}")
    print(f"   🔴 Phishing: {(filtered_df['label'] == 1).sum()}")
    print(f"   🟢 Legitimate: {(filtered_df['label'] == 0).sum()}")
    print(f"\n   Next step: Train the model!")
    print(f"   Run: python -m ml.train_model")
    print(f"=" * 55)

    return filtered_df


def detect_url_column(df):
    """Auto-detect the URL column"""

    possible_names = [
        "url", "URL", "Url",
        "urls", "URLs",
        "link", "Link",
        "links", "Links",
        "website", "Website",
        "web_address",
        "domain", "Domain",
    ]

    for name in possible_names:
        if name in df.columns:
            return name

    # Check if first column looks like URLs
    first_col = df.columns[0]
    sample = str(df[first_col].iloc[0])
    if "http" in sample or "www" in sample or ".com" in sample:
        return first_col

    return None


def detect_label_column(df):
    """Auto-detect the label column"""

    possible_names = [
        "label", "Label",
        "labels", "Labels",
        "type", "Type",
        "class", "Class",
        "category", "Category",
        "target", "Target",
        "result", "Result",
        "status", "Status",
        "is_phishing",
        "phishing",
        "malicious",
    ]

    for name in possible_names:
        if name in df.columns:
            return name

    # Check last column
    last_col = df.columns[-1]
    unique_vals = df[last_col].nunique()
    if unique_vals <= 10:  # likely a label column
        return last_col

    return None


def normalize_labels(df, label_col):
    """
    Convert various label formats to: 1 = phishing, 0 = legitimate

    Handles:
        - "phishing" / "legitimate" / "benign"
        - "bad" / "good"
        - "malicious" / "safe"
        - 1 / 0
        - "yes" / "no"
    """

    df = df.copy()

    # Get unique values
    unique_vals = df[label_col].unique()
    print(f"\n   Detected label values: {unique_vals}")

    # Check if already 0 and 1
    if set(unique_vals) <= {0, 1, 0.0, 1.0}:
        df["label"] = df[label_col].astype(int)
        return df

    # String labels — convert to lowercase
    df[label_col] = df[label_col].astype(str).str.lower().str.strip()

    # Define mapping
    phishing_labels = [
        "phishing", "malicious", "bad", "spam",
        "malware", "defacement", "yes", "1",
        "suspicious", "unsafe", "dangerous",
        "phish", "fake", "fraud",
    ]

    legit_labels = [
        "legitimate", "benign", "good", "safe",
        "clean", "no", "0", "normal", "legal",
        "real", "genuine", "ham",
    ]

    def map_label(val):
        val = str(val).lower().strip()

        for p in phishing_labels:
            if p in val:
                return 1

        for l in legit_labels:
            if l in val:
                return 0

        # Unknown — try to guess
        return -1

    df["label"] = df[label_col].apply(map_label)

    # Remove unknown labels
    unknown_count = (df["label"] == -1).sum()
    if unknown_count > 0:
        print(f"   ⚠️ Removed {unknown_count} rows with unknown labels")
        # Show what was unknown
        unknown_vals = df[df["label"] == -1][label_col].unique()
        print(f"   Unknown values: {unknown_vals[:10]}")
        df = df[df["label"] != -1]

    df["label"] = df["label"].astype(int)

    return df


# ── Run ──
if __name__ == "__main__":
    filter_dataset()