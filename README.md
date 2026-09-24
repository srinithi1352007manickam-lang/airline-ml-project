# ✈️ SkyPulse AI - Airline Customer Satisfaction Machine Learning System

An end-to-end Machine Learning web application that predicts passenger satisfaction using the **Airline Customer Satisfaction** dataset and a **Random Forest Classifier** with a modern, responsive web dashboard built with Streamlit and Plotly.

---

## 📋 Table of Contents
1. [Project Overview](#-project-overview)
2. [Dataset Details & Inspection](#-dataset-details--inspection)
3. [Machine Learning Pipeline](#-machine-learning-pipeline)
4. [Model Performance & Evaluation](#-model-performance--evaluation)
5. [Key Feature Importances](#-key-feature-importances)
6. [Web Application Features](#-web-application-features)
7. [Project Directory Structure](#-project-directory-structure)
8. [Installation & Local Setup](#-installation--local-setup)
9. [Usage Guide](#-usage-guide)

---

## 🚀 Project Overview

Customer satisfaction directly governs retention and profitability in the competitive aviation industry. This project solves a binary classification problem: predicting whether a passenger is **Satisfied** or **Dissatisfied** based on:
- Passenger profile (Age, Customer Loyalty, Travel Purpose, Flight Class, Distance)
- Cabin experience ratings (Seat comfort, Inflight entertainment, Food/drink, Cleanliness, Leg room)
- Airport & digital services (Inflight Wi-Fi, Online booking, Support, Boarding, Gate convenience)
- Flight operations (Departure and Arrival delays in minutes)

---

## 📊 Dataset Details & Inspection

- **Source File:** `dataset/Airline_customer_satisfaction.csv`
- **Total Samples:** `129,880` rows
- **Total Features:** `22` columns
- **Duplicate Rows:** `0`
- **Target Column:** `satisfaction`
  - `satisfied`: 71,087 samples (54.7%)
  - `dissatisfied`: 58,793 samples (45.3%)
- **Missing Values:** `Arrival Delay in Minutes` had 393 missing records (0.3%), handled automatically via **median imputation** inside the preprocessing pipeline.

### Column Breakdown:
| Feature Category | Columns |
| :--- | :--- |
| **Target Variable** | `satisfaction` ('satisfied', 'dissatisfied') |
| **Categorical Features (3)** | `Customer Type`, `Type of Travel`, `Class` |
| **Demographics & Travel (2)**| `Age`, `Flight Distance` |
| **Inflight Experience (8)** | `Seat comfort`, `Food and drink`, `Inflight entertainment`, `Cleanliness`, `Leg room service`, `On-board service`, `Baggage handling`, `Checkin service` |
| **Digital & Airport (6)** | `Inflight wifi service`, `Online support`, `Ease of Online booking`, `Online boarding`, `Gate location`, `Departure/Arrival time convenient` |
| **Flight Delays (2)** | `Departure Delay in Minutes`, `Arrival Delay in Minutes` |

---

## 🌲 Machine Learning Pipeline

1. **Data Leakage Prevention:** Preprocessing steps (`SimpleImputer` and `OneHotEncoder`) are fitted strictly on the training set and applied to test and runtime inputs.
2. **Stratified Splitting:** 80% Training (103,904 samples) and 20% Testing (25,976 samples) preserving exact class ratios.
3. **Pipeline Architecture:**
   - Numerical Transformer: `SimpleImputer(strategy='median')`
   - Categorical Transformer: `SimpleImputer(strategy='most_frequent')` + `OneHotEncoder(handle_unknown='ignore', sparse_output=False)`
   - Classifier: `RandomForestClassifier(n_estimators=100, max_depth=16, random_state=42, n_jobs=-1)`
4. **Model Reusability:** The fitted pipeline is serialized into `model.pkl` along with metadata, training metrics, and feature names.

---

## 📈 Model Performance & Evaluation

Tested on **25,976 unseen test samples**:

| Metric | Score | Note |
| :--- | :---: | :--- |
| **Accuracy** | **95.23%** | High overall classification precision |
| **Precision** | **96.37%** | Minimal false positive satisfaction classifications |
| **Recall** | **94.87%** | Captures 94.87% of all truly satisfied passengers |
| **F1-Score** | **95.61%** | Robust harmonic balance of precision and recall |
| **ROC-AUC** | **0.9922** | Near-optimal discriminatory power |

### Confusion Matrix:
```
                 Predicted Dissatisfied    Predicted Satisfied
True Dissatisfied         11,251 (TN)              508 (FP)
True Satisfied               730 (FN)           13,487 (TP)
```

---

## 🔍 Key Feature Importances

Top 10 drivers identified by the Random Forest model:
1. **Inflight entertainment** (`22.77%`)
2. **Seat comfort** (`15.35%`)
3. **Ease of Online booking** (`9.52%`)
4. **Online support** (`6.32%`)
5. **Food and drink** (`4.41%`)
6. **On-board service** (`4.01%`)
7. **Online boarding** (`3.79%`)
8. **Leg room service** (`3.45%`)
9. **Customer Type: Loyal Customer** (`3.43%`)
10. **Class: Business** (`2.68%`)

---

## 🖥️ Web Application Features

The modern Streamlit dashboard contains 5 dedicated sections:
1. **📊 Dashboard:** High-level project KPIs, dataset indicators, target distribution donut chart, travel class breakdown, and top drivers.
2. **🔍 Data Overview:** Dynamic data preview with row sliders, dataset diagnostics, missing values analysis, and interactive EDA visualizations.
3. **⚙️ Model Training:** Interactive training studio with sliders for hyperparameters (`n_estimators`, `max_depth`, `test_size`), real-time training progress, confusion matrix heatmap, and feature importance rankings.
4. **🔮 Prediction System:** Live prediction tool with quick presets ("Business Executive", "Frustrated Budget Flyer", "Average Traveler"), grouped input sliders, instant satisfaction probability gauge, and customized insight explanations.
5. **ℹ️ About Project:** Detailed technical documentation explaining the Random Forest mechanism, pipeline structure, and metric evaluations.

---

## 📁 Project Directory Structure

```
srika/
│
├── dataset/
│   └── Airline_customer_satisfaction.csv   # Dataset file (129,880 rows)
│
├── utils/
│   ├── __init__.py                         # Package initializer
│   └── preprocessing.py                    # Preprocessing pipeline, model training, evaluation & metrics
│
├── app.py                                  # Modern Streamlit web application
├── train_model.py                          # Standalone CLI training script
├── model.pkl                               # Serialized model & pipeline bundle
├── requirements.txt                        # Python dependencies
└── README.md                               # Project documentation
```

---

## ⚙️ Installation & Local Setup

### 1. Prerequisites
- Python 3.9+ or Anaconda environment installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Train the Model (Optional / Verification)
The model can be trained and evaluated via the command line:
```bash
python train_model.py
```
*Note: If `python` points to Anaconda, you can use: `& "C:\ProgramData\anaconda3\python.exe" train_model.py`.*

### 4. Launch the Web Application
```bash
streamlit run app.py
```

The application will launch in your browser at: `http://localhost:8501`

---

## 🎯 Usage Guide

1. **Viewing Dashboard:** Open `http://localhost:8501` and explore key metrics and overall distributions.
2. **Running Retraining:** Head over to **⚙️ Model Training**, adjust hyperparameters (e.g. 150 trees, max depth 18), and click **Train Random Forest Model**.
3. **Testing Live Predictions:**
   - Go to **🔮 Prediction System**.
   - Click one of the quick preset buttons (e.g., `🌟 Business Executive` or `⚠️ Frustrated Budget Flyer`) or enter custom ratings.
   - Click **⚡ Predict Passenger Satisfaction** to view the confidence score and contributing drivers.
