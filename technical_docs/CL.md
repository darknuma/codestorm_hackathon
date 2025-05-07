# Technical Documentation: Nigerian Young Farmers Credit Dataset Generator for `HELPER_CL.PY`

## 1. Overview

This Python script for `data_assets/helper_cl.py` generates a synthetic dataset of 4,000 young Nigerian farmers (ages 18-45) with comprehensive financial, agricultural, and credit-related attributes. The dataset is designed for developing alternative credit scoring models tailored to agricultural lending in Nigeria.

**Version:** 1.0  
**Date:** May 6, 2025  
**Project Author:** Emmanuel Aminu  

## 2. Key Features

- **Geographic Distribution**: Covers all 36 Nigerian states across 6 geopolitical regions
- **Agricultural Specifics**: Crop types, farm sizes, and yields vary by region
- **Financial Inclusion**: Captures both formal and informal financial behaviors
- **Credit Assessment**: Includes calculated credit scores and default probabilities
- **Loan Product Matching**: Recommends suitable financial products per farmer

## 3. Data Structure

### 3.1 Core Attributes

| Category | Variables | Description |
|----------|----------|-------------|
| **Demographics** | `gender`, `age`, `state`, `region`, `education_level` | Basic farmer characteristics |
| **Farm Operations** | `primary_crop`, `farm_size_hectares`, `years_farming_experience`, `yield_tons_per_hectare` | Agricultural production details |
| **Financial** | `annual_farm_revenue`, `annual_off_farm_income`, `total_annual_income`, `farm_profit` | Income and profitability metrics |
| **Financial Access** | `has_bank_account`, `has_formal_id`, `mobile_money_activity_score`, `distance_to_bank_km` | Financial inclusion indicators |
| **Credit History** | `has_prior_loan`, `loan_amount`, `loan_repayment_rate`, `loan_repayment_history` | Previous borrowing behavior |
| **Credit Assessment** | `credit_score`, `creditworthiness`, `default_probability`, `max_recommended_loan` | Calculated credit metrics |
| **Loan Products** | `suitable_loan_products` | Recommended financial products |

### 3.2 Calculated Fields

1. **Credit Score (300-850 range)**
   - Incorporates 25+ factors including education, financial access, farming practices, and repayment history
   - Weighted formula based on Nigerian agricultural lending research

2. **Default Probability**
   - Bayesian-style calculation considering:
     - Credit score
     - Income stability
     - Farming practices
     - Social capital (cooperative membership)
     - Historical repayment

3. **Suitable Loan Products**
   - Rules-based recommendations considering:
     - Creditworthiness tier
     - Farm size
     - Income level
     - Digital readiness

## 4. Technical Implementation

### 4.1 Core Dependencies

```python
import pandas as pd
import numpy as np
import random
from faker import Faker
```

### 4.2 Data Generation Logic

#### Regional Variations

```python
# Region-specific crop distributions
crops_by_region = {
    'North Central': ['Maize', 'Rice', 'Yam', 'Cassava', 'Sorghum', 'Millet', 'Cowpea'],
    # ... other regions ...
}

# Region-appropriate farm sizes
farm_size_ranges = {
    'North Central': (0.5, 5),  # hectares
    # ... other regions ...
}
```

#### Yield Calculations

```python
def calculate_yield(row):
    base = base_yields[row['primary_crop']]
    education_factor = {'No Formal Education':0.8, 'Primary':0.9, ...}
    modern_practices_factor = 1.0 + improvements
    return base * education_factor * modern_practices_factor * ...
```

#### Credit Scoring Model

```python
def calculate_credit_score(row):
    score = 400  # Base
    # Education points
    score += education_points[row['education_level']]
    # Financial inclusion
    if row['has_bank_account']: score += 30
    # ... 15 additional factors ...
    return max(300, min(850, score))
```

### 4.3 Statistical Distributions

| Variable | Distribution Type | Parameters | Justification |
|----------|------------------|------------|---------------|
| Age | Uniform | 18-45 | Young farmer focus |
| Education | Categorical | [15%, 30%,40%,15%] | National literacy rates |
| Farm Size | Region-based ranges | Varies | FAO smallholder data |
| Credit Score | Composite formula | 300-850 | FICO-like scale |

## 5. Usage Examples

### 5.1 Loading the Data

```python
df = pd.read_csv('nigerian_young_farmers_data.csv')
```

### 5.2 Credit Risk Modeling

```python
from sklearn.ensemble import RandomForestClassifier

X = df[['credit_score', 'default_probability', 'farm_profit', ...]]
y = df['loan_repayment_history_encoded']

model = RandomForestClassifier()
model.fit(X_train, y_train)
```

### 5.3 Loan Product Recommendation Engine

```python
def recommend_products(farmer_profile):
    products = []
    if farmer_profile['credit_score'] >= 600:
        products.append('Equipment Loan')
    # ... other rules ...
    return products
```

## 6. Validation Methodology

### 6.1 Statistical Checks

```python
assert df['years_farming_experience'].max() <= df['age'].max() - 18
assert df['credit_score'].between(300, 850).all()
```

### 6.2 Business Logic Validation

- Farm revenue >= production * crop prices
- Loan amounts <= recommended maximum
- Default probability inversely correlates with credit score

## 7. Limitations

1. **Synthetic Nature**: Data patterns are simulated not observed
2. **Climate Factors**: No explicit climate risk modeling
3. **Market Dynamics**: Fixed crop prices don't reflect volatility

## 8. Future Enhancements

1. Integrate real weather data APIs
2. Add temporal dimensions for historical trends
3. Incorporate supply chain relationships
4. Add mobile money transaction simulations

This dataset provides a robust foundation for developing agricultural credit scoring models that combine traditional financial metrics with alternative data sources relevant to Nigerian smallholder farmers
