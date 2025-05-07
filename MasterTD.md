# Technical Documentation: Nigerian Farmer Synthetic Data Generator

## Overview

This `data_assets/generator.py` generates a comprehensive synthetic dataset of Nigerian farmers for alternative credit scoring and agricultural finance analysis. The dataset combines:

- Demographic information
- Farm characteristics and practices
- Financial data
- Credit assessment metrics
- Alternative data points for financial inclusion

## Core Data Categories

### 1. Farmer Demographics

- `farmer_id`: Unique identifier (NGF000001 format)
- `age`: Farmer age (16-65 years)
- `gender`: Male (75%) or Female (25%) distribution
- `education_category`: 8 levels from "No Formal Education" to "Masters/PhD"
- `marital_status`: Single, Married, Divorced, Widowed
- `household_size`: 1-14 members
- `state`: One of Nigeria's 36 states + FCT
- `region`: 6 geopolitical regions (North Central, North East, etc.)

### 2. Farm Characteristics

- `farm_size_ha`: 0.05-6ha (regionally varied, average ~1.28ha)
- `primary_crop`: Region-specific with national weighting (Cassava 46%, Maize 50%, etc.)
- `secondary_crop`: Secondary crop or "None"
- `farming_experience_years`: 1-45 years
- `land_acquisition_method`: Inheritance (65%), Purchase (8%), etc.
- `has_land_title`: True (10.7% male, 3.8% female managed plots)

### 3. Agricultural Practices

- `uses_fertilizer`: 35.4% adoption rate
- `uses_improved_seeds`: 10.1% adoption rate
- `uses_irrigation`: 2.2% of plots
- `pest_disease_control_method`: Modern, Organic, Traditional, etc.
- `yield_consistency_rating`: High, Medium, Low, Very Low
- `post_harvest_loss_perc`: 5-45% loss
- `uses_extension_services`: 20.7% participation

### 4. Livestock Data

- `owns_livestock`: 46.9% of households
- `livestock_type`: Goats (64.7%), Poultry (53.8%) most common
- `primary_livestock_use`: Sold Alive (62%), Savings/Insurance (21%), etc.
- Regional variations: NW highest livestock, SS highest fishing

### 5. Financial Data

- `annual_farm_revenue_ngn`: Calculated from yield × price
- `annual_farm_expenses_ngn`: Input costs + labor
- `farm_profit_ngn`: Revenue - Expenses
- `has_off_farm_income`: 45% of farmers
- `total_annual_income_ngn`: Farm + off-farm income
- `income_per_capita_ngn`: Income per household member

### 6. Asset Ownership

- `owns_tractor`: 0.1% (rare)
- `owns_plow`: 5.1%
- `owns_sprayer`: 14.2%
- `owns_cutlass`: 90.4% (very common)
- `has_storage_facility`: 35%
- `has_weather_insurance`: 5%

### 7. Financial Inclusion

- `has_bank_account`: 55%
- `has_formal_id`: 65%
- `smartphone_owner`: 60%
- `mobile_money_usage_frequency`: Daily, Weekly, etc.
- `digital_footprint_score_1_10`: Digital activity metric

### 8. Alternative Payment Data

- `utility_bill_payment_score_1_10`
- `mobile_money_activity_score_1_10`
- Payment timeliness metrics (utility, rent, phone)
- Last payment dates

### 9. Credit Assessment

- `credit_score`: 300-850 scale
- `creditworthiness_category`: Excellent to Very Poor
- `max_recommended_loan_ngn`: Based on capacity
- `suitable_loan_products`: Microfinance, Equipment Loan, etc.
- `predicted_default_probability`: 2-98% range

## Key Generation Logic

### Yield Calculation

```python
base_yield × education_factor × modern_practices_factor × experience_factor × random_factor
```

Modern practices include:

- Improved seeds (+15%)
- Fertilizer (+20%)
- Irrigation (+35%)
- Pest control (+10%)

### Credit Scoring (300-850)

Factors considered:

- Education level (+0-80)
- Financial inclusion (bank account +35)
- Farming experience (+0-30)
- Off-farm income (+50)
- Land tenure security (+10-40)
- Loan repayment history (-70 to +70)
- Digital footprint (+0-38)
- Profitability (+5 to +35)

### Loan Suitability

Products offered based on:

- Credit score thresholds
- Farm size
- Income level
- Digital capability

## Data Relationships

1. **Region → Crop Patterns**: Each region has specific crop weights
2. **Education → Yield**: Higher education improves yield potential
3. **Gender → Input Use**: Males use more inputs except seeds/labor
4. **Farm Size → Labor Costs**: Larger farms incur higher labor costs
5. **Digital Access → Financial Inclusion**: Smartphone owners have better access

## Validation Metrics

The generator maintains these statistical targets:

- Average farm size: ~1.28ha
- Fertilizer use: ~35%
- Improved seeds: ~10%
- Irrigation: ~2%
- Livestock ownership: ~47%
- Land titles: ~7% (male), ~4% (female)

## Output

CSV file with 10,000 records containing 80+ fields covering all aspects of farmer profiles, operations, and creditworthiness.

This dataset enables analysis of:

- Agricultural productivity drivers
- Financial inclusion gaps
- Alternative credit scoring models
- Input adoption patterns
- Regional variations in farming practices
