# 📝 Final Report: Creditworthiness & Farm Business Success Prediction

## 📌 Project Overview

This project addresses the challenge of assessing **creditworthiness** and **farm business viability** among rural farmers. By using machine learning, we developed robust predictive models to:

* **Classify** farmers into credit score categories.
* **Predict** key business success metrics like income or revenue.

The dual-model approach offers practical insights for financial institutions, NGOs, or agri-tech platforms aiming to make **data-driven lending or support decisions**.

---

## 📊 Dataset Summary

* **Total records**: 10,000+
* **Key Features**:

  * `monthly_mobile_spend_naira`, `farm_size_ha`, `income_per_capita_ngn`, `annual_farm_revenue_ngn`, etc.
* **Target Variables**:

  * Regression: *e.g.*, `income_per_capita_ngn`
  * Classification: `creditworthiness_category` (0 = Very Poor to 5 = Excellent)

---

## 🔍 Data Preprocessing

* **Missing Values**: Handled appropriately.
* **Encoding**: If needed for categorical variables.
* **Feature Selection**: Top features retained after correlation check.
* **Data Leakage Prevention**: Ensured no target-derived features are used as inputs.

---

## ⚙️ Modeling

### 🔹 Regression Models (Business Success Prediction)

| Algorithm               | R² Score  | MAE       | RMSE      |
| ----------------------- | --------- | --------- | --------- |
| Random Forest Regressor | 0.70      | \~29.00   | \~36.25   |
| Gradient Boosting       | 0.76      | \~26.00   | \~32.49   |
| XGBoost Regressor       | **0.763** | **25.81** | **32.30** |

> **Best Model**: XGBoost Regressor (after hyperparameter tuning)

---

## 🔎 Feature Importance

Top predictors identified using model's `.feature_importances_`:

* `income_per_capita_ngn`
* `annual_farm_yield_tons_per_ha`
* `distance_to_market_km`
* `farm_size_ha`
* `monthly_mobile_spend_naira`

These features are highly interpretable and support domain understanding.

---

## 🖥️ Streamlit App Features

* **Dual Mode**:

  * Classification: Predict creditworthiness category.
  * Regression: Predict income or revenue.
* **User Input**: Farmers can input features like farm size, income, spend, etc.
* **Model Output**: Shows prediction + model confidence.
* **Export Options**: Predictions can be downloaded or saved.

---

## ✅ Key Achievements

* Built high-performance ML models for both regression and classification tasks.
* Achieved strong generalization without data leakage or overfitting.
* Integrated models into an interactive, user-friendly Streamlit application.

---

## 🚀 Future Improvements

* Add SHAP or LIME explanations for transparency.
* Add user authentication and database logging in the app.
* Explore ensemble models or stacking.
* Test on real-world unseen data for robustness.

