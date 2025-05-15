# """General Model data generation module.

# This module generates synthetic data for general modeling,
# including comprehensive farmer profiles and agricultural metrics.
# """

# import pandas as pd
# import numpy as np
# from faker import Faker
# import random
# import os

# os.makedirs('data', exist_ok=True)

# fake = Faker()

# # Configuration
# NUM_FARMERS = 4000

# NIGERIAN_STATES = [
# 	'Abia',
# 	'Adamawa',
# 	'Akwa Ibom',
# 	'Anambra',
# 	'Bauchi',
# 	'Bayelsa',
# 	'Benue',
# 	'Borno',
# 	'Cross River',
# 	'Delta',
# 	'Ebonyi',
# 	'Edo',
# 	'Ekiti',
# 	'Enugu',
# 	'Gombe',
# 	'Imo',
# 	'Jigawa',
# 	'Kaduna',
# 	'Kano',
# 	'Katsina',
# 	'Kebbi',
# 	'Kogi',
# 	'Kwara',
# 	'Lagos',
# 	'Nasarawa',
# 	'Niger',
# 	'Ogun',
# 	'Ondo',
# 	'Osun',
# 	'Oyo',
# 	'Plateau',
# 	'Rivers',
# 	'Sokoto',
# 	'Taraba',
# 	'Yobe',
# 	'Zamfara',
# 	'FCT',
# ]

# EDUCATION_LEVELS_YEARS = {
# 	'None': 0,
# 	'Primary Incomplete': 3,
# 	'Primary Complete': 6,
# 	'Secondary Incomplete': 9,
# 	'Secondary Complete': 12,
# 	'OND/NCE': 14,
# 	'HND/BSc': 16,
# 	'Masters/PhD': 18,
# }

# MARITAL_STATUSES = ['Single', 'Married', 'Divorced', 'Widowed']

# PRIMARY_ENTERPRISES = [
# 	'Cassava',
# 	'Yam',
# 	'Maize',
# 	'Rice',
# 	'Vegetables',
# 	'Poultry',
# 	'Aquaculture',
# 	'Goats/Sheep',
# 	'Cocoa',
# 	'Oil Palm',
# 	'Sorghum',
# 	'Millet',
# ]
# PEST_DISEASE_CONTROL_METHODS = [
# 	'Modern Chemical',
# 	'Organic',
# 	'Traditional',
# 	'Integrated Pest Management',
# 	'None',
# ]
# UTILITY_PAYMENT_TIMELINESS_CATS = ['Excellent', 'Good', 'Fair', 'Poor']
# MOBILE_MONEY_USAGE_CATS = ['Daily', 'Weekly', 'Monthly', 'Rarely', 'Never']
# YIELD_CONSISTENCY_CATS = ['High', 'Medium', 'Low']
# LOAN_PRODUCTS_ZOWASEL = ['Input Loan', 'Mechanization Loan', 'Bundled Services Loan']


# # Helper function to create weighted choices
# def weighted_choice(choices_weights):
# 	choices, weights = zip(*choices_weights)
# 	return random.choices(choices, weights=weights, k=1)[0]


# data = []

# for i in range(NUM_FARMERS):
# 	farmer_id = f'FARMER_{1001 + i}'
# 	age = random.randint(18, 65)
# 	gender = random.choice(['Male', 'Female'])

# 	education_choice = weighted_choice(
# 		[
# 			('None', 0.15),
# 			('Primary Incomplete', 0.10),
# 			('Primary Complete', 0.25),
# 			('Secondary Incomplete', 0.10),
# 			('Secondary Complete', 0.25),
# 			('OND/NCE', 0.08),
# 			('HND/BSc', 0.05),
# 			('Masters/PhD', 0.02),
# 		]
# 	)
# 	education_level_years = EDUCATION_LEVELS_YEARS[education_choice]

# 	marital_status = weighted_choice(
# 		[
# 			('Single', 0.20 if age < 30 else 0.10),
# 			('Married', 0.70),
# 			('Divorced', 0.05),
# 			('Widowed', 0.05),
# 		]
# 	)
# 	household_size = (
# 		random.randint(1, 12) if marital_status == 'Single' and age < 25 else random.randint(2, 15)
# 	)
# 	state = random.choice(NIGERIAN_STATES)
# 	# lga = fake.city() # Simplified, real LGAs would need a proper mapping

# 	has_off_farm_income = random.choices([True, False], weights=[0.4, 0.6])[0]
# 	off_farm_income_ngn = round(random.uniform(20000, 300000), 2) if has_off_farm_income else 0

# 	farming_experience_years = max(
# 		1, min(age - 16, random.randint(1, 40))
# 	)  # Ensure experience is less than age
# 	farm_size_ha = round(
# 		random.uniform(0.2, 10) if random.random() < 0.8 else random.uniform(10, 50), 2
# 	)  # Skewed to smaller farms
# 	primary_enterprise = random.choice(PRIMARY_ENTERPRISES)

