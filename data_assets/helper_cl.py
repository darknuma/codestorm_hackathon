"""Credit Lending data generation module.

This module generates synthetic data for credit lending analysis,
including farmer profiles, loan details, and credit scores.
"""

import pandas as pd
import numpy as np
import random
from faker import Faker
import os

os.makedirs('data', exist_ok=True)

np.random.seed(42)
random.seed(42)

try:
	fake = Faker('en_NG')  #
except:
	fake = Faker()

# Number of farmers to generate
num_farmers = 4000

# Define Nigerian states and regions
nigerian_states = [
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
	'FCT',
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
]

nigerian_regions = {
	'North Central': ['Benue', 'FCT', 'Kogi', 'Kwara', 'Nasarawa', 'Niger', 'Plateau'],
	'North East': ['Adamawa', 'Bauchi', 'Borno', 'Gombe', 'Taraba', 'Yobe'],
	'North West': ['Jigawa', 'Kaduna', 'Kano', 'Katsina', 'Kebbi', 'Sokoto', 'Zamfara'],
	'South East': ['Abia', 'Anambra', 'Ebonyi', 'Enugu', 'Imo'],
	'South South': ['Akwa Ibom', 'Bayelsa', 'Cross River', 'Delta', 'Edo', 'Rivers'],
	'South West': ['Ekiti', 'Lagos', 'Ogun', 'Ondo', 'Osun', 'Oyo'],
}

# Map states to regions
state_to_region = {}
for region, states in nigerian_regions.items():
	for state in states:
		state_to_region[state] = region

# Define common crops by region
crops_by_region = {
	'North Central': ['Maize', 'Rice', 'Yam', 'Cassava', 'Sorghum', 'Millet', 'Cowpea'],
	'North East': ['Millet', 'Sorghum', 'Groundnut', 'Cowpea', 'Maize', 'Rice'],
	'North West': ['Millet', 'Sorghum', 'Maize', 'Rice', 'Groundnut', 'Cotton'],
	'South East': ['Cassava', 'Yam', 'Rice', 'Maize', 'Vegetables', 'Oil Palm'],
	'South South': ['Cassava', 'Yam', 'Plantain', 'Oil Palm', 'Cocoa', 'Rubber'],
	'South West': ['Cocoa', 'Cassava', 'Maize', 'Yam', 'Oil Palm', 'Vegetables'],
}

# Define farm sizes based on regions (in hectares)
farm_size_ranges = {
	'North Central': (0.5, 5),
	'North East': (0.8, 7),
	'North West': (0.8, 8),
	'South East': (0.3, 3),
	'South South': (0.5, 4),
	'South West': (0.5, 5),
}

# Generate farmer data
data = {
	'farmer_id': [f'NGF{i:06d}' for i in range(1, num_farmers + 1)],
	'gender': np.random.choice(['Male', 'Female'], size=num_farmers, p=[0.65, 0.35]),
	'age': np.random.randint(18, 46, size=num_farmers),  # Young farmers 18-45
	'state': np.random.choice(nigerian_states, size=num_farmers),
	'education_level': np.random.choice(
		['No Formal Education', 'Primary', 'Secondary', 'Tertiary'],
		size=num_farmers,
		p=[0.15, 0.30, 0.40, 0.15],
	),
	'years_farming_experience': np.random.randint(1, 16, size=num_farmers),
	'owns_smartphone': np.random.choice([True, False], size=num_farmers, p=[0.65, 0.35]),
	'has_bank_account': np.random.choice([True, False], size=num_farmers, p=[0.55, 0.45]),
	'has_formal_id': np.random.choice([True, False], size=num_farmers, p=[0.60, 0.40]),
	'belongs_to_cooperative': np.random.choice([True, False], size=num_farmers, p=[0.40, 0.60]),
	'distance_to_market_km': np.random.uniform(1, 50, size=num_farmers),
	'distance_to_bank_km': np.random.uniform(1, 70, size=num_farmers),
	'has_off_farm_income': np.random.choice([True, False], size=num_farmers, p=[0.45, 0.55]),
	'has_prior_loan': np.random.choice([True, False], size=num_farmers, p=[0.25, 0.75]),
	'utility_bill_payment_score': np.random.randint(1, 11, size=num_farmers),  # 1-10 scale
	'mobile_money_activity_score': np.random.randint(1, 11, size=num_farmers),  # 1-10 scale
	'land_ownership_status': np.random.choice(
		['Owned', 'Family Owned', 'Leased', 'Community Land'],
		size=num_farmers,
		p=[0.30, 0.35, 0.25, 0.10],
	),
	'irrigation_access': np.random.choice([True, False], size=num_farmers, p=[0.20, 0.80]),
	'has_weather_insurance': np.random.choice([True, False], size=num_farmers, p=[0.10, 0.90]),
	'has_storage_facility': np.random.choice([True, False], size=num_farmers, p=[0.30, 0.70]),
	'uses_improved_seeds': np.random.choice([True, False], size=num_farmers, p=[0.45, 0.55]),
	'uses_fertilizer': np.random.choice([True, False], size=num_farmers, p=[0.60, 0.40]),
	'digital_footprint_score': np.random.randint(1, 11, size=num_farmers),  # 1-10 scale
	'loan_repayment_history': np.random.choice(
		['None', 'Poor', 'Fair', 'Good', 'Excellent'],
		size=num_farmers,
		p=[0.75, 0.05, 0.05, 0.10, 0.05],  # Majority have no history
	),
}

