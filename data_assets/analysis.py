import os
import random
import pandas as pd
import numpy as np
from faker import Faker
import datetime

# --- Configuration & Constants ---
NUM_FARMERS = 10000  # Number of unique farmers to generate. Adjust as needed.
# MAX_ENTERPRISES_PER_FARMER = 1 # Now generating 1 primary enterprise based on master data concept
# MAX_LOANS_PER_ENTERPRISE = 1   # Now generating 1 loan based on prior_loan concept
OUTPUT_DIR = 'simplified_farmer_data_output_v2'

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize Faker
fake = Faker()  # Using Nigerian locale for names

# Set seeds for reproducibility
np.random.seed(42)
random.seed(42)

# --- Data Definitions (Adapted from original script, PDF, and Master Data) ---
NIGERIAN_STATES = [
	'Abia',
	'Adamawa',
	'Akwa Ibom',
	'Anambra',
	'Bauchi',
	'Bayelsa',
	'Benue',
	'Borno',
	'Cross River',
	'Delta',
	'Ebonyi',
	'Edo',
	'Ekiti',
	'Enugu',
	'Gombe',
	'Imo',
	'Jigawa',
	'Kaduna',
	'Kano',
	'Katsina',
	'Kebbi',
	'Kogi',
	'Kwara',
	'Lagos',
	'Nasarawa',
	'Niger',
	'Ogun',
	'Ondo',
	'Osun',
	'Oyo',
	'Plateau',
	'Rivers',
	'Sokoto',
	'Taraba',
	'Yobe',
	'Zamfara',
	'FCT',
]
NIGERIAN_REGIONS = {
	'North Central': ['Benue', 'FCT', 'Kogi', 'Kwara', 'Nasarawa', 'Niger', 'Plateau'],
	'North East': ['Adamawa', 'Bauchi', 'Borno', 'Gombe', 'Taraba', 'Yobe'],
	'North West': ['Jigawa', 'Kaduna', 'Kano', 'Katsina', 'Kebbi', 'Sokoto', 'Zamfara'],
	'South East': ['Abia', 'Anambra', 'Ebonyi', 'Enugu', 'Imo'],
	'South South': ['Akwa Ibom', 'Bayelsa', 'Cross River', 'Delta', 'Edo', 'Rivers'],
	'South West': ['Ekiti', 'Lagos', 'Ogun', 'Ondo', 'Osun', 'Oyo'],
}
STATE_TO_REGION = {state: region for region, states in NIGERIAN_REGIONS.items() for state in states}

MARITAL_STATUSES = ['Single', 'Married', 'Divorced', 'Widowed']
YES_NO = ['Yes', 'No']  # For boolean style fields
BOOLEAN_CHOICES = [True, False]  # For actual boolean fields

GENDERS = ['Male', 'Female']
ENTERPRISE_TYPES = ['Crop']  # Focusing on Crop type based on master data structure
PRIMARY_CROPS_LIST = [
	'Maize',
	'Cassava',
	'Sorghum',
	'Yam',
	'Cowpea',
	'Rice',
	'Millet',
	'Groundnut',
	'Vegetables',
	'Oil Palm',
	'Cocoa',
	'Plantain',
	'Soybean',
	'Sesame',
	'Tomato',
]
SECONDARY_CROPS_LIST = PRIMARY_CROPS_LIST + ['None']

FARM_SIZE_CATEGORIES_MASTER = [
	'Subsistence (<1ha)',
	'Small (1-5ha)',
	'Medium (5-10ha)',
	'Large (>10ha)',
]  # From master
FARMING_EQUIPMENT_TYPES = ['Traditional', 'Modern', 'Integrated']  # PDF schema

# Master Data Inspired Lists
LAND_ACQUISITION_METHODS_MASTER = [
	'Inheritance',
	'Family Owned',
	'Purchased',
	'Leased',
	'Community Land',
	'Rented',
	'Gift',
]
PEST_DISEASE_CONTROL_METHODS_MASTER = [
	'Modern Chemical',
	'Organic',
	'Traditional',
	'Integrated Pest Management',
	'None',
]
YIELD_CONSISTENCY_RATINGS_MASTER = ['High', 'Medium', 'Low', 'Very Low']
PRIOR_LOAN_REPAYMENT_HISTORY_MASTER = ['None', 'Poor', 'Fair', 'Good', 'Excellent']
PRIOR_LOAN_PURPOSES_MASTER = [
	'Input Loan',
	'Mechanization Loan',
	'Bundled Services Loan',
	'Working Capital',
	'Asset Acquisition',
	'Land Expansion',
	'Processing Equipment',
	'Storage Construction',
]


