# 🌿 Farm Success Predictor

Predict a farmer’s credit score and creditworthiness using farm, financial, and demographic data.

---

## 🔍 Overview

This Streamlit application allows users to:
- **Manually input farm and personal details** OR
- **Upload a preprocessed CSV file** with encoded features

The model then predicts:
- A **credit score** (numeric)
- A **creditworthiness category**: _Poor_, _Fair_, or _Good_

---

## 📁 Project Structure

```
├── xgboost_credit_score_model.pkl
├── education_category_encoder.pkl
├── primary_crop_encoder.pkl
├── mobile_money_usage_frequency_encoder.pkl
├── creditworthiness_category_encoder.pkl
├── streamlit_app.py
```

---

## 🚀 How to Run

1. **Clone this repo**:
   ```bash
   git clone [URL]
   cd your-repo-name
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the app**:
   ```bash
   streamlit run streamlit_app.py
   ```

---

## 🧠 Model Details

- **Algorithm**: XGBoost Regression
- **Target**: Predicts numeric credit score
- **Input Features**: 27+ features including financial, farm-specific, and demographic data

---

## 🧾 Feature Descriptions

For detailed descriptions of all the features used by the model, [📄 click here to view the Feature Dictionary](https://docs.google.com/document/d/1f952T8SshQjFEVpDRrHSrurXQNAdqoJsnUpFOF7Bf38/edit?usp=sharing)

---

## 📥 CSV Upload Guidelines

Your CSV **must include all required columns** (already encoded). Make sure:
- Column names are **case-sensitive**
- Categorical fields are **already label-encoded**

---

## 🛠 Sample Input Fields

- Monthly mobile spend (₦)
- Post-harvest loss (%)
- Distance to market/bank (km)
- Mobile money usage frequency
- Education category
- Creditworthiness rating
- Smartphone ownership
- Land title status
- Household size

... and more!

---

## 🧑‍🌾 Built For

- Agricultural cooperatives  
- Microfinance institutions  
- Agri-fintech platforms  
- Rural data-driven solutions

