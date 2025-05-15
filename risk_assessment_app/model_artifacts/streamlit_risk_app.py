import streamlit as st
import pandas as pd
import numpy as np
import joblib
import shap
import matplotlib.pyplot as plt
import os

# --- Configuration & Load Artifacts ---

PREPROCESSOR_PATH = "./preprocessor.joblib"
FEATURE_NAMES_PATH = "./feature_names.joblib"
MODEL_PATH = "./xgb_risk_model.joblib"
MITIGATION_KB_PATH="./mitigation_kb.joblib"
ORIGINAL_COLUMNS_PATH="./original_columns.joblib"


# Function to load artifacts safely
def load_artifacts():
    try:
        model = joblib.load(MODEL_PATH)
        preprocessor = joblib.load(PREPROCESSOR_PATH)
        processed_feature_names = joblib.load(FEATURE_NAMES_PATH)
        mitigation_kb = joblib.load(MITIGATION_KB_PATH)
        original_input_columns = joblib.load(ORIGINAL_COLUMNS_PATH)
        return model, preprocessor, processed_feature_names, mitigation_kb, original_input_columns
    except FileNotFoundError as e:
        st.error(f"Error loading model artifacts: {e}. Ensure training script has been run.")
        return None, None, None, None, None

xgb_model, preprocessor, processed_feature_names, mitigation_kb, original_input_columns = load_artifacts()

explainer = None
if xgb_model:
    try:
        explainer = shap.TreeExplainer(xgb_model)
    except Exception as e:
        st.warning(f'Could not initialize SHAP explainer: {e}')

artifacts_to_check = [
    xgb_model,
    preprocessor,
    processed_feature_names,
    mitigation_kb,
    original_input_columns
]

if any(artifact is None for artifact in artifacts_to_check):
    st.error("Critical Error: One or more model artifacts failed to load. "
             "Please ensure all artifact files (xgb_risk_model.joblib, preprocessor.joblib, "
             "feature_names.joblib, mitigation_kb.joblib, original_columns.joblib) "
             "are present in the correct 'model_artifacts' and 'risk_assessment_app/model_artifacts' directories "
             "and that the training script has been run successfully to generate them.")
    st.stop()


# --- Streamlit App UI ---
st.set_page_config(layout='wide')
st.title('🌿 Farmer Loan Default Risk Assessment & Mitigation Advisor')
st.markdown("""
This tool uses an XGBoost machine learning model to predict the likelihood of loan default 
for a farmer and suggests potential mitigation strategies based on identified risk factors.
Fill in the farmer's details below to get an assessment.
""")


# --- Input Form ---
st.sidebar.header('Farmer Data Input')


EDUCATION_CATEGORIES = [
	'No Formal Education',
	'Primary Incomplete',
	'Primary Complete',
	'Secondary Incomplete',
	'Secondary Complete',
	'OND/NCE',
	'HND/BSc',
	'Masters/PhD',
]
MARITAL_STATUSES = ['Single', 'Married', 'Divorced', 'Widowed']
LAND_ACQUISITION_METHODS = [
	'Inheritance',
	'Family Owned',
	'Purchased',
	'Leased',
	'Community Land',
	'Rented',
	'Gift',
]
ALL_CROPS = [
	'Maize',
	'Cassava',
	'Yam',
	'Rice',
	'Sorghum',
	'Millet',
	'Cowpea',
	'Beans',
	'Groundnut',
	'Cotton',
	'Vegetables',
	'Oil Palm',
	'Plantain',
	'Cocoa',
	'Rubber',
	'Soybean',
	'Sesame',
	'Tomato',
	'Guinea Corn',
	'None',
]  # Added None
LIVESTOCK_TYPES = [
	'Poultry',
	'Goats',
	'Sheep',
	'Cattle',
	'Pigs',
	'Fish Farming',
	'Ducks',
	'Guinea Fowl',
	'None',
]
PEST_DISEASE_CONTROL_METHODS = [
	'Modern Chemical',
	'Organic',
	'Traditional',
	'Integrated Pest Management',
	'None',
]
YIELD_CONSISTENCY_RATINGS = ['High', 'Medium', 'Low', 'Very Low']
MOBILE_MONEY_USAGE_FREQUENCIES = ['Daily', 'Weekly', 'Monthly', 'Rarely', 'Never']
SOCIAL_MEDIA_USAGE_CATS = ['None', 'Low', 'Medium', 'High']
UTILITY_PAYMENT_TIMELINESS_CATS = ['Excellent', 'Good', 'Fair', 'Poor', 'N/A']  # Added N/A for rent
LOAN_PURPOSES = [
	'Input Loan',
	'Mechanization Loan',
	'Bundled Services Loan',
	'Working Capital',
	'Asset Acquisition',
	'Land Expansion',
	'Processing Equipment',
	'Storage Construction',
]
PRIOR_LOAN_REPAYMENT_HISTORY_CATS = ['None', 'Poor', 'Fair', 'Good', 'Excellent']