# Create the DataFrame
df = pd.DataFrame(data)

# Add region based on state
df['region'] = df['state'].map(state_to_region)

# Add primary crop based on region
df['primary_crop'] = df.apply(lambda x: random.choice(crops_by_region[x['region']]), axis=1)

# Add farm size based on region
df['farm_size_hectares'] = df.apply(
	lambda x: round(random.uniform(*farm_size_ranges[x['region']]), 2), axis=1
)

# Add yield data - varies by crop and region with some randomness
base_yields = {
	'Maize': 2.0,
	'Rice': 2.2,
	'Yam': 8.0,
	'Cassava': 12.0,
	'Sorghum': 1.8,
	'Millet': 1.5,
	'Cowpea': 0.8,
	'Groundnut': 1.0,
	'Cotton': 1.2,
	'Vegetables': 15.0,
	'Oil Palm': 4.0,
	'Plantain': 10.0,
	'Cocoa': 0.5,
	'Rubber': 1.2,
}


def calculate_yield(row):
	base = base_yields[row['primary_crop']]
	# Education and modern practices boost yields
	education_factor = {
		'No Formal Education': 0.8,
		'Primary': 0.9,
		'Secondary': 1.0,
		'Tertiary': 1.2,
	}

	modern_practices_factor = 1.0
	if row['uses_improved_seeds']:
		modern_practices_factor += 0.15
	if row['uses_fertilizer']:
		modern_practices_factor += 0.2
	if row['irrigation_access']:
		modern_practices_factor += 0.25

	# Experience factor
	experience_factor = min(1.0 + (row['years_farming_experience'] * 0.02), 1.3)

	# Random variation factor
	random_factor = random.uniform(0.8, 1.2)

	return round(
		base
		* education_factor[row['education_level']]
		* modern_practices_factor
		* experience_factor
		* random_factor,
		2,
	)


df['yield_tons_per_hectare'] = df.apply(calculate_yield, axis=1)

# Calculate total production
df['total_production_tons'] = df['farm_size_hectares'] * df['yield_tons_per_hectare']

# Average crop prices (in Naira per ton) - simplified estimates
crop_prices = {
	'Maize': 180000,
	'Rice': 300000,
	'Yam': 250000,
	'Cassava': 100000,
	'Sorghum': 170000,
	'Millet': 160000,
	'Cowpea': 350000,
	'Groundnut': 400000,
	'Cotton': 500000,
	'Vegetables': 300000,
	'Oil Palm': 450000,
	'Plantain': 200000,
	'Cocoa': 1200000,
	'Rubber': 600000,
}

# Calculate revenue
df['crop_price_per_ton'] = df['primary_crop'].map(crop_prices)
df['annual_farm_revenue'] = df['total_production_tons'] * df['crop_price_per_ton']


