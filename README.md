# 🛡️ SafeClick — Phishing Link Detection & Learning System

<p align="center">
  <strong>Detect phishing links instantly. Learn why they're dangerous.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Flask-3.0-green?style=flat-square&logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/ML-Scikit--learn-orange?style=flat-square&logo=scikit-learn" alt="Scikit-learn">
  <img src="https://img.shields.io/badge/Accuracy-94.55%25-brightgreen?style=flat-square" alt="Accuracy">
  <img src="https://img.shields.io/badge/License-Educational-lightgrey?style=flat-square" alt="License">
</p>

---

## 📖 About The Project

**SafeClick** is a machine learning-based phishing URL detection system that helps users identify whether a link is **safe**, **suspicious**, or a **phishing** attempt. It doesn't just detect — it **educates** users about phishing attacks and teaches them how to stay safe online.

### The Problem
- 🎣 **91%** of cyber attacks start with a phishing email
- 📧 **3.4 billion** phishing emails are sent every day
- 💰 Average cost of a phishing attack: **$4.76 million**
- 😰 Most people can't tell a phishing link from a real one

### Our Solution
SafeClick analyzes any URL using **36 intelligent features** and a **Random Forest ML model** trained on **3,00,000+ real URLs** to give users:
- A **phishing score** (0-100)
- A **risk level** (Safe / Suspicious / Phishing)
- **Detailed reasons** explaining why the URL is dangerous
- **Educational tips** about phishing and online safety

---

## 🎯 Features

| Feature | Description |
|---------|-------------|
| 🔍 **URL Scanner** | Paste any URL to instantly check if it's phishing |
| 📊 **Phishing Score** | Get a score from 0-100 (higher = more dangerous) |
| 🚦 **Risk Level** | Clear labels: SAFE / SUSPICIOUS / PHISHING |
| 📋 **Detailed Reasons** | Explains exactly WHY the URL is flagged |
| 💡 **Learn Section** | Educational tips and facts about phishing |
| 🤖 **Machine Learning** | Trained on 70,000+ real-world URLs |
| 📈 **94-95% Accuracy** | Reliable and realistic detection |
| 📱 **Responsive Design** | Works on desktop, tablet, and mobile |
| ⚡ **Fast Analysis** | Results in under 1 second |
| 🔄 **Batch Scanning** | Scan up to 10 URLs at once via API |

---

## 🏗️ Project Structure
```
SafeClick/
│
├── 📁 backend/ ← Python (Flask + Machine Learning)
│ ├── 📁 api/
│ │ ├── init.py
│ │ ├── app.py ← Flask app with CORS
│ │ └── routes.py ← API endpoints (/api/scan)
│ │
│ ├── 📁 ml/
│ │ ├── init.py
│ │ ├── feature_extractor.py ← Extracts 36 features from URL
│ │ ├── predict.py ← Loads model & predicts score
│ │ ├── explainer.py ← Generates human-readable reasons
│ │ └── train_model.py ← Training pipeline
│ │
│ ├── 📁 models/
│ │ ├── phishing_model.pkl ← Trained ML model (generated)
│ │ ├── scaler.pkl ← Feature scaler (generated)
│ │ └── model_info.json ← Model metadata & metrics
│ │
│ ├── 📁 data/
│ │ ├── 📁 raw/ ← Raw dataset from Kaggle
│ │ ├── 📁 processed/ ← Cleaned & filtered dataset
│ │ ├── download_data.py ← Sample data generator
│ │ └── filter_dataset.py ← Filters 450K → 70K URLs
│ │
│ ├── 📁 notebooks/
│ │ ├── 01_data_exploration.ipynb
│ │ ├── 02_feature_engineering.ipynb
│ │ ├── 03_model_training.ipynb
│ │ └── 04_evaluation.ipynb
│ │
│ ├── 📁 tests/
│ │ ├── test_features.py ← Feature extraction tests
│ │ └── test_api.py ← API endpoint tests
│ │
│ ├── config.py ← All settings & constants
│ ├── requirements.txt ← Python dependencies
│ └── run.py ← Start backend server
│
├── 📁 frontend/ ← HTML + CSS + JavaScript
│ ├── index.html ← Main scanner page
│ ├── about.html ← About the project
│ ├── how-it-works.html ← How it works page
│ │
│ ├── 📁 css/
│ │ ├── style.css ← Global styles
│ │ ├── scanner.css ← Scanner section styles
│ │ └── results.css ← Results display styles
│ │
│ ├── 📁 js/
│ │ ├── api.js ← ⭐ Connects frontend to backend
│ │ ├── scanner.js ← Scanner form logic
│ │ ├── results.js ← Results display + animation
│ │ └── utils.js ← Helper functions + tips
│ │
│ └── 📁 assets/
│ └── 📁 images/
│
├── .gitignore
└── README.md
```

## 💻 Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | HTML5, CSS3, JavaScript | User interface & scanner |
| **Backend** | Python 3.8+, Flask | REST API server |
| **ML Model** | Scikit-learn, Random Forest | Phishing prediction |
| **Data Processing** | Pandas, NumPy | Dataset handling |
| **Feature Extraction** | urllib, regex, tldextract | URL analysis |
| **Visualization** | Matplotlib, Seaborn | Model evaluation charts |
| **Communication** | REST API (JSON) | Frontend ↔ Backend |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** — [Download Python](https://www.python.org/downloads/)
- **Web Browser** — Chrome, Edge, or Firefox
- **Git** — [Download Git](https://git-scm.com/downloads/)

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/SafeClick.git
cd SafeClick
``` 

```
Frontend (localhost:5500)              Backend (localhost:5000)

index.html                             run.py
    │                                      │
    │ User clicks "Scan Now"               │
    ▼                                      │
js/api.js                                  │
    │                                      │
    │ fetch("localhost:5000/api/scan") ───► api/routes.py
    │                                      │
    │                                      ├── ml/feature_extractor.py
    │                                      ├── ml/predict.py
    │                                      ├── ml/explainer.py
    │                                      │
    │ JSON response ◄────────────────────── │
    ▼                                      
js/results.js
    │
    Shows score + reasons on page
    ```


    