"""
============================================
TRAIN_MODEL.PY
Trains ONLY on final_dataset.csv
============================================

Usage:
    cd backend
    python -m ml.train_model
"""

import os
import json
import time
import pandas as pd
import numpy as np
from datetime import datetime

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)

import joblib
import config
from ml.feature_extractor import extract_features, get_feature_values_as_list


def load_dataset():
    """
    Load ONLY from final_dataset.csv
    Must have columns: url, label
    label: 1 = phishing, 0 = legitimate
    """

    print("\n📂 Loading dataset...")

    # Only load final_dataset.csv
    if not os.path.exists(config.FINAL_DATASET_CSV):
        raise FileNotFoundError(
            f"\n❌ Dataset not found!\n"
            f"   Expected file: {config.FINAL_DATASET_CSV}\n"
            f"\n   To create it:\n"
            f"   1. Download dataset from Kaggle\n"
            f"   2. Put CSV in backend/data/raw/dataset.csv\n"
            f"   3. Run: python data/filter_dataset.py\n"
        )

    df = pd.read_csv(config.FINAL_DATASET_CSV)

    # Validate columns
    if "url" not in df.columns or "label" not in df.columns:
        raise ValueError(
            "Dataset must have 'url' and 'label' columns.\n"
            "   label: 1 = phishing, 0 = legitimate"
        )

    print(f"   File: {config.FINAL_DATASET_CSV}")
    print(f"   Total URLs: {len(df)}")
    print(f"   Phishing (1): {(df['label'] == 1).sum()}")
    print(f"   Legitimate (0): {(df['label'] == 0).sum()}")

    return df


def extract_features_from_dataset(df):
    """
    Extract features from all URLs
    """

    print("\n🔧 Extracting features from URLs...")
    print(f"   Processing {len(df)} URLs (this may take a few minutes)...")

    feature_list = []
    labels = []
    errors = 0

    start_time = time.time()

    for idx, row in df.iterrows():
        try:
            url = str(row["url"]).strip()
            features = extract_features(url)
            feature_values = get_feature_values_as_list(features)
            feature_list.append(feature_values)
            labels.append(row["label"])

        except Exception as e:
            errors += 1
            continue

        # Progress update every 5000 URLs
        if (idx + 1) % 5000 == 0:
            elapsed = time.time() - start_time
            print(f"   Processed {idx + 1}/{len(df)} URLs... ({elapsed:.1f}s)")

    elapsed = time.time() - start_time
    print(f"   ✅ Feature extraction complete in {elapsed:.1f}s")
    print(f"   Successfully processed: {len(feature_list)}")
    print(f"   Errors/skipped: {errors}")

    X = np.array(feature_list)
    y = np.array(labels)

    return X, y


def train_model(X_train, y_train):
    """
    Train Random Forest model
    Tuned for 94-95% accuracy on 70K dataset
    """

    print("\n🤖 Training Random Forest model...")

    model = RandomForestClassifier(
        n_estimators=50,
        max_depth=10,
        min_samples_split=10,
        min_samples_leaf=5,
        max_features=0.6,
        random_state=42,
        n_jobs=-1,
        class_weight="balanced",
    )

    start_time = time.time()
    model.fit(X_train, y_train)
    elapsed = time.time() - start_time

    print(f"   ✅ Training complete in {elapsed:.1f}s")

    return model


def evaluate_model(model, X_test, y_test):
    """
    Evaluate model performance
    """

    print("\n📊 Evaluating model...")

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print(f"   Accuracy:  {accuracy:.4f}  ({accuracy*100:.2f}%)")
    print(f"   Precision: {precision:.4f}")
    print(f"   Recall:    {recall:.4f}")
    print(f"   F1-Score:  {f1:.4f}")

    print(f"\n   Classification Report:")
    print(classification_report(y_test, y_pred,
                                target_names=["Legitimate", "Phishing"]))

    cm = confusion_matrix(y_test, y_pred)
    print(f"   Confusion Matrix:")
    print(f"   {cm}")

    metrics = {
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
        "confusion_matrix": cm.tolist(),
    }

    return metrics


def save_model(model, scaler, metrics, num_features, num_samples):
    """
    Save model, scaler, and info
    """

    print("\n💾 Saving model...")

    os.makedirs(config.MODELS_DIR, exist_ok=True)

    # Save model
    joblib.dump(model, config.MODEL_PATH)
    print(f"   Model saved: {config.MODEL_PATH}")

    # Save scaler
    joblib.dump(scaler, config.SCALER_PATH)
    print(f"   Scaler saved: {config.SCALER_PATH}")

    # Save model info
    model_info = {
        "model_type": "RandomForestClassifier",
        "model_settings": {
            "n_estimators": 50,
            "max_depth": 10,
            "min_samples_split": 10,
            "min_samples_leaf": 5,
            "max_features": 0.6,
        },
        "num_features": num_features,
        "feature_names": config.FEATURE_NAMES,
        "num_training_samples": num_samples,
        "dataset": "final_dataset.csv",
        "metrics": metrics,
        "trained_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "thresholds": {
            "phishing": config.PHISHING_THRESHOLD,
            "suspicious": config.SUSPICIOUS_THRESHOLD,
        }
    }

    with open(config.MODEL_INFO_PATH, "w") as f:
        json.dump(model_info, f, indent=4)
    print(f"   Model info saved: {config.MODEL_INFO_PATH}")

    print("\n   ✅ All files saved successfully!")


def run_training_pipeline():
    """
    Complete training pipeline
    ONLY uses final_dataset.csv
    """

    print("=" * 55)
    print("🛡️   SafeClick  — Model Training Pipeline")
    print("=" * 55)
    print("📁 Training on: final_dataset.csv ONLY")

    # Step 1: Load final_dataset.csv
    df = load_dataset()

    # Step 2: Extract features
    X, y = extract_features_from_dataset(df)

    print(f"\n📐 Feature matrix shape: {X.shape}")
    print(f"   Number of features: {X.shape[1]}")
    print(f"   Number of samples: {X.shape[0]}")

    # Step 3: Split into train/test
    print("\n✂️  Splitting dataset (80% train, 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"   Training set: {X_train.shape[0]} samples")
    print(f"   Testing set:  {X_test.shape[0]} samples")

    # Step 4: Scale features
    print("\n⚖️  Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Step 5: Train model
    model = train_model(X_train_scaled, y_train)

    # Step 6: Evaluate model
    metrics = evaluate_model(model, X_test_scaled, y_test)

    # Step 7: Save everything
    save_model(model, scaler, metrics, X.shape[1], X_train.shape[0])

    print("\n" + "=" * 55)
    print(f"🎉 Training complete!")
    print(f"   Dataset: final_dataset.csv")
    print(f"   Samples: {X.shape[0]}")
    print(f"   Accuracy: {metrics['accuracy']*100:.2f}%")
    print(f"   Model saved and ready to use!")
    print("=" * 55)


# ── Run ──
if __name__ == "__main__":
    run_training_pipeline()