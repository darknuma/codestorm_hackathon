# """Data Science data generation module.

# This module generates synthetic data for data science analysis,
# including farmer demographics, farm characteristics, and financial data.
# """

# import pandas as pd
# import random
# from faker import Faker
# import os

# os.makedirs('data', exist_ok=True)

# fake = Faker()

# # Nigerian states
# nigerian_states = [
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
# ]

# # Common crops in Nigeria
# crops = [
# 	'Cassava',
# 	'Maize',
# 	'Rice',
# 	'Yam',
# 	'Sorghum',
# 	'Millet',
# 	'Cowpea',
# 	'Groundnut',
# 	'Soybean',
# 	'Sesame',
# 	'Cocoa',
# 	'Oil Palm',
# 	'Rubber',
# 	'Cotton',
# 	'Tomato',
# 	'Vegetables',
# ]

# # Livestock types
# livestock = ['Poultry', 'Cattle', 'Goats', 'Sheep', 'Pigs', 'Fish Farming', 'None']

# # Loan products
# loan_products = ['Farm Inputs', 'Mechanization Services', 'Bundled Services', 'None']


# # Generate synthetic farmer data
# def generate_farmers(num_farmers=4000):
# 	data = []

# 	for _ in range(num_farmers):
# 		# Basic demographics
# 		state = random.choice(nigerian_states)
# 		age = random.randint(18, 65)
# 		gender = random.choice(['Male', 'Female'])
# 		education = random.choice(['None', 'Primary', 'Secondary', 'Tertiary'])
# 		household_size = random.randint(1, 12)

# 		# Farm characteristics
# 		farm_size = round(random.uniform(0.1, 10), 2)  # in hectares
# 		primary_crop = random.choice(crops)
# 		secondary_crop = random.choice([c for c in crops if c != primary_crop] + ['None'])
# 		livestock_type = random.choice(livestock)
# 		farming_experience = random.randint(0, age - 18)  # Years

# 		# Financial data
# 		has_bank_account = random.choice([True, False])
# 		mobile_money_user = random.choice([True, False])
# 		monthly_income = random.randint(5000, 200000)  # Naira
# 		off_farm_income = random.randint(0, monthly_income // 2)

# 		# Alternative data points
# 		utility_payment_score = random.randint(300, 850)  # Simulated credit score
# 		mobile_airtime_spend = random.randint(
# 			500, 10000
# 		)  # Monthly side note doesn't having smartphone affect mobile airtime what about those that doesn't have smartphone
# 		has_smartphone = random.choice([True, False])

# 		# Loan history
# 		has_previous_loan = random.choice([True, False])
# 		if has_previous_loan:
# 			loan_amount = random.randint(20000, 500000)
# 			loan_product = random.choice(loan_products[:-1])
# 			repaid_on_time = random.choices([True, False], weights=[0.7, 0.3])[0]
# 			default_history = not repaid_on_time
# 		else:
# 			loan_amount = 0
# 			loan_product = 'None'
# 			repaid_on_time = False
# 			default_history = False

# 		# Cooperative membership
# 		cooperative_member = random.choices([True, False], weights=[0.6, 0.4])[0]
# 		if cooperative_member:
# 			cooperative_repayment_rate = random.randint(70, 100)  # Percentage
# 		else:
# 			cooperative_repayment_rate = 0

# 		# Generate recent payment dates (alternative data)
# 		last_utility_payment = fake.date_between(start_date='-90d', end_date='today')
# 		last_rent_payment = (
# 			fake.date_between(start_date='-60d', end_date='today') if age > 22 else None
# 		)

# 		# Digital footprint
# 		social_media_usage = random.choice(['None', 'Low', 'Medium', 'High'])
# 		ecommerce_activity = random.choices([True, False], weights=[0.3, 0.7])[0]

# 		data.append(
# 			[
# 				state,
# 				age,
# 				gender,
# 				education,
# 				household_size,
# 				farm_size,
# 				primary_crop,
# 				secondary_crop,
# 				livestock_type,
# 				farming_experience,
# 				has_bank_account,
# 				mobile_money_user,
# 				monthly_income,
# 				off_farm_income,
# 				utility_payment_score,
# 				mobile_airtime_spend,
# 				has_smartphone,
# 				has_previous_loan,
# 				loan_amount,
# 				loan_product,
# 				repaid_on_time,
# 				default_history,
# 				cooperative_member,
# 				cooperative_repayment_rate,
# 				last_utility_payment,
# 				last_rent_payment,
# 				social_media_usage,
# 				ecommerce_activity,
# 			]
# 		)

# 	columns = [
# 		'state',
# 		'age',
# 		'gender',
# 		'education',
# 		'household_size',
# 		'farm_size_hectares',
# 		'primary_crop',
# 		'secondary_crop',
# 		'livestock_type',
# 		'farming_experience_years',
# 		'has_bank_account',
# 		'uses_mobile_money',
# 		'monthly_income_naira',
# 		'off_farm_income_naira',
# 		'utility_payment_score',
# 		'monthly_mobile_spend_naira',
# 		'has_smartphone',
# 		'has_previous_loan',
# 		'last_loan_amount_naira',
# 		'loan_product_type',
# 		'repaid_last_loan_on_time',
# 		'has_default_history',
# 		'cooperative_member',
# 		'cooperative_repayment_rate_percent',
# 		'last_utility_payment_date',
# 		'last_rent_payment_date',
# 		'social_media_usage',
# 		'ecommerce_activity',
# 	]

# 	return pd.DataFrame(data, columns=columns)


# # Generate 4000 farmers
# farmers_df = generate_farmers(4000)

# # Add calculated fields
# farmers_df['total_income'] = (
# 	farmers_df['monthly_income_naira'] + farmers_df['off_farm_income_naira']
# )
# farmers_df['income_per_capita'] = farmers_df['total_income'] / farmers_df['household_size']
# farmers_df['farm_size_category'] = pd.cut(
# 	farmers_df['farm_size_hectares'],
# 	bins=[0, 1, 5, 10, float('inf')],
# 	labels=['Subsistence (<1ha)', 'Small (1-5ha)', 'Medium (5-10ha)', 'Large (>10ha)'],
# )

# # Save to CSV in the data directory
# output_file = os.path.join('data', 'data_science_dataset.csv')
# farmers_df.to_csv(output_file, index=False)
# print(f"Generated dataset saved to '{output_file}'")