# Generate off-farm income data
def generate_off_farm_income(row):
	if row['has_off_farm_income']:
		# Base value varies by education
		education_base = {
			'No Formal Education': 100000,
			'Primary': 150000,
			'Secondary': 300000,
			'Tertiary': 600000,
		}
		base = education_base[row['education_level']]
		# Add some randomness
		return round(base * random.uniform(0.7, 1.3), -3)  # Round to nearest thousand
	else:
		return 0


df['annual_off_farm_income'] = df.apply(generate_off_farm_income, axis=1)
df['total_annual_income'] = df['annual_farm_revenue'] + df['annual_off_farm_income']


# Calculate farm expenses (simplified)
def calculate_expenses(row):
	# Base cost per hectare varies by crop
	base_cost_per_hectare = {
		'Maize': 120000,
		'Rice': 200000,
		'Yam': 180000,
		'Cassava': 90000,
		'Sorghum': 110000,
		'Millet': 100000,
		'Cowpea': 130000,
		'Groundnut': 150000,
		'Cotton': 180000,
		'Vegetables': 250000,
		'Oil Palm': 200000,
		'Plantain': 150000,
		'Cocoa': 300000,
		'Rubber': 250000,
	}

	base = base_cost_per_hectare[row['primary_crop']] * row['farm_size_hectares']

	# Modern practices increase costs
	if row['uses_improved_seeds']:
		base *= 1.1
	if row['uses_fertilizer']:
		base *= 1.15
	if row['irrigation_access']:
		base *= 1.2

	# Random variation
	return round(base * random.uniform(0.9, 1.1), -3)  # Round to nearest thousand


df['annual_farm_expenses'] = df.apply(calculate_expenses, axis=1)
df['farm_profit'] = df['annual_farm_revenue'] - df['annual_farm_expenses']
df['total_profit'] = df['total_annual_income'] - df['annual_farm_expenses']


# Loan history for those with prior loans
def generate_loan_details(row):
	if row['has_prior_loan']:
		# Loan amount as a function of farm size and revenue
		loan_amount = min(
			row['annual_farm_revenue'] * random.uniform(0.2, 0.5),
			500000 + (row['farm_size_hectares'] * 100000),
		)
		loan_amount = round(loan_amount, -3)  # Round to nearest thousand

		# Repayment rate based on several factors
		base_repayment_probability = 0.7

		# Factors that improve repayment
		if row['education_level'] in ['Secondary', 'Tertiary']:
			base_repayment_probability += 0.1
		if row['belongs_to_cooperative']:
			base_repayment_probability += 0.05
		if row['has_off_farm_income']:
			base_repayment_probability += 0.05
		if row['farm_profit'] > loan_amount * 0.5:
			base_repayment_probability += 0.1

		# Cap at 0.95
		repayment_probability = min(base_repayment_probability, 0.95)

		# Determine actual repayment rate
		actual_repayment_rate = random.uniform(
			max(0.3, repayment_probability - 0.2), min(1.0, repayment_probability + 0.1)
		)

		return pd.Series(
			{
				'loan_amount': loan_amount,
				'loan_repayment_rate': round(actual_repayment_rate, 2),
				'loan_purpose': random.choice(
					[
						'Seeds/Fertilizer',
						'Equipment',
						'Labor',
						'Irrigation',
						'Storage',
						'Transport',
						'Processing',
						'Land Expansion',
					]
				),
			}
		)
	else:
		return pd.Series({'loan_amount': 0, 'loan_repayment_rate': 0, 'loan_purpose': 'None'})


loan_details = df.apply(generate_loan_details, axis=1)
df = pd.concat([df, loan_details], axis=1)


