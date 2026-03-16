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
``` 