LOAN_SOURCES = [
	'Commercial Bank',
	'Microfinance Bank',
	'Cooperative',
	'Bank of Agriculture',
	'Informal Lender',
	'Family/Friends',
	'Government Program',
]  # PDF
DEFAULT_REASONS = [
	'Market Loss',
	'Low/Poor Yield',
	'Illness of Farmer',
	'Pest Attack',
	'Drought/Flood',
	'Diversion of Funds',
	'Input Price Hike',
	'Policy Change',
	'Other',
]  # PDF
CREDIT_WORTHINESS_STATUSES_PDF = ['Creditworthy', 'Non-creditworthy']  # PDF
LOAN_USE_STATUSES_PDF = ['Yes', 'No']  # Used as intended? PDF


# --- Helper Function ---
def weighted_choice(choices_weights):
	choices, weights = zip(*choices_weights)
	total_weight = sum(weights)
	if not np.isclose(total_weight, 1.0) and total_weight > 0:
		weights = [w / total_weight for w in weights]
	elif total_weight == 0:
		return random.choice(choices) if choices else None
	return random.choices(choices, weights=weights, k=1)[0]


def get_realistic_education_years(age):
	if age < 6:
		return 0
	max_possible_schooling_years = age - 6
	if age < 18:
		possible_education_weights = [(0, 0.3), (3, 0.2), (6, 0.2), (9, 0.2), (12, 0.1)]
	elif age < 25:
		possible_education_weights = [
			(0, 0.1),
			(6, 0.15),
			(9, 0.15),
			(12, 0.3),
			(14, 0.2),
			(16, 0.1),
		]
	else:
		possible_education_weights = [
			(0, 0.20),
			(3, 0.10),
			(6, 0.20),
			(9, 0.10),
			(12, 0.20),
			(14, 0.10),
			(16, 0.07),
			(18, 0.03),
		]
	valid_choices = [
		(years, weight)
		for years, weight in possible_education_weights
		if years <= max_possible_schooling_years
	]
	return weighted_choice(valid_choices) if valid_choices else 0


def get_farm_size_category_from_ha(farm_size_ha):
	"""Determines farm size category based on hectares from master data style."""
	if farm_size_ha < 1:
		return 'Subsistence (<1ha)'
	if farm_size_ha < 5:
		return 'Small (1-5ha)'
	if farm_size_ha < 10:
		return 'Medium (5-10ha)'
	return 'Large (>10ha)'


# --- Data Storage ---
farmer_profiles_data = []
farm_enterprises_data = []
loan_records_data = []

# --- Counters for IDs ---
enterprise_id_counter = 1
loan_id_counter = 1

print(f'Generating data for {NUM_FARMERS} farmers...')

