import streamlit as st
import pandas as pd
import joblib

# Load model and encoders
regression_model = joblib.load("xgboost_credit_score_model.pkl")
education_encoder = joblib.load("education_category_encoder.pkl")
primary_crop_encoder = joblib.load("primary_crop_encoder.pkl")
mobile_money_encoder = joblib.load("mobile_money_usage_frequency_encoder.pkl")
creditworthiness_encoder = joblib.load("creditworthiness_category_encoder.pkl")

# Features
all_features = [
    'monthly_mobile_spend_naira', 'post_harvest_loss_perc', 'distance_to_market_km', 'distance_to_bank_km',
    'percentage_sold_unprocessed', 'percentage_consumed', 'income_per_capita_ngn', 'annual_farm_revenue_ngn',
    'annual_farm_yield_tons_per_ha', 'farm_size_ha', 'farming_experience_years', 'age', 'education_category',
    'primary_crop', 'mobile_money_usage_frequency', 'creditworthiness_category', 'mobile_money_activity_score_1_10',
    'cooperative_repayment_rate_percent', 'prior_loan_repayment_rate', 'has_off_farm_income', 'gender',
    'has_land_title', 'has_weather_insurance', 'smartphone_owner', 'cooperative_member', 'has_prior_loan',
    'household_size'
]

# Default values
default_values = {
    'post_harvest_loss_percentage': 5,
    'distance_to_market_km': 0.5,
    'distance_to_bank_km': 1,
    'percentage_sold_unprocessed': 0,
    'percentage_consumed': 0,
    'income_per_capita_ngn': 2769,
    'annual_farm_revenue_ngn': 36000,
    'annual_farm_yield_tons_per_ha': 0.45,
    'mobile_money_usage_frequency': 2,
    'creditworthiness_category': 2,
    'cooperative_repayment_rate_percent': 0,
    'prior_loan_repayment_rate': 0,
    'household_size': 1,
    'monthly_mobile_spend_naira': 100,
    'age': 16,
    'farm_size_ha': 0.1,
    'farming_experience_years': 1
}

# Safe encoder transformation
def safe_transform(encoder, value):
    try:
        return encoder.transform([value])[0]
    except ValueError:
        return -1

# Categorize credit score
def categorize_credit_score(score):
    if score < 564:
        return 'Poor'
    elif score < 650:
        return 'Fair'
    else:
        return 'Good'

# Get user input
def get_user_input():
    input_data = {}

    education_options = [
        'No Formal Education', 'Primary Incomplete', 'Primary Complete',
        'Secondary Incomplete', 'Secondary Complete', 'OND/NCE',
        'HND/BSc', 'Masters/PhD'
    ]

    input_data['household_size'] = st.slider("Household Size (1-14)", 1, 14, 1)
    input_data['mobile_money_activity_score_1_10'] = st.slider("Mobile Money Activity Score (1-10)", 1, 10, 5)

    input_data['education_category'] = st.selectbox("Education Level", education_options)
    input_data['primary_crop'] = st.selectbox("Primary Crop", ['Maize', 'Cassava', 'Yam', 'Rice'])
    input_data['creditworthiness_category'] = st.selectbox(
        "Creditworthiness Category",
        ["Very Poor", "Poor", "Fair", "Good", "Very Good", "Excellent"],
        index=2
    )
    mobile_money_usage_options = ['Never', 'Rarely', 'Monthly', 'Weekly', 'Daily']
    input_data['mobile_money_usage_frequency'] = st.selectbox("Mobile Money Usage Frequency", mobile_money_usage_options)

    input_data['education_category'] = safe_transform(education_encoder, input_data['education_category'])
    input_data['primary_crop'] = safe_transform(primary_crop_encoder, input_data['primary_crop'])
    input_data['creditworthiness_category'] = safe_transform(creditworthiness_encoder, input_data['creditworthiness_category'])
    input_data['mobile_money_usage_frequency'] = safe_transform(mobile_money_encoder, input_data['mobile_money_usage_frequency'])

    input_data['has_land_title'] = int(st.checkbox("Do you have a land title?", False))
    input_data['has_weather_insurance'] = int(st.checkbox("Do you have weather insurance?", False))
    input_data['smartphone_owner'] = int(st.checkbox("Do you own a smartphone?", True))
    input_data['cooperative_member'] = int(st.checkbox("Are you a member of a cooperative?", False))
    input_data['has_prior_loan'] = int(st.checkbox("Have you taken a prior loan?", False))
    input_data['has_off_farm_income'] = int(st.checkbox("Do you have off-farm income?", False))

    input_data['gender'] = int(st.radio("Gender", ['Male', 'Female']) == 'Male')

    for feature in all_features:
        if feature in input_data or feature in ['education_category', 'primary_crop', 'creditworthiness_category', 'gender']:
            continue
        default = default_values.get(feature, 0.0)
        input_data[feature] = st.number_input(f"{feature.replace('_', ' ').title()}", value=float(default))

    return pd.DataFrame([input_data])

# Streamlit app
st.title("🌿 Farm Success Predictor")
st.write("Predict farm revenue and credit score category based on farm and demographic data.")

input_mode = st.sidebar.radio("Choose Input Mode", ["Manual Input", "Upload CSV"])

if input_mode == "Manual Input":
    input_df = get_user_input()
    trained_features = regression_model.get_booster().feature_names
    input_features = input_df.columns.tolist()

    missing_features = set(trained_features) - set(input_features)
    extra_features = set(input_features) - set(trained_features)

    if missing_features or extra_features:
        st.write(f"Missing Features: {missing_features}")
        st.write(f"Extra Features: {extra_features}")
    else:
        input_df = input_df[trained_features]
        if st.button("Predict"):
            prediction = regression_model.predict(input_df)[0]
            prediction = round(prediction)
            category = categorize_credit_score(prediction)

            st.success(f"📈 Predicted Farm Credit Score: **{prediction}**")
            st.info(f"📊 Creditworthiness Category: **{category}**")

else:
    uploaded_file = st.file_uploader("Upload CSV file with all required columns (without credit_score)", type=["csv"])
    if uploaded_file is not None:
        data_csv = pd.read_csv(uploaded_file)
        st.write("📄 Preview of uploaded data:", data_csv.head())
        if st.button("Predict Batch"):
            predictions = regression_model.predict(data_csv)
            predictions_rounded = [round(p) for p in predictions]
            categories = [categorize_credit_score(p) for p in predictions_rounded]

            output_df = data_csv.copy()
            output_df['Predicted_Credit_Score'] = predictions_rounded
            output_df['Creditworthiness_Category'] = categories

            st.write("📊 Batch Predictions Preview:", output_df.head())

            csv = output_df.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Download Predictions as CSV", data=csv, file_name="credit_score_predictions.csv", mime='text/csv')