# 	# Simplified income calculation (can be made more sophisticated)
# 	enterprise_base_income_per_ha = {
# 		'Cassava': 150000,
# 		'Yam': 180000,
# 		'Maize': 120000,
# 		'Rice': 160000,
# 		'Vegetables': 200000,
# 		'Poultry': 500000,
# 		'Aquaculture': 600000,  # Per unit, not ha for these
# 		'Goats/Sheep': 300000,
# 		'Cocoa': 250000,
# 		'Oil Palm': 220000,
# 		'Sorghum': 110000,
# 		'Millet': 100000,
# 	}
# 	base_income = enterprise_base_income_per_ha.get(primary_enterprise, 100000)
# 	if primary_enterprise in ['Poultry', 'Aquaculture', 'Goats/Sheep']:  # Non-HA based income
# 		annual_farm_income_ngn = round(
# 			base_income * (farm_size_ha if farm_size_ha < 5 else 5) * random.uniform(0.7, 1.3), 2
# 		)  # Cap multiplier for non-HA
# 	else:
# 		annual_farm_income_ngn = round(farm_size_ha * base_income * random.uniform(0.7, 1.3), 2)

# 	operating_expenditure_ngn = round(annual_farm_income_ngn * random.uniform(0.4, 0.8), 2)
# 	value_farm_assets_ngn = round(
# 		(annual_farm_income_ngn * random.uniform(1.0, 3.0)) + (farm_size_ha * 50000), 2
# 	)

# 	cooperative_member = random.choices([True, False], weights=[0.35, 0.65])[0]

# 	# Loan Data
# 	requests_loan = random.choices([True, False], weights=[0.7, 0.3])[0]
# 	loan_amount_requested_ngn = 0
# 	loan_purpose = 'N/A'
# 	interest_rate_annual_perc = 0
# 	loan_tenure_months = 0
# 	disbursement_lag_days = 0
# 	loan_supervision_visits = 0

# 	# Alternative Credit Data
# 	utility_payment_timeliness = random.choice(UTILITY_PAYMENT_TIMELINESS_CATS)
# 	rent_payment_timeliness = random.choice(
# 		UTILITY_PAYMENT_TIMELINESS_CATS + ['N/A']
# 	)  # N/A if owns home
# 	phone_bill_timeliness = random.choice(UTILITY_PAYMENT_TIMELINESS_CATS)

# 	# Zowasel-like platform data
# 	value_chain_platform_registered = random.choices([True, False], weights=[0.25, 0.75])[
# 		0
# 	]  # e.g. Zowasel
# 	years_on_platform = 0
# 	marketplace_sales_ngn_last_year = 0

# 	if value_chain_platform_registered:
# 		years_on_platform = random.randint(0, 5)
# 		if years_on_platform > 0:
# 			marketplace_sales_ngn_last_year = round(
# 				random.uniform(0, annual_farm_income_ngn * 0.8), 2
# 			)  # Sells portion via platform

# 	if requests_loan:
# 		loan_amount_requested_ngn = (
# 			round(random.uniform(50000, 2000000) / 10000, 0) * 10000
# 		)  # Round to nearest 10k
# 		if (
# 			value_chain_platform_registered and random.random() < 0.8
# 		):  # Higher chance of Zowasel loan types if registered
# 			loan_purpose = random.choice(LOAN_PRODUCTS_ZOWASEL)
# 		else:
# 			loan_purpose = random.choice(
# 				LOAN_PRODUCTS_ZOWASEL + ['Working Capital', 'Asset Acquisition', 'Land Expansion']
# 			)
# 		interest_rate_annual_perc = round(random.uniform(12, 35), 2)
# 		loan_tenure_months = random.choice([3, 6, 9, 12, 18, 24])
# 		disbursement_lag_days = random.randint(7, 90)
# 		loan_supervision_visits = random.randint(0, 5)

# 	soil_type_known = random.choices([True, False], weights=[0.6, 0.4])[0]
# 	uses_irrigation = random.choices([True, False], weights=[0.2, 0.8])[0]
# 	pest_disease_control_method = random.choice(PEST_DISEASE_CONTROL_METHODS)

# 	# Simplified yield rating
# 	base_yield_score = 5
# 	if uses_irrigation:
# 		base_yield_score += 1
# 	if pest_disease_control_method in ['Modern Chemical', 'Integrated Pest Management']:
# 		base_yield_score += 1
# 	if pest_disease_control_method == 'None':
# 		base_yield_score -= 1
# 	yield_rating_score = np.clip(base_yield_score + random.randint(-1, 1), 1, 10)  # Score 1-10

# 	yield_consistency_rating = random.choice(YIELD_CONSISTENCY_CATS)
# 	post_harvest_loss_perc = round(random.uniform(5, 40), 2)
# 	smartphone_owner = random.choices([True, False], weights=[0.65, 0.35])[0]

# 	mobile_money_usage_frequency = 'Never'
# 	if smartphone_owner:
# 		mobile_money_usage_frequency = weighted_choice(
# 			[('Daily', 0.1), ('Weekly', 0.3), ('Monthly', 0.3), ('Rarely', 0.2), ('Never', 0.1)]
# 		)

