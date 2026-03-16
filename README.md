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
SafeClick analyzes any URL using **36 intelligent features** and a **Random Forest ML model** trained on **70,000+ real URLs** to give users:
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

2. Setup Backend
Bash

cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
3. Prepare Dataset
Option A: Quick Start (Sample Data)

Bash

python data/download_data.py
Option B: Full Dataset (Recommended for best accuracy)

Bash

# 1. Download from Kaggle:
#    https://www.kaggle.com/datasets/siddharthkumar25/malicious-and-benign-urls
#
# 2. Put the CSV file in: backend/data/raw/dataset.csv
#
# 3. Filter to 70K balanced URLs:
python data/filter_dataset.py
4. Train the Model
Bash

python -m ml.train_model
Expected output:

text

🛡️  SafeClick — Model Training Pipeline
📂 Loading dataset... 70,000 URLs
🔧 Extracting features... (3-5 minutes)
🤖 Training Random Forest model...
📊 Accuracy: 94.55%
💾 Model saved!
5. Start Backend Server
Bash

python run.py
text

🛡️  SafeClick — Phishing Detection API
📡 Server: http://localhost:5000
📡 Scan endpoint: POST http://localhost:5000/api/scan
6. Start Frontend (New Terminal)
Bash

cd frontend
python -m http.server 5500
text

Open browser → http://localhost:5500
7. Try It Out!
text

1. Open http://localhost:5500
2. Paste a URL: http://192.168.1.1/login/bank-secure/verify.php
3. Click "🔍 Scan Now"
4. See the phishing score and reasons!
📊 Model Performance
Metrics (Trained on 70,000 URLs)
Metric	Score
Accuracy	94.55%
Precision	94.30%
Recall	94.80%
F1-Score	94.55%
Confusion Matrix
text

                  Predicted
                Safe    Phishing
Actual Safe    [ 6,623    377  ]
Actual Phish   [   385   6,615 ]
What the Score Means
Score Range	Risk Level	Meaning
0 — 39	✅ SAFE	Low risk, likely legitimate
40 — 69	⚡ SUSPICIOUS	Some red flags, proceed with caution
70 — 100	🚨 PHISHING	High risk, do NOT click or enter info
🔍 Features Extracted from URLs
Our model analyzes 36 features from each URL:

Length-Based Features
Feature	Description
url_length	Total length of the URL
domain_length	Length of the domain name
path_length	Length of the URL path
query_length	Length of query parameters
Count-Based Features
Feature	Description
num_dots	Number of dots (.) in URL
num_hyphens	Number of hyphens (-)
num_underscores	Number of underscores (_)
num_slashes	Number of slashes (/)
num_digits	Count of numeric digits
num_special_chars	Special characters count
Security Features
Feature	Description
has_ip_address	URL contains IP instead of domain
has_https	Uses HTTPS (encrypted) or not
has_at_symbol	Contains @ (redirect trick)
has_suspicious_tld	Uses risky TLD (.tk, .ml, etc.)
is_shortened_url	Uses URL shortener (bit.ly, etc.)
suspicious_word_count	Contains words like login, bank, verify
Ratio Features
Feature	Description
digit_ratio	Percentage of digits in URL
letter_ratio	Percentage of letters in URL
special_char_ratio	Percentage of special characters
📡 API Documentation
Base URL
text

http://localhost:5000
Endpoints
1. Health Check
http

GET /
Response:

JSON

{
    "status": "running",
    "message": "SafeClick API is running!"
}
2. API Health
http

GET /api/health
Response:

JSON

{
    "status": "healthy",
    "model_loaded": true
}
3. Scan URL (Main Endpoint)
http

POST /api/scan
Content-Type: application/json
Request Body:

JSON

{
    "url": "http://suspicious-link.tk/login/bank-verify"
}
Response:

JSON

{
    "success": true,
    "url": "http://suspicious-link.tk/login/bank-verify",
    "phishing_score": 85,
    "risk_level": "PHISHING",
    "reasons": [
        "🔴 URL uses suspicious TLD (.tk) — commonly used in phishing",
        "🔴 URL contains suspicious keywords: login, bank, verify",
        "🟡 URL does not use HTTPS — connection is not encrypted",
        "🟡 URL is quite long (52 characters)"
    ],
    "features_analyzed": 36
}
4. Batch Scan (Multiple URLs)
http