EDUCATION_YEARS_MAP = {
    'No Formal Education': 0,
    'Primary Incomplete': 3,    
    'Primary Complete': 6,
    'Secondary Incomplete': 9,  
    'Secondary Complete': 12,
    'OND/NCE': 14,
    'HND/BSc': 16,
    'Masters/PhD': 18         
}



input_data = {}
with st.sidebar.form('farmer_input_form'):
	st.write('**Demographics & General Info:**')
	input_data['age'] = st.number_input('Age', min_value=18, max_value=100, value=35, step=1)
	input_data['gender'] = st.selectbox('Gender', ['Male', 'Female'])
	input_data['education_category'] = st.selectbox(
		'Education Category', EDUCATION_CATEGORIES, index=2
	)
	selected_education_category = input_data.get('education_category') 
	input_data['education_level_years'] = EDUCATION_YEARS_MAP.get(selected_education_category, 0) # Default to 0 if category not found
	input_data['marital_status'] = st.selectbox('Marital Status', MARITAL_STATUSES, index=1)
	input_data['household_size'] = st.number_input(
		'Household Size', min_value=1, max_value=20, value=5, step=1
	)

	st.write('**Farm Characteristics & Practices:**')
	input_data['farming_experience_years'] = st.number_input(
		'Farming Experience (Years)', min_value=0, max_value=60, value=10, step=1
	)
	input_data['farm_size_ha'] = st.number_input(
		'Farm Size (Hectares)', min_value=0.05, max_value=100.0, value=1.5, step=0.1, format='%.2f'
	)
	farm_size_ha_value = input_data.get('farm_size_ha', 0.0)  
	def categorize_farm_size(ha):
		if ha < 1: 
			return 'Small (<1ha)'
		elif ha < 5:
			return 'Medium (1-5ha)'
		elif ha < 20:
			return 'Large (5-20ha)'
		else:
			return 'Very Large (20ha+)'

	input_data['farm_size_category'] = categorize_farm_size(farm_size_ha_value)
	input_data['land_acquisition_method'] = st.selectbox(
		'Land Acquisition Method', LAND_ACQUISITION_METHODS, index=0
	)
	input_data['has_land_title'] = st.checkbox('Has Land Title?', value=False)
	input_data['primary_crop'] = st.selectbox('Primary Crop', ALL_CROPS, index=0)
	input_data['secondary_crop'] = st.selectbox(
		'Secondary Crop', ALL_CROPS, index=len(ALL_CROPS) - 1
	)  # Default to 'None'
	
    
	input_data['owns_livestock'] = st.checkbox('Owns Livestock?', value=True)
	input_data['livestock_type'] = st.selectbox('Livestock Type (if any)', LIVESTOCK_TYPES, index=0)
	LIVESTOCK_USES = [
        'Meat', 'Milk', 'Eggs', 'Draught/Labour', 'Manure', 
        'Breeding', 'Combination', 'Pets', 'None/Not Applicable' 
    ]
	input_data['primary_livestock_use'] = st.selectbox(
        'Primary Use of Livestock (if any)', 
        LIVESTOCK_USES, 
        index=LIVESTOCK_USES.index('None/Not Applicable') # Sensible default
    )
	
	input_data['uses_improved_seeds'] = st.checkbox(
		'Uses Improved Seeds?', value=False
	)  # Default based on low national average
	input_data['uses_fertilizer'] = st.checkbox(
		'Uses Fertilizer?', value=False
	)  # Default based on low national average
	input_data['uses_irrigation'] = st.checkbox(
		'Uses Irrigation?', value=False
	)  # Default based on very low national average
	input_data['pest_disease_control_method'] = st.selectbox(
		'Pest/Disease Control Method', PEST_DISEASE_CONTROL_METHODS, index=0
	)
	input_data['soil_type_known'] = st.checkbox('Soil Type Known?', value=True)
	input_data['uses_extension_services'] = st.checkbox('Uses Extension Services?', value=False)

	st.write('**Production & Financials (Annual Estimates):**')
	input_data['annual_farm_yield_tons_per_ha'] = st.number_input(
		'Annual Farm Yield (tons/ha)', min_value=0.0, value=2.5, step=0.1, format='%.2f'
	)
	input_data['total_production_tons'] = st.number_input(
		'Total Production (tons)', min_value=0.0, value=3.75, step=0.1, format='%.2f'
	)  # Example: 1.5ha * 2.5t/ha
	input_data['crop_price_per_ton_ngn'] = st.number_input(
		'Avg. Crop Price (NGN/ton)', min_value=0, value=150000, step=1000
	)
	input_data['annual_farm_revenue_ngn'] = st.number_input(
		'Annual Farm Revenue (NGN)', min_value=0, value=500000, step=10000
	)
	input_data['annual_farm_expenses_ngn'] = st.number_input(
		'Annual Farm Expenses (NGN)', min_value=0, value=250000, step=10000
	)
	input_data['farm_profit_ngn'] = st.number_input(
		'Farm Profit (NGN)', value=250000, step=10000
	)  # Auto-calculate or input
	input_data['has_off_farm_income'] = st.checkbox('Has Off-Farm Income?', value=True)
	input_data['annual_off_farm_income_ngn'] = st.number_input(
		'Annual Off-Farm Income (NGN)', min_value=0, value=100000, step=5000
	)
	input_data['total_annual_income_ngn'] = st.number_input(
		'Total Annual Income (NGN)', value=600000, step=10000
	)  # Auto-calculate or input
	input_data['income_per_capita_ngn'] = st.number_input(
		'Income Per Capita (NGN)', value=120000, step=1000
	)  # Auto-calculate or input

	input_data['yield_consistency_rating'] = st.selectbox(
		'Yield Consistency Rating', YIELD_CONSISTENCY_RATINGS, index=1
	)
	input_data['post_harvest_loss_perc'] = st.number_input(
		'Post-Harvest Loss (%)', min_value=0.0, max_value=100.0, value=15.0, step=0.5, format='%.1f'
	)
	input_data['percentage_sold_unprocessed'] = st.number_input(
		'Percentage of Crop Sold Unprocessed (%)',
		min_value=0.0,
		max_value=100.0,
		value=60.0,
		step=1.0,
		format='%.1f',
	)
	input_data['percentage_consumed'] = st.number_input(
		'Percentage of Crop Consumed by Household (%)',
		min_value=0.0,
		max_value=100.0,
		value=30.0,
		step=1.0,
		format='%.1f',
	)

	st.write('**Assets & Risk Mitigation:**')
	input_data['has_storage_facility'] = st.checkbox('Has Storage Facility?', value=False)
	input_data['has_weather_insurance'] = st.checkbox('Has Weather Insurance?', value=False)
	# Simplified asset ownership for the form
	input_data['owns_sprayer'] = st.checkbox('Owns Sprayer?', value=False)
	input_data['owns_wheelbarrow'] = st.checkbox('Owns Wheelbarrow?', value=True)
	input_data['owns_cutlass'] = st.checkbox('Owns Cutlass?', value=True)
	# Not including tractor, plow, sickle for form simplicity, but they are in the training data
	# Add them if they were highly important features

	st.write('**Financial Inclusion & Digital Footprint:**')
	input_data['has_bank_account'] = st.checkbox('Has Bank Account?', value=True)
	input_data['has_formal_id'] = st.checkbox('Has Formal ID?', value=True)
	input_data['smartphone_owner'] = st.checkbox('Owns Smartphone?', value=True)
	input_data['mobile_money_usage_frequency'] = st.selectbox(
		'Mobile Money Usage Frequency', MOBILE_MONEY_USAGE_FREQUENCIES, index=2
	)
	input_data['monthly_mobile_spend_naira'] = st.number_input(
		'Monthly Mobile Spend (NGN)', min_value=0, value=1500, step=100
	)
	input_data['social_media_usage'] = st.selectbox(
		'Social Media Usage', SOCIAL_MEDIA_USAGE_CATS, index=1
	)
	input_data['ecommerce_activity'] = st.checkbox('Engages in E-commerce Activity?', value=False)
	input_data['active_on_agri_forums'] = st.checkbox('Active on Agri Forums?', value=False)
	input_data['digital_footprint_score_1_10'] = st.slider(
		'Digital Footprint Score (1-10)', 1, 10, value=5
	)

	st.write('**Alternative Payment Data:**')
	input_data['utility_bill_payment_score_1_10'] = st.slider(
		'Utility Bill Payment Score (1-10)', 1, 10, value=7
	)
	input_data['mobile_money_activity_score_1_10'] = st.slider(
		'Mobile Money Activity Score (1-10)', 1, 10, value=6
	)
	input_data['utility_payment_timeliness'] = st.selectbox(
		'Utility Payment Timeliness', UTILITY_PAYMENT_TIMELINESS_CATS, index=1
	)
	input_data['rent_payment_timeliness'] = st.selectbox(
		'Rent Payment Timeliness', UTILITY_PAYMENT_TIMELINESS_CATS, index=1
	)  # Assuming 'N/A' handled if not applicable
	input_data['phone_bill_timeliness'] = st.selectbox(
		'Phone Bill Timeliness', UTILITY_PAYMENT_TIMELINESS_CATS, index=0
	)

	st.write('**Social Capital & Value Chain:**')
	input_data['cooperative_member'] = st.checkbox('Cooperative Member?', value=True)
	input_data['cooperative_repayment_rate_percent'] = st.number_input(
		'Cooperative Repayment Rate (%)',
		min_value=0,
		max_value=100,
		value=85,
		step=1,
		disabled=not input_data['cooperative_member'],
	)
	input_data['value_chain_platform_registered'] = st.checkbox(
		'Registered on Value Chain Platform?', value=False
	)
	input_data['years_on_platform'] = st.number_input(
		'Years on Platform',
		min_value=0,
		max_value=10,
		value=0,
		step=1,
		disabled=not input_data['value_chain_platform_registered'],
	)
	input_data['marketplace_sales_ngn_last_year'] = st.number_input(
		'Marketplace Sales Last Year (NGN)',
		min_value=0,
		value=0,
		step=1000,
		disabled=not input_data['value_chain_platform_registered'],
	)

	st.write('**Logistics:**')
	input_data['distance_to_market_km'] = st.number_input(
		'Distance to Market (km)', min_value=0.0, value=10.0, step=0.5, format='%.1f'
	)
	input_data['distance_to_bank_km'] = st.number_input(
		'Distance to Bank (km)', min_value=0.0, value=15.0, step=0.5, format='%.1f'
	)

	st.write('**Loan History & Current Request:**')
	input_data['has_prior_loan'] = st.checkbox('Has Prior Loan?', value=False)
	input_data['prior_loan_amount_ngn'] = st.number_input(
		'Prior Loan Amount (NGN)',
		min_value=0,
		value=0,
		step=1000,
		disabled=not input_data['has_prior_loan'],
	)
	input_data['prior_loan_repayment_rate'] = st.number_input(
		'Prior Loan Repayment Rate (0.0-1.0)',
		min_value=0.0,
		max_value=1.0,
		value=0.0,
		step=0.01,
		format='%.2f',
		disabled=not input_data['has_prior_loan'],
	)
	input_data['prior_loan_repayment_history'] = st.selectbox(
		'Prior Loan Repayment History',
		PRIOR_LOAN_REPAYMENT_HISTORY_CATS,
		index=0,
		disabled=not input_data['has_prior_loan'],
	)
	input_data['prior_loan_purpose'] = st.selectbox(
		'Prior Loan Purpose',
		LOAN_PURPOSES + ['N/A'],
		index=len(LOAN_PURPOSES),
		disabled=not input_data['has_prior_loan'],
	)

	# Current loan details (features for the model)
	input_data['loan_amount_requested_ngn'] = st.number_input(
		'Current Loan Amount Requested (NGN)', min_value=10000, value=200000, step=10000
	)
	input_data['current_loan_purpose'] = st.selectbox(
		'Current Loan Purpose', LOAN_PURPOSES, index=0
	)
	input_data['current_loan_tenure_months'] = st.selectbox(
		'Current Loan Tenure (Months)', [3, 6, 9, 12, 18, 24, 36], index=2
	)

	# For this example, we assume the form covers the key ones used by the model.
	# If 'owns_tractor', 'owns_plow', 'owns_sickle' were important, they'd need to be added to the form or defaulted.
	# For now, we'll add them with default False if not in form.
	for col in original_input_columns:
		if col not in input_data:
			if col in [
				'owns_tractor',
				'owns_plow',
				'owns_sickle',
			]:  # Example default for missing booleans
				input_data[col] = False
			# Add other default logic if needed for other missing columns
			# else:
			#    input_data[col] = 0 # Default for other missing numerics, or handle appropriately

	submitted = st.form_submit_button('Assess Farmer Risk')