# 	active_on_agri_forums = (
# 		random.choices([True, False], weights=[0.15, 0.85])[0] if smartphone_owner else False
# 	)
# 	distance_to_market_km = round(random.uniform(1, 70), 1)
# 	distance_to_lender_km = round(random.uniform(5, 150), 1) if requests_loan else 0

# 	# Simulate Loan Repayment Status (Simplified)
# 	# This is a very basic simulation. Real models would be more complex. i think we shoud remove creditworthiness score
# 	creditworthiness_score = 0
# 	if education_level_years >= EDUCATION_LEVELS_YEARS['Secondary Complete']:
# 		creditworthiness_score += 1
# 	if has_off_farm_income:
# 		creditworthiness_score += 1
# 	if cooperative_member:
# 		creditworthiness_score += 1
# 	if annual_farm_income_ngn > 500000:
# 		creditworthiness_score += 1
# 	if operating_expenditure_ngn / (annual_farm_income_ngn + 1e-6) < 0.6:
# 		creditworthiness_score += 1  # Lower op_ex ratio is good
# 	if value_chain_platform_registered and marketplace_sales_ngn_last_year > 0:
# 		creditworthiness_score += 2
# 	if utility_payment_timeliness == 'Excellent':
# 		creditworthiness_score += 2
# 	elif utility_payment_timeliness == 'Good':
# 		creditworthiness_score += 1
# 	if phone_bill_timeliness == 'Excellent':
# 		creditworthiness_score += 1

# 	if interest_rate_annual_perc > 30 and requests_loan:
# 		creditworthiness_score -= 1
# 	if post_harvest_loss_perc > 30:
# 		creditworthiness_score -= 1
# 	if yield_consistency_rating == 'Low':
# 		creditworthiness_score -= 1

# 	loan_repayment_status = 'N/A'
# 	if requests_loan:
# 		if creditworthiness_score >= 5:
# 			loan_repayment_status = weighted_choice(
# 				[('Fully Repaid', 0.8), ('Partially Repaid', 0.15), ('Defaulted', 0.05)]
# 			)
# 		elif creditworthiness_score >= 2:
# 			loan_repayment_status = weighted_choice(
# 				[('Fully Repaid', 0.4), ('Partially Repaid', 0.4), ('Defaulted', 0.2)]
# 			)
# 		else:
# 			loan_repayment_status = weighted_choice(
# 				[('Fully Repaid', 0.1), ('Partially Repaid', 0.3), ('Defaulted', 0.6)]
# 			)

# 	data.append(
# 		{
# 			'farmer_id': farmer_id,
# 			'age': age,
# 			'gender': gender,
# 			'education_level_years': education_level_years,
# 			'education_category': education_choice,
# 			'marital_status': marital_status,
# 			'household_size': household_size,
# 			'state': state,
# 			# "lga": lga,
# 			'off_farm_income_ngn': off_farm_income_ngn,
# 			'farming_experience_years': farming_experience_years,
# 			'farm_size_ha': farm_size_ha,
# 			'primary_enterprise': primary_enterprise,
# 			'annual_farm_income_ngn': annual_farm_income_ngn,
# 			'operating_expenditure_ngn': operating_expenditure_ngn,
# 			'value_farm_assets_ngn': value_farm_assets_ngn,
# 			'cooperative_member': cooperative_member,
# 			'requests_loan': requests_loan,
# 			'loan_amount_requested_ngn': loan_amount_requested_ngn,
# 			'loan_purpose': loan_purpose,
# 			'interest_rate_annual_perc': interest_rate_annual_perc,
# 			'loan_tenure_months': loan_tenure_months,
# 			'disbursement_lag_days': disbursement_lag_days,
# 			'loan_supervision_visits': loan_supervision_visits,
# 			'utility_payment_timeliness': utility_payment_timeliness,
# 			'rent_payment_timeliness': rent_payment_timeliness,
# 			'phone_bill_timeliness': phone_bill_timeliness,
# 			'value_chain_platform_registered': value_chain_platform_registered,
# 			'years_on_platform': years_on_platform,
# 			'marketplace_sales_ngn_last_year': marketplace_sales_ngn_last_year,
# 			'soil_type_known': soil_type_known,
# 			'uses_irrigation': uses_irrigation,
# 			'pest_disease_control_method': pest_disease_control_method,
# 			'yield_rating_score_1_10': yield_rating_score,
# 			'yield_consistency_rating': yield_consistency_rating,
# 			'post_harvest_loss_perc': post_harvest_loss_perc,
# 			'smartphone_owner': smartphone_owner,
# 			'mobile_money_usage_frequency': mobile_money_usage_frequency,
# 			'active_on_agri_forums': active_on_agri_forums,
# 			'distance_to_market_km': distance_to_market_km,
# 			'distance_to_lender_km': distance_to_lender_km,
# 			'simulated_creditworthiness_score': creditworthiness_score if requests_loan else None,
# 			'loan_repayment_status': loan_repayment_status,
# 		}
# 	)

# # Convert data to DataFrame
# df = pd.DataFrame(data)

# # Save to CSV in the data directory
# output_file = os.path.join('data', 'general_model_data.csv')
# df.to_csv(output_file, index=False)
# print(f"Generated dataset saved to '{output_file}'")