# Create a synthetic credit score
def calculate_credit_score(row):
	# Base score
	score = 400  # Base score on a 300-850 scale

	# Education impact
	education_points = {'No Formal Education': 0, 'Primary': 20, 'Secondary': 40, 'Tertiary': 60}
	score += education_points[row['education_level']]

	# Financial inclusion factors
	if row['has_bank_account']:
		score += 30
	if row['has_formal_id']:
		score += 20

	# Income and stability factors
	score += min(row['years_farming_experience'] * 5, 50)  # Max 50 points for experience
	if row['has_off_farm_income']:
		score += 40

	# Utility payments and digital activity
	score += (row['utility_bill_payment_score'] - 1) * 5  # 0-45 points
	score += (row['mobile_money_activity_score'] - 1) * 5  # 0-45 points

	# Land security
	land_points = {'Owned': 40, 'Family Owned': 30, 'Leased': 20, 'Community Land': 10}
	score += land_points[row['land_ownership_status']]

	# Prior loan history
	if row['has_prior_loan']:
		repayment_history_points = {'Poor': -50, 'Fair': 0, 'Good': 50, 'Excellent': 80}
		if row['loan_repayment_history'] in repayment_history_points:
			score += repayment_history_points[row['loan_repayment_history']]

		# Actual repayment rate impact
		score += int((row['loan_repayment_rate'] - 0.5) * 100)  # -50 to +50 points

	# Social capital
	if row['belongs_to_cooperative']:
		score += 30

	# Modern farming practices
	if row['uses_improved_seeds']:
		score += 15
	if row['uses_fertilizer']:
		score += 15
	if row['irrigation_access']:
		score += 20

	# Risk mitigation
	if row['has_weather_insurance']:
		score += 25
	if row['has_storage_facility']:
		score += 15

	# Digital literacy
	if row['owns_smartphone']:
		score += 20
	score += (row['digital_footprint_score'] - 1) * 3  # 0-27 points

	# Distance factors (inverse relationship)
	score -= min(int(row['distance_to_bank_km'] / 5), 30)  # Max -30 points
	score -= min(int(row['distance_to_market_km'] / 5), 30)  # Max -30 points

	# Profitability factors
	profit_margin = row['farm_profit'] / max(row['annual_farm_revenue'], 1)
	if profit_margin > 0.3:
		score += 40
	elif profit_margin > 0.2:
		score += 30
	elif profit_margin > 0.1:
		score += 20
	elif profit_margin > 0:
		score += 10
	else:
		score -= 20

	# Cap the score within 300-850 range
	return max(300, min(850, score))


df['credit_score'] = df.apply(calculate_credit_score, axis=1)


# Define creditworthiness categories
def determine_creditworthiness(score):
	if score >= 700:
		return 'Excellent'
	elif score >= 650:
		return 'Good'
	elif score >= 600:
		return 'Fair'
	elif score >= 550:
		return 'Needs Improvement'
	else:
		return 'Poor'


df['creditworthiness'] = df['credit_score'].apply(determine_creditworthiness)


# Calculate maximum advisable loan amount based on credit score and income
def calculate_max_loan(row):
	# Base multiplier based on credit score
	if row['credit_score'] >= 700:
		multiplier = 1.0
	elif row['credit_score'] >= 650:
		multiplier = 0.8
	elif row['credit_score'] >= 600:
		multiplier = 0.6
	elif row['credit_score'] >= 550:
		multiplier = 0.4
	else:
		multiplier = 0.2

	# Calculate as a percentage of annual income
	base_amount = row['total_annual_income'] * multiplier

	# Adjust for farm size and profitability
	if row['farm_profit'] > 0:
		profit_factor = min(1.0 + (row['farm_profit'] / row['total_annual_income']) * 0.5, 1.5)
	else:
		profit_factor = max(0.5, 1.0 + (row['farm_profit'] / max(row['total_annual_income'], 1)))

	# Final calculation with some randomness
	max_loan = base_amount * profit_factor * random.uniform(0.9, 1.1)

	return round(max_loan, -3)  # Round to nearest thousand


df['max_recommended_loan'] = df.apply(calculate_max_loan, axis=1)


# Determine suitable loan products
def determine_loan_products(row):
	products = []

	# Input finance
	if row['credit_score'] >= 550:
		products.append('Input Finance')

	# Equipment loans - higher threshold
	if row['credit_score'] >= 600 and row['farm_size_hectares'] >= 1.0:
		products.append('Equipment Loan')

	# Working capital
	if row['credit_score'] >= 600:
		products.append('Working Capital')

	# Land acquisition
	if row['credit_score'] >= 700 and row['years_farming_experience'] >= 5:
		products.append('Land Acquisition')

	# Processing equipment
	if row['credit_score'] >= 650 and row['total_annual_income'] >= 500000:
		products.append('Processing Equipment')

	# Insurance products
	if row['farm_size_hectares'] >= 1.0:
		products.append('Crop Insurance')

	# Digital finance
	if row['owns_smartphone'] and row['digital_footprint_score'] >= 5:
		products.append('Digital Finance Solutions')

	# If no products are suitable, recommend starter product
	if not products and row['credit_score'] >= 500:
		products.append('Microfinance Starter')

	return ', '.join(products) if products else 'Not Eligible'


