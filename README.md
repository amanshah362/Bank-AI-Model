# Bank Marketing Prediction System (Flask + Machine Learning)

This project is an end-to-end Machine Learning system that predicts whether a bank customer will subscribe to a term deposit based on demographic, financial, and marketing campaign data.  
The model is deployed as a Flask web application for real-time predictions.

---

## 📊 Dataset
The dataset is taken from the **Bank Marketing Dataset**, which contains information about customer attributes and marketing interactions.

Target Variable:
- `y` → Whether the customer subscribed (`yes` / `no`)

Features include:
- Age, balance, campaign history
- Job, marital status, education
- Loan, housing, default, previous outcome
- Contact type and month

---

## 🔍 Project Workflow

### 1. Data Analysis & Cleaning
- Checked missing values and duplicates
- Performed statistical analysis using `describe()`
- Analyzed feature distributions using histograms
- Detected outliers using IQR method
- Studied correlations using heatmaps

### 2. Feature Engineering
- **One-Hot Encoding** for nominal categorical variables
- **Ordinal Encoding** for ordered categories
- **Robust Scaling** for numerical features (outlier-resistant)

All preprocessing is handled using a **ColumnTransformer pipeline**.

---

## 🧠 Machine Learning Model

Algorithm:
- **Logistic Regression**

Special handling:
- Class imbalance solved using `class_weight='balanced'`
- High iteration limit to ensure convergence

Pipeline:
```python
Preprocessing → Logistic Regression → Prediction
