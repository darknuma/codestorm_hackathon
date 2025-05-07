# Technical Documentation: Synthetic Nigerian Farmer Credit Data Generation for `HELPER_DS.PY`

## 1. Purpose and Objectives

This documentation explains the technical rationale behind the synthetic farmer dataset generation script designed to support alternative credit scoring models for Nigerian agricultural finance. The system creates realistic but artificial data that mirrors:

- Traditional creditworthiness indicators from Nigerian agricultural studies
- Alternative financial behavior data points
- Agricultural operation characteristics
- Geographic distribution across Nigeria

This is for `data_assets/helper_ds.py`
**Version:** 1.0  
**Date:** May 6, 2025  
**Project Author:** Emmanuel Aminu  

## 2. Core Technical Decisions

### 2.1 Data Structure Design

**Rationale:**
The dataset schema combines three critical data dimensions identified in research:

1. **Demographic Factors** (Age, Education, Location)
   - Based on Cross River State study findings showing education level contributes 25% to creditworthiness
   - Age distribution follows Nigeria's agricultural workforce pyramid

2. **Financial Behaviors**
   - Utility payment patterns modeled after EFInA financial inclusion metrics
   - Mobile money usage reflects 45% penetration rate in rural Nigeria

3. **Agricultural Operations**
   - Crop types weighted by FAO Nigeria production statistics
   - Farm sizes follow smallholder dominance (87% <5ha)

**Implementation:**

```python
columns = [
    # Demographic
    'state', 'age', 'gender', 'education', 'household_size',
    
    # Agricultural
    'farm_size_hectares', 'primary_crop', 'livestock_type', 
    
    # Financial
    'utility_payment_score', 'mobile_money_usage',
    
    # Loan
    'loan_product_type', 'repayment_history'
]
```

### 2.2 Statistical Distributions

**Key Distributions:**

| Variable | Distribution Type | Parameters | Justification |
|----------|------------------|------------|---------------|
| Age | Uniform | min=18, max=65 | Matches working age population |
| Farm Size | Right-skewed normal | μ=2.5, σ=3.0 | Reflects smallholder dominance |
| Loan Repayment | Binomial | p=0.7 | Matches BOA's 68% repayment rate |
| Mobile Money Usage | Binomial | p=0.45 | EFInA 2022 penetration data |

**Implementation Example:**

```python
# Age follows working population distribution
age = random.randint(18, 65)

# Farm size follows right-skewed distribution
farm_size = abs(np.random.normal(2.5, 3.0))
farm_size = round(min(farm_size, 20), 2)  # Cap at 20ha
```

### 2.3 Alternative Data Integration

**Technical Approach:**

1. **Digital Footprint Proxy**:
   - Social media usage levels correlate with digital financial literacy
   - Ecommerce activity indicates market access

2. **Payment Behavior**:
   - Utility score modeled after FICO-like scoring (300-850 range)
   - Payment dates simulate real transaction timeliness

**Code Implementation:**

```python
# Digital behavior proxies
social_media_usage = random.choices(
    ['None', 'Low', 'Medium', 'High'],
    weights=[0.3, 0.4, 0.2, 0.1]
)[0]

# Payment behavior modeling
last_payment = fake.date_between(
    start_date=f'-{random.randint(1,90)}d', 
    end_date='today'
)
```

## 3. Agricultural Specifics

### 3.1 Crop and Livestock Distributions

**Data Sources:**

- FAO Nigeria crop production statistics
- National Agricultural Sample Survey 2019

**Implementation Logic:**

```python
# Weight crops by production prevalence
crops = ['Cassava', 'Maize', 'Rice', 'Yam', 'Sorghum']
weights = [0.35, 0.25, 0.2, 0.15, 0.05]  # Relative production volumes
primary_crop = random.choices(crops, weights=weights)[0]
```

### 3.2 Farm Size Categorization

**Technical Rationale:**
Categorization aligns with Nigerian agricultural standards:

| Category | Size Range | Population % |
|----------|-----------|--------------|
| Subsistence | <1ha | 62% |
| Small | 1-5ha | 25% |
| Medium | 5-10ha | 10% |
| Large | >10ha | 3% |

**Implementation:**

```python
bins = [0, 1, 5, 10, float('inf')]
labels = ['Subsistence', 'Small', 'Medium', 'Large']
df['farm_size_category'] = pd.cut(df['farm_size_hectares'], bins, labels)
```

## 4. Geographic Considerations

### 4.1 State-Level Distribution

**Technical Approach:**

- Uniform distribution across 36 states
- Implicit urban/rural weighting through state selection

```python
states = [
    'Lagos', 'Kano', ... # All 36 states
    ]
state = random.choice(states)
```

### 4.2 Location-Based Features

Derived variables:

- Distance to financial institutions (simulated)
- Market access potential

```python
# Simulate urban/rural access differences
if state in ['Lagos', 'Rivers', 'Abuja']:
    bank_distance = random.randint(1, 10)  # km
else:
    bank_distance = random.randint(5, 50)  # km
```

## 5. Validation Methodology

### 5.1 Statistical Validation

**Implemented Checks:**

1. Value ranges enforcement
2. Logical relationships (e.g., experience ≤ age-18)
3. Distribution adherence tests

```python
# Validation example
assert df['farming_experience_years'].max() <= df['age'].max() - 18
```

### 5.2 Business Rule Validation

Rules implemented:

- Minimum age for rent payments (22+)
- Cooperative members have repayment rates
- Loan amounts proportional to farm size

```python
df['last_rent_payment_date'] = df.apply(
    lambda x: fake.date_between('-60d', 'today') if x['age'] > 22 else None,
    axis=1
)
```

## 6. Limitations and Mitigations

**Known Limitations:**

1. **Correlation Structure**: Simplified relationships between variables
   - *Mitigation*: Added conditional probabilities for key relationships

2. **Temporal Patterns**: Static snapshot lacks historical depth
   - *Mitigation*: Included payment timing data

3. **Climate Factors**: Missing explicit climate risk metrics
   - *Mitigation*: Implicit through state-level variations

## 7. Usage Recommendations

### 7.1 Model Development

```python
# Recommended feature engineering
df['digital_footprint_score'] = (
    (df['social_media_usage'] != 'None') * 0.3 +
    df['ecommerce_activity'] * 0.2 +
    df['has_smartphone'] * 0.5
) * 100
```

### 7.2 Data Expansion

To enhance realism:

1. Integrate weather API data
2. Add crop price fluctuation patterns
3. Incorporate transportation cost variables

This technical approach provides a balanced synthetic dataset that maintains statistical validity while enabling innovative credit scoring model development for Nigerian agricultural finance.