df['suitable_loan_products'] = df.apply(determine_loan_products, axis=1)


# Calculate predicted default probability based on various factors
def calculate_default_probability(row):
	# Base default risk
	base_risk = 0.30  # Starting point - 30% base risk for agricultural lending

	# Credit score impact (higher score = lower risk)
	credit_factor = 1.0 - ((row['credit_score'] - 300) / 550)  # 300-850 range mapped to 1.0-0.0

	# Income stability impact
	if row['has_off_farm_income']:
		income_stability_factor = 0.7
	else:
		income_stability_factor = 1.0

	# Experience impact
	experience_factor = max(0.7, 1.0 - (row['years_farming_experience'] * 0.02))

	# Modern farming practices impact
	modern_practices_factor = 1.0
	if row['uses_improved_seeds']:
		modern_practices_factor -= 0.05
	if row['uses_fertilizer']:
		modern_practices_factor -= 0.05
	if row['irrigation_access']:
		modern_practices_factor -= 0.1
	if row['has_weather_insurance']:
		modern_practices_factor -= 0.1

	# Social capital impact
	social_factor = 0.9 if row['belongs_to_cooperative'] else 1.0

	# Previous repayment history impact
	history_factor = 1.0
	if row['has_prior_loan']:
		history_mapping = {'Excellent': 0.6, 'Good': 0.8, 'Fair': 1.0, 'Poor': 1.3, 'None': 1.0}
		history_factor = history_mapping.get(row['loan_repayment_history'], 1.0)

	# Calculate final default probability
	default_prob = (
		base_risk
		* credit_factor
		* income_stability_factor
		* experience_factor
		* modern_practices_factor
		* social_factor
		* history_factor
	)

	# Add some randomness within reasonable bounds
	default_prob = default_prob * random.uniform(0.85, 1.15)

	# Cap between 0.01 (1%) and 0.9 (90%)
	return round(max(0.01, min(0.9, default_prob)), 4)


df['default_probability'] = df.apply(calculate_default_probability, axis=1)


# Generate a farmer profile summary string
def create_profile_summary(row):
	gender_pronoun = 'He' if row['gender'] == 'Male' else 'She'

	summary = f'{row["gender"]} farmer, age {row["age"]}, from {row["state"]} state. '
	summary += (
		f'{gender_pronoun} has {row["years_farming_experience"]} years of farming experience '
	)
	summary += f'with {row["education_level"]} education. '

	summary += f'Primarily grows {row["primary_crop"]} on {row["farm_size_hectares"]} hectares. '

	if row['belongs_to_cooperative']:
		summary += f'{gender_pronoun} is a member of a farming cooperative. '

	if row['has_off_farm_income']:
		summary += f'{gender_pronoun} has additional income sources beyond farming. '

	summary += f'Annual farm revenue: ₦{row["annual_farm_revenue"]:,.0f}. '

	if row['has_prior_loan']:
		summary += f'Has prior loan experience with {row["loan_repayment_history"].lower()} repayment history. '
	else:
		summary += 'No prior formal loan history. '

	credit_cat = row['creditworthiness'].lower()
	summary += (
		f'Credit assessment: {credit_cat} creditworthiness with a score of {row["credit_score"]}.'
	)

	return summary


df['profile_summary'] = df.apply(create_profile_summary, axis=1)

# Save to CSV in the data directory
output_file = os.path.join('data', 'credit_lending_data.csv')
df.to_csv(output_file, index=False)
print(f"Generated dataset saved to '{output_file}'")


# Data summary
print('\nData Summary:')
print(f'Average credit score: {df["credit_score"].mean():.2f}')
print(f'Creditworthiness distribution: {df["creditworthiness"].value_counts().to_dict()}')
print(f'Average farm size: {df["farm_size_hectares"].mean():.2f} hectares')
print(f'Average annual farm revenue: ₦{df["annual_farm_revenue"].mean():,.2f}')
print(f'Average default probability: {df["default_probability"].mean():.2%}')