# --- Main Generation Loop ---
for i in range(NUM_FARMERS):
	farmer_id = f'FARMER_{i + 1:05d}'

	# 1. Farmer_Profile Generation (largely same as before)
	age = random.randint(18, 70)
	gender = random.choice(GENDERS)
	name = fake.name_male() if gender == 'Male' else fake.name_female()
	education_level_years = get_realistic_education_years(age)

	if age < 20:
		marital_status = weighted_choice([('Single', 0.9), ('Married', 0.1)])
	elif age < 30:
		marital_status = weighted_choice(
			[('Single', 0.4), ('Married', 0.55), ('Divorced', 0.03), ('Widowed', 0.02)]
		)
	else:
		marital_status = weighted_choice(
			[('Single', 0.1), ('Married', 0.7), ('Divorced', 0.05), ('Widowed', 0.15)]
		)

	if marital_status == 'Single':
		household_size = random.randint(1, 3) if age < 25 else random.randint(1, 5)
	elif marital_status == 'Married':
		min_hh = 2
		if age < 25:
			household_size = random.randint(min_hh, min_hh + 2)
		elif age < 40:
			household_size = random.randint(min_hh, min_hh + 5)
		else:
			household_size = random.randint(min_hh, min_hh + 8)
	else:
		household_size = random.randint(1, 6)
	household_size = max(1, household_size)

	# Simulate master data fields for this farmer
	master_has_off_farm_income = random.choices(BOOLEAN_CHOICES, weights=[0.45, 0.55])[0]
	master_annual_off_farm_income_ngn = 0
	if master_has_off_farm_income:
		if education_level_years == 0:
			base_off_farm = 50000
		elif education_level_years <= 6:
			base_off_farm = 100000
		elif education_level_years <= 12:
			base_off_farm = 200000
		else:
			base_off_farm = 350000
		master_annual_off_farm_income_ngn = (
			round(random.uniform(0.5, 1.5) * base_off_farm / 1000) * 1000
		)

	state = random.choice(NIGERIAN_STATES)
	region = STATE_TO_REGION[state]

	# Fields for Farmer_Profile table
	has_bank_account_val = random.choices(YES_NO, weights=[0.6, 0.4])[0]
	owns_smartphone_val = random.choices(YES_NO, weights=[0.55, 0.45])[0]
	uses_mobile_money_val = 'No'
	if owns_smartphone_val == 'Yes':
		uses_mobile_money_val = random.choices(YES_NO, weights=[0.7, 0.3])[0]

	farmer_profiles_data.append(
		{
			'Farmer_ID': farmer_id,
			'Name': name,
			'Age': age,
			'Gender': gender,
			'Education_Level': education_level_years,
			'Marital_Status': marital_status,
			'Household_Size': household_size,
			'Offfarm_Income': master_annual_off_farm_income_ngn,  # From master concept
			'Region': region,
			'State': state,
			'Has_Bank_Account': has_bank_account_val,
			'Owns_Smartphone': owns_smartphone_val,
			'Uses_Mobile_Money': uses_mobile_money_val,
		}
	)

	# Simulate other master data fields for enterprise and loan
	master_farming_experience_years = random.randint(1, max(1, age - 15))
	master_farm_size_ha = round(random.uniform(0.2, 15.0), 2)
	master_farm_size_category = get_farm_size_category_from_ha(master_farm_size_ha)
	master_land_acquisition_method = random.choice(LAND_ACQUISITION_METHODS_MASTER)
	master_has_land_title = random.choices(BOOLEAN_CHOICES, weights=[0.2, 0.8])[0]
	master_primary_crop = random.choice(PRIMARY_CROPS_LIST)
	master_secondary_crop = random.choice(SECONDARY_CROPS_LIST) if random.random() > 0.4 else 'None'
	master_uses_improved_seeds = random.choices(BOOLEAN_CHOICES, weights=[0.3, 0.7])[0]
	master_uses_fertilizer = random.choices(BOOLEAN_CHOICES, weights=[0.4, 0.6])[0]
	master_uses_irrigation = random.choices(BOOLEAN_CHOICES, weights=[0.1, 0.9])[0]
	master_pest_disease_control_method = random.choice(PEST_DISEASE_CONTROL_METHODS_MASTER)
	master_soil_type_known = random.choices(BOOLEAN_CHOICES, weights=[0.5, 0.5])[0]
	master_uses_extension_services = random.choices(BOOLEAN_CHOICES, weights=[0.2, 0.8])[0]

	base_yield = random.uniform(0.5, 5.0)  # tons/ha
	if master_uses_fertilizer:
		base_yield *= random.uniform(1.1, 1.3)
	if master_uses_improved_seeds:
		base_yield *= random.uniform(1.1, 1.4)
	if master_uses_irrigation:
		base_yield *= random.uniform(1.1, 1.5)  # Irrigation has impact
	master_annual_farm_yield_tons_per_ha = round(base_yield, 2)

	master_total_production_tons = round(
		master_farm_size_ha * master_annual_farm_yield_tons_per_ha, 2
	)
	master_crop_price_per_ton_ngn = random.randint(150000, 400000)
	master_annual_farm_revenue_ngn = (
		round(master_total_production_tons * master_crop_price_per_ton_ngn / 1000) * 1000
	)
	master_annual_farm_expenses_ngn = (
		round(master_annual_farm_revenue_ngn * random.uniform(0.4, 0.8) / 1000) * 1000
	)
	master_farm_profit_ngn = master_annual_farm_revenue_ngn - master_annual_farm_expenses_ngn

	master_yield_consistency_rating = random.choice(YIELD_CONSISTENCY_RATINGS_MASTER)
	master_post_harvest_loss_perc = round(random.uniform(5, 40), 2)
	master_has_storage_facility = random.choices(BOOLEAN_CHOICES, weights=[0.35, 0.65])[0]
	master_has_weather_insurance = random.choices(BOOLEAN_CHOICES, weights=[0.05, 0.95])[
		0
	]  # Low rate
	master_owns_tractor = random.choices(BOOLEAN_CHOICES, weights=[0.05, 0.95])[
		0
	]  # Low ownership for specific machinery
	master_owns_plow = random.choices(BOOLEAN_CHOICES, weights=[0.1, 0.9])[0]
	master_owns_sprayer = random.choices(BOOLEAN_CHOICES, weights=[0.15, 0.85])[0]

	# 2. Farm_Enterprise Generation (1 primary crop enterprise per farmer)
	enterprise_id = f'ENT_{enterprise_id_counter:06d}'
	enterprise_id_counter += 1

	enterprise_type_val = 'Crop'  # Based on master data structure

	# Infer Farming_Equipment_type from ownership data (simplified)
	if master_owns_tractor or master_owns_plow:
		farming_equipment_type_val = random.choice(['Modern', 'Integrated'])
	else:
		farming_equipment_type_val = 'Traditional'

	depends_on_rain_val = 'Yes'
	if master_uses_irrigation:
		depends_on_rain_val = random.choices(['No', 'Partially'], weights=[0.7, 0.3])[0]

	monthly_income_val = round(master_annual_farm_revenue_ngn / 12 / 1000) * 1000
	monthly_expense_val = round(master_annual_farm_expenses_ngn / 12 / 1000) * 1000

	# Estimate Value_of_Farm_Assets (PDF field)
	value_of_farm_assets_val = (
		round(master_farm_size_ha * random.uniform(75000, 250000) / 1000) * 1000
	)  # Simplified
	if farming_equipment_type_val == 'Modern':
		value_of_farm_assets_val *= 1.5
	if master_has_storage_facility:
		value_of_farm_assets_val += random.randint(50000, 200000)

	farm_enterprises_data.append(
		{
			'Enterprise_ID': enterprise_id,
			'Farmer_ID': farmer_id,
			'Enterprise_Type': enterprise_type_val,
			'Primary_Crop': master_primary_crop,
			'Secondary_Crop': master_secondary_crop,
			'Farm_Size': master_farm_size_ha,  # Hectares for crop
			'Farm_Size_Category': master_farm_size_category,  # Mapped from master
			'Farming_Experience': master_farming_experience_years,  # General experience from master
			'Farming_Equipment_type': farming_equipment_type_val,  # PDF field, inferred
			'Uses_Irrigation': 'Yes' if master_uses_irrigation else 'No',
			'Depends_on_Rain': depends_on_rain_val,  # PDF field, inferred
			'Uses_Fertilizer': 'Yes' if master_uses_fertilizer else 'No',
			'Uses_Improved_Seeds': 'Yes' if master_uses_improved_seeds else 'No',
			'Yield_per_Hectare': master_annual_farm_yield_tons_per_ha,  # Tons
			'Profit': master_farm_profit_ngn,
			'Monthly_Income': monthly_income_val,  # PDF field, derived
			'Monthly_Expense': monthly_expense_val,  # PDF field, derived
			'Value_of_Farm_Assets': value_of_farm_assets_val,  # PDF field
			'Total_Operating_Expenditure': master_annual_farm_expenses_ngn,
			'Farm_Income': master_annual_farm_revenue_ngn,
			# New fields added from master data concept
			'Land_Acquisition_Method': master_land_acquisition_method,
			'Has_Land_Title': 'Yes' if master_has_land_title else 'No',
			'Pest_Disease_Control_Method': master_pest_disease_control_method,
			'Soil_Type_Known': 'Yes' if master_soil_type_known else 'No',
			'Uses_Extension_Services': 'Yes' if master_uses_extension_services else 'No',
			'Total_Production_Tons': master_total_production_tons,
			'Crop_Price_Per_Ton_NGN': master_crop_price_per_ton_ngn,
			'Yield_Consistency_Rating': master_yield_consistency_rating,
			'Post_Harvest_Loss_Perc': master_post_harvest_loss_perc,
			'Has_Storage_Facility': 'Yes' if master_has_storage_facility else 'No',
			'Has_Weather_Insurance': 'Yes' if master_has_weather_insurance else 'No',
			'Owns_Tractor': 'Yes' if master_owns_tractor else 'No',
			'Owns_Plow': 'Yes' if master_owns_plow else 'No',
			'Owns_Sprayer': 'Yes' if master_owns_sprayer else 'No',
		}
	)

	# 3. Loan_Record Generation (from master prior_loan concept)
	master_has_prior_loan = random.choices(BOOLEAN_CHOICES, weights=[0.25, 0.75])[
		0
	]  # 25% had a prior loan
	if master_has_prior_loan:
		loan_id = f'LOAN_{loan_id_counter:07d}'
		loan_id_counter += 1

		master_prior_loan_amount_ngn = (
			round(random.uniform(0.1, 0.5) * master_annual_farm_revenue_ngn / 5000) * 5000
		)
		master_prior_loan_amount_ngn = max(20000, master_prior_loan_amount_ngn)

		master_prior_loan_repayment_history = random.choice(PRIOR_LOAN_REPAYMENT_HISTORY_MASTER)
		master_prior_loan_repayment_rate = 0.0
		if master_prior_loan_repayment_history == 'Excellent':
			master_prior_loan_repayment_rate = random.uniform(0.95, 1.0)
		elif master_prior_loan_repayment_history == 'Good':
			master_prior_loan_repayment_rate = random.uniform(0.8, 0.94)
		elif master_prior_loan_repayment_history == 'Fair':
			master_prior_loan_repayment_rate = random.uniform(0.5, 0.79)
		elif master_prior_loan_repayment_history == 'Poor':
			master_prior_loan_repayment_rate = random.uniform(0.1, 0.49)
		master_prior_loan_repayment_rate = round(master_prior_loan_repayment_rate, 2)

		master_prior_loan_purpose = random.choice(PRIOR_LOAN_PURPOSES_MASTER)

		# PDF schema fields for Loan_Record
		interest_rate_val = round(random.uniform(5.0, 35.0), 1)
		loan_duration_months_val = random.choice([6, 12, 18, 24, 36])

		# Simulate loan date for prior loan (must be in the past)
		max_loan_start_offset_years = min(
			10, master_farming_experience_years - 1 if master_farming_experience_years > 1 else 1
		)
		loan_taken_years_ago = random.randint(
			1, max_loan_start_offset_years if max_loan_start_offset_years > 0 else 1
		)
		loan_date_val = datetime.date.today() - datetime.timedelta(
			days=loan_taken_years_ago * 365 + random.randint(0, 364)
		)

		has_defaulted_val = 'No'
		if master_prior_loan_repayment_history in ['Poor']:  # Simplified default inference
			has_defaulted_val = 'Yes'

		loan_repayment_amount_val = round(
			master_prior_loan_amount_ngn * master_prior_loan_repayment_rate
		)  # Based on actual repayment rate

		repayment_date_val = None
		if master_prior_loan_repayment_rate > 0:  # If any repayment was made
			# Assume repayment happened over the loan duration or partially if defaulted
			repayment_date_val = loan_date_val + datetime.timedelta(
				days=random.randint(30, loan_duration_months_val * 30)
			)
			if repayment_date_val > datetime.date.today():
				repayment_date_val = datetime.date.today()  # Cap at today

		loan_use_status_val = random.choice(LOAN_USE_STATUSES_PDF)  # Used as intended?
		loan_use_duration_val = random.randint(1, loan_duration_months_val)

		# Credit worthiness for this loan (can differ from farmer's general)
		credit_worthiness_val = random.choice(CREDIT_WORTHINESS_STATUSES_PDF)
		if has_defaulted_val == 'Yes':
			credit_worthiness_val = 'Non-creditworthy'

		loan_asset_ratio_val = (
			round(master_prior_loan_amount_ngn / max(1, value_of_farm_assets_val), 2)
			if value_of_farm_assets_val > 0
			else 0
		)
		op_ex_income_ratio_val = (
			round(master_annual_farm_expenses_ngn / max(1, master_annual_farm_revenue_ngn), 2)
			if master_annual_farm_revenue_ngn > 0
			else 0
		)

		loan_source_val = random.choice(LOAN_SOURCES)
		loan_supervision_freq_val = random.randint(0, 5)
		distance_to_lender_val = round(random.uniform(1, 100), 1)
		disbursement_lag_val = random.randint(0, 6)  # Months

		default_reason_val = 'N/A'
		if has_defaulted_val == 'Yes':
			default_reason_val = random.choice(DEFAULT_REASONS)

		# Master data's general credit score for the farmer
		master_credit_score = random.randint(300, 850)  # General score from master data concept

		loan_records_data.append(
			{
				'Loan_ID': loan_id,
				'Farmer_ID': farmer_id,
				'Enterprise_ID': enterprise_id,  # Assumes loan tied to this primary enterprise
				'Loan_Amount': master_prior_loan_amount_ngn,  # From master's prior loan
				'Interest_Rate': interest_rate_val,  # PDF field, generated
				'Loan_Date': loan_date_val.strftime('%Y-%m-%d'),  # PDF field, generated
				'Loan_Use_Status': loan_use_status_val,  # PDF field
				'Loan_Repayment_Amount': loan_repayment_amount_val,  # Calculated from master's rate
				'Repayment_Date': repayment_date_val.strftime('%Y-%m-%d')
				if repayment_date_val
				else None,  # PDF field
				'Duration_Months': loan_duration_months_val,  # PDF field, generated for this loan
				'Loan_Use_Duration': loan_use_duration_val,  # PDF field
				'Credit_Worthiness_Status': credit_worthiness_val,  # PDF field (specific to this loan's outcome)
				'Loan_Asset_Ratio': loan_asset_ratio_val,  # PDF field
				'OpEx_Income_Ratio': op_ex_income_ratio_val,  # PDF field
				'Loan_Source': loan_source_val,  # PDF field
				'Loan_Supervision_Frequency': loan_supervision_freq_val,  # PDF field
				'Distance_to_Lender': distance_to_lender_val,  # PDF field
				'Disbursement_Lag': disbursement_lag_val,  # PDF field
				'Has_Defaulted': has_defaulted_val,  # Inferred from master
				'Default_Reason': default_reason_val,  # PDF field
				# New fields added from master data concept related to prior loan
				'Prior_Loan_Repayment_Rate_Master': master_prior_loan_repayment_rate,
				'Prior_Loan_Repayment_History_Master': master_prior_loan_repayment_history,
				'Prior_Loan_Purpose_Master': master_prior_loan_purpose,
				'Farmer_Credit_Score_General_Master': master_credit_score,
			}
		)

	if (i + 1) % (NUM_FARMERS // 10 or 1) == 0:
		print(f'Generated data for {i + 1}/{NUM_FARMERS} farmers...')

# --- Convert to Pandas DataFrames ---
df_farmer_profiles = pd.DataFrame(farmer_profiles_data)
df_farm_enterprises = pd.DataFrame(farm_enterprises_data)
df_loan_records = pd.DataFrame(loan_records_data)

# --- Save to CSV Files ---
farmer_profiles_path = os.path.join(OUTPUT_DIR, 'farmer_profiles.csv')
farm_enterprises_path = os.path.join(OUTPUT_DIR, 'farm_enterprises.csv')
loan_records_path = os.path.join(OUTPUT_DIR, 'loan_records.csv')

df_farmer_profiles.to_csv(farmer_profiles_path, index=False)
df_farm_enterprises.to_csv(farm_enterprises_path, index=False)
df_loan_records.to_csv(loan_records_path, index=False)

print(f'\nData generation complete.')
print(f'Output directory: {OUTPUT_DIR}')
print(f'Farmer Profiles saved to: {farmer_profiles_path} ({len(df_farmer_profiles)} records)')
print(f'Farm Enterprises saved to: {farm_enterprises_path} ({len(df_farm_enterprises)} records)')
print(f'Loan Records saved to: {loan_records_path} ({len(df_loan_records)} records)')

# --- Basic Validation/Summary (Optional) ---
print('\n--- Farmer Profiles Summary (First 5) ---')
print(df_farmer_profiles.head())
print('\n--- Farm Enterprises Summary (First 5) ---')
print(df_farm_enterprises.head())
print('\n--- Loan Records Summary (First 5) ---')
if not df_loan_records.empty:
	print(df_loan_records.head())
else:
	print('No loan records generated (or all farmers had no prior loans in simulation).')