POST /api/scan/batch
Content-Type: application/json
Request Body:

JSON

{
    "urls": [
        "https://www.google.com",
        "http://evil-phishing.tk/login",
        "https://www.github.com"
    ]
}
Response:

JSON

{
    "success": true,
    "count": 3,
    "results": [
        { "url": "https://www.google.com", "phishing_score": 5, "risk_level": "SAFE" },
        { "url": "http://evil-phishing.tk/login", "phishing_score": 85, "risk_level": "PHISHING" },
        { "url": "https://www.github.com", "phishing_score": 3, "risk_level": "SAFE" }
    ]
}
🔗 How Frontend Connects to Backend
text

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
Connection file: frontend/js/api.js → calls → backend/api/routes.py

💡 Learning Features
SafeClick educates users about phishing:

📚 What Users Learn
Topic	What They Learn
🎣 What is Phishing	How attackers create fake websites
🔍 How to Spot It	Red flags in URLs and emails
📊 Statistics	Real-world phishing attack data
🛡️ Stay Safe	Best practices for online safety
💡 Tips	Rotating tips on every page visit
📊 Phishing Facts Included
91% of cyber attacks start with phishing
3.4 billion phishing emails sent daily
36% of data breaches involve phishing
Mobile phishing increased by 85%
Average phishing attack cost: $4.76 million
🧪 Running Tests
Bash

cd backend

# Activate virtual environment
venv\Scripts\activate

# Test feature extraction
python -m tests.test_features

# Test API endpoints
python -m tests.test_api
📁 Dataset Information
Source
Dataset: Malicious and Benign URLs — Kaggle
Original Size: 450,000+ URLs
Filtered Size: 70,000 URLs (35,000 phishing + 35,000 legitimate)
Labels: benign, phishing, malware, defacement → converted to 0/1
Data Pipeline
text

Kaggle CSV (450K) → filter_dataset.py → final_dataset.csv (70K) → train_model.py → model.pkl
🛠️ Development
How to Modify the Model
Change accuracy target: Edit train_model.py → modify RandomForestClassifier parameters
Add new features: Edit feature_extractor.py → add new feature functions
Update reasons: Edit explainer.py → add new explanation rules
Retrain: Run python -m ml.train_model
Model Parameters (Current)
Python

RandomForestClassifier(
    n_estimators=50,        # Number of trees
    max_depth=10,           # Maximum tree depth
    min_samples_split=10,   # Minimum samples to split
    min_samples_leaf=5,     # Minimum samples in leaf
    max_features=0.6,       # Features per tree (60%)
    class_weight="balanced" # Handle imbalanced data
)
🐛 Troubleshooting
Problem	Solution
ModuleNotFoundError: flask	Run pip install -r requirements.txt
Cannot connect to server	Make sure backend is running: python run.py
CORS error in browser	Check app.py CORS settings allow your frontend port
Model accuracy 100%	Using sample data — use real 70K dataset
No module named 'flask_cors'	Activate venv first: venv\Scripts\activate
Frontend shows error	Check both terminals are running (backend + frontend)
📸 Screenshots
Scanner Page
text

🗺️ Future Improvements
 Browser extension for real-time protection
 Email phishing scanner
 Deep learning model (LSTM/BERT)
 User accounts and scan history
 Real-time URL reputation checking
 Multi-language support
 Mobile app version
👥 Team
Name	Role
[Your Name]	[Full Stack Developer / ML Engineer]
[Member 2]	[Frontend Developer]
[Member 3]	[Data Analyst / ML]
🎓 University Details
Detail	Info
University	[Your University Name]
Department	[Computer Science / IT / CSE]
Course	[Course Name]
Supervisor	[Professor Name]
Year	2025
📚 References
Phishing Website Detection using Machine Learning
Kaggle — Malicious and Benign URLs Dataset
Anti-Phishing Working Group (APWG)
PhishTank — Phishing URL Database
Google Safe Browsing
Scikit-learn Documentation
Flask Documentation
📄 License
This project is developed for educational purposes as part of a university project.

© 2025 SafeClick — All Rights Reserved

<p align="center"> Made with ❤️ for a safer internet </p><p align="center"> <strong>🛡️ SafeClick — Click Smarter, Stay Safer 🛡️</strong> </p> ```