# --- Prediction and Mitigation Logic ---
if submitted:
	st.subheader('Risk Assessment Results')
	try:
		# Create DataFrame in the order of original_input_columns
		input_df_ordered = pd.DataFrame([input_data])[original_input_columns]

		# Convert boolean looking columns that might be True/False from checkboxes to int
		for col in input_df_ordered.columns:
			if input_df_ordered[col].dtype == 'bool':
				input_df_ordered[col] = input_df_ordered[col].astype(int)

		# Preprocess the input data
		input_processed = preprocessor.transform(input_df_ordered)
		input_processed_df = pd.DataFrame(input_processed, columns=processed_feature_names)

		# Make prediction
		prediction = xgb_model.predict(input_processed_df)[0]
		prediction_proba = xgb_model.predict_proba(input_processed_df)[0][
			1
		]  # Probability of high risk (class 1)

		risk_status = 'High Risk' if prediction == 1 else 'Lower Risk'
		st.metric(
			label='Predicted Risk Status',
			value=risk_status,
			delta=f'{prediction_proba:.2%} probability of being High Risk',
		)

		if risk_status == 'High Risk' and explainer:
			st.subheader('Key Factors Contributing to High Risk (SHAP Analysis)')

			current_shap_values = explainer.shap_values(input_processed_df)
			if isinstance(
				current_shap_values, list
			):  # For binary classification, shap_values can be a list of two arrays
				current_shap_values = current_shap_values[
					1
				]  # Values for the positive class (High Risk)

			shap_df = pd.DataFrame(
				{
					'feature': processed_feature_names,
					'shap_value': current_shap_values.flatten(),
					'feature_value_processed': input_processed_df.iloc[0].values.flatten(),
				}
			)

			# Get original values for display
			original_values_for_shap = []
			for feature_name_processed in processed_feature_names:
				original_col_candidate = (
					feature_name_processed.split('__')[0]
					if '__' in feature_name_processed
					else feature_name_processed
				)
				if original_col_candidate in input_df_ordered.columns:
					original_values_for_shap.append(
						input_df_ordered[original_col_candidate].iloc[0]
					)
				else:
					original_values_for_shap.append('N/A (Processed Feature)')

			shap_df['feature_value_original'] = original_values_for_shap

			# Features that pushed the score towards high risk (positive SHAP values)
			risk_driving_features = shap_df[shap_df['shap_value'] > 0.01].sort_values(
				by='shap_value', ascending=False
			)  # Threshold for SHAP impact

			if not risk_driving_features.empty:
				# Display SHAP Waterfall plot for the single prediction
				# Create a SHAP Explanation object for a single instance
				shap_explanation = shap.Explanation(
					values=current_shap_values.flatten(),  # Use SHAP values for the predicted class
					base_values=explainer.expected_value[1]
					if isinstance(explainer.expected_value, list)
					else explainer.expected_value,  # Base value for the predicted class
					data=input_processed_df.iloc[0].values.flatten(),  # Processed feature values
					feature_names=processed_feature_names,
				)
				fig, ax = plt.subplots(figsize=(10, 6))
				shap.plots.waterfall(shap_explanation, max_display=10, show=False)
				st.pyplot(fig)
				plt.close(fig)

				st.subheader('Suggested Mitigation Strategies')
				suggested_count = 0
				for _, row_shap in risk_driving_features.head(5).iterrows():  # Show top 5 drivers
					if suggested_count >= 3:
						break  # Max 3 suggestions

					feature_name_processed = row_shap['feature']
					strategy = None
					display_feature_name = feature_name_processed  

					# 1. Direct match for processed feature name (e.g. one-hot encoded)
					if feature_name_processed in mitigation_kb:
						strategy = mitigation_kb[feature_name_processed]
					else:
						# 2. Try matching original feature name if it was boolean/numerical
						original_name_candidate = (
							feature_name_processed.split('__')[0]
							if '__' in feature_name_processed
							else feature_name_processed
						)

						if original_name_candidate in mitigation_kb:
							strategy = mitigation_kb[original_name_candidate]
						# Specific strategy for boolean features if their "False" value is risky
						elif (
							input_df_ordered[original_name_candidate].iloc[0] == 0
							and f'{original_name_candidate}__False' in mitigation_kb
						):
							strategy = mitigation_kb[
								f'{original_name_candidate}__False'
							]
						elif (
							input_df_ordered[original_name_candidate].iloc[0] == 1
							and f'{original_name_candidate}__True' in mitigation_kb
						):  # Less common to have strategy for True being risky
							strategy = mitigation_kb[f'{original_name_candidate}__True']

					if strategy:
						st.markdown(f'**Factor:** `{display_feature_name}`')
						st.markdown(
							f"   *Farmer's Current Status for '{original_name_candidate}':* `{row_shap['feature_value_original']}`"
						)
						st.info(f'   **Suggestion:** {strategy}')
						suggested_count += 1

				if suggested_count == 0:
					st.write(
						'No specific actionable mitigation strategies found for the top risk factors from the knowledge base. General financial literacy and improved farm management are always beneficial.'
					)
			else:
				st.write(
					'SHAP analysis did not identify strong specific drivers for the high-risk prediction, or they are not in the mitigation knowledge base.'
				)
		elif risk_status == 'Lower Risk':
			st.success(
				'Farmer is predicted as Lower Risk. Maintain good practices and explore opportunities for growth.'
			)
			if explainer:  
				st.subheader('Key Factors Contributing to Lower Risk (SHAP Analysis)')
				current_shap_values = explainer.shap_values(input_processed_df)
				if isinstance(current_shap_values, list):
					current_shap_values = current_shap_values[1]  # For positive class (high risk)

				shap_df = pd.DataFrame(
					{
						'feature': processed_feature_names,
						'shap_value': current_shap_values.flatten(),
					}
				)
				# Features that pushed the score away from high risk (negative SHAP values)
				positive_factors = shap_df[shap_df['shap_value'] < -0.01].sort_values(
					by='shap_value', ascending=True
				)
				if not positive_factors.empty:
					for _, row_shap in positive_factors.head(3).iterrows():
						original_name_candidate = (
							row_shap['feature'].split('__')[0]
							if '__' in row_shap['feature']
							else row_shap['feature']
						)
						original_value = (
							input_df_ordered[original_name_candidate].iloc[0]
							if original_name_candidate in input_df_ordered
							else 'N/A'
						)
						st.markdown(
							f'- **Positive Factor:** `{row_shap["feature"]}` (Your status: `{original_value}`) strongly contributed to a lower risk assessment.'
						)
				else:
					st.write(
						'The model indicates a generally positive profile contributing to lower risk.'
					)

	except Exception as e:
		st.error(f'An error occurred during prediction or SHAP analysis: {e}')
		st.error(
			'Please ensure all inputs are correctly formatted and the model artifacts are valid.'
		)


else:
	st.info("Please fill in the farmer's data in the sidebar and click 'Assess Farmer Risk'.")

st.sidebar.markdown('---')
st.sidebar.markdown('Developed as part of the Agri-Finance Risk Assessment Project.')
