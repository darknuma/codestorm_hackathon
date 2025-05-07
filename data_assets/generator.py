"""
Consolidated Generator script to generate synthetic data for Nigerian farmers,
combining principles and features from helper_ds.py, helper_cl.py, and helper_gm.py.
This script aims to produce a comprehensive dataset for alternative credit scoring models
and general agricultural finance analysis.
Version 2: Incorporates statistical context from LSMS-ISA survey data.
"""

import os
import random
import pandas as pd
import numpy as np
from faker import Faker
# from uuid import (
# 	uuid4,
# )  # Retained if needed for other unique ID generation, though farmer_id is custom

# --- Configuration & Constants ---
NUM_FARMERS = 10000
OUTPUT_DIR = 'data'
OUTPUT_FILENAME = os.path.join(OUTPUT_DIR, 'master_nigerian_farmer_data.csv')

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize Faker
fake = Faker()  # Using default locale

# Set seeds for reproducibility
np.random.seed(42)
random.seed(42)

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

# Major crops nationally based on context (Maize, Cassava, Sorghum/Guinea Corn, Yam, Beans/Cowpea)
MAJOR_NATIONAL_CROPS = ['Maize', 'Cassava', 'Sorghum', 'Yam', 'Cowpea']

CROPS_BY_REGION = {
	'North Central': [
		'Maize',
		'Rice',
		'Yam',
		'Cassava',
		'Sorghum',
		'Millet',
		'Cowpea',
		'Soybean',
		'Sesame',
		'Beans',
	],
	'North East': ['Millet', 'Sorghum', 'Groundnut', 'Cowpea', 'Maize', 'Rice', 'Sesame', 'Beans'],
	'North West': [
		'Millet',
		'Sorghum',
		'Maize',
		'Rice',
		'Groundnut',
		'Cotton',
		'Cowpea',
		'Tomato',
		'Beans',
	],
	'South East': ['Cassava', 'Yam', 'Rice', 'Maize', 'Vegetables', 'Oil Palm', 'Cocoa', 'Beans'],
	'South South': [
		'Cassava',
		'Yam',
		'Plantain',
		'Oil Palm',
		'Cocoa',
		'Rubber',
		'Rice',
		'Vegetables',
		'Beans',
	],
	'South West': [
		'Cocoa',
		'Cassava',
		'Maize',
		'Yam',
		'Oil Palm',
		'Vegetables',
		'Cowpea',
		'Plantain',
		'Beans',
	],
}
# Add Guinea Corn alias if needed
for region, crops in CROPS_BY_REGION.items():
	if 'Sorghum' in crops:
		crops.append('Guinea Corn')
ALL_CROPS = sorted(
	list(set(crop for crops_list in CROPS_BY_REGION.values() for crop in crops_list))
)


# Adjusted farm size ranges to better reflect national average ~1.28 ha
FARM_SIZE_RANGES_HA = {  # (min, max) hectares - Aiming for lower average
	'North Central': (0.3, 4),
	'North East': (0.4, 5),
	'North West': (0.4, 6),
	'South East': (0.1, 2.5),  # Generally smaller farms
	'South South': (0.2, 3),
	'South West': (0.2, 3.5),
}

EDUCATION_LEVELS_MAPPING = {
	'No Formal Education': 0,
	'Primary Incomplete': 3,
	'Primary Complete': 6,
	'Secondary Incomplete': 9,
	'Secondary Complete': 12,
	'OND/NCE': 14,
	'HND/BSc': 16,
	'Masters/PhD': 18,
}
EDUCATION_CATEGORIES = list(EDUCATION_LEVELS_MAPPING.keys())

MARITAL_STATUSES = ['Single', 'Married', 'Divorced', 'Widowed']

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
# Regional livestock prevalence hints
LIVESTOCK_WEIGHTS_BY_REGION = {
	'North Central': {
		'Poultry': 0.71,
		'Goats': 0.69,
		'Sheep': 0.18,
		'Cattle': 0.41,
		'Pigs': 0.1,
		'Fish Farming': 0.02,
		'Ducks': 0.07,
		'Guinea Fowl': 0.01,
		'None': 0.3,
	},
	'North East': {
		'Poultry': 0.44,
		'Goats': 0.68,
		'Sheep': 0.39,
		'Cattle': 0.36,
		'Pigs': 0.01,
		'Fish Farming': 0.01,
		'Ducks': 0.05,
		'Guinea Fowl': 0.02,
		'None': 0.3,
	},
	'North West': {
		'Poultry': 0.42,
		'Goats': 0.72,
		'Sheep': 0.56,
		'Cattle': 0.48,
		'Pigs': 0.01,
		'Fish Farming': 0.01,
		'Ducks': 0.03,
		'Guinea Fowl': 0.05,
		'None': 0.2,
	},  # Highest livestock
	'South East': {
		'Poultry': 0.65,
		'Goats': 0.52,
		'Sheep': 0.07,
		'Cattle': 0.01,
		'Pigs': 0.15,
		'Fish Farming': 0.003,
		'Ducks': 0.01,
		'Guinea Fowl': 0.0,
		'None': 0.4,
	},
	'South South': {
		'Poultry': 0.53,
		'Goats': 0.55,
		'Sheep': 0.02,
		'Cattle': 0.0,
		'Pigs': 0.1,
		'Fish Farming': 0.073,
		'Ducks': 0.01,
		'Guinea Fowl': 0.01,
		'None': 0.4,
	},  # Highest fishing
	'South West': {
		'Poultry': 0.58,
		'Goats': 0.53,
		'Sheep': 0.07,
		'Cattle': 0.06,
		'Pigs': 0.05,
		'Fish Farming': 0.003,
		'Ducks': 0.0,
		'Guinea Fowl': 0.01,
		'None': 0.4,
	},
}
# National average weights (fallback) - Prioritizing Goats and Poultry
NATIONAL_LIVESTOCK_WEIGHTS = {
	'Poultry': 0.54,
	'Goats': 0.65,
	'Sheep': 0.31,
	'Cattle': 0.25,
	'Pigs': 0.05,
	'Fish Farming': 0.02,
	'Ducks': 0.03,
	'Guinea Fowl': 0.02,
	'None': 0.53,
}

PRIMARY_LIVESTOCK_USES = [
	'Sold Alive',
	'Savings/Insurance',
	'Food for the Family',
	'Crop Agriculture',
	'Sale of Livestock Products',
	'Social Status/Prestige',
	'Transport',
]
LIVESTOCK_USE_WEIGHTS = [
	0.621,
	0.207,
	0.164,
	0.098,
	0.091,
	0.010,
	0.014,
]  # Approx weights from Table 6.18

LAND_OWNERSHIP_STATUSES = [
	'Inherited',
	'Family Owned',
	'Purchased',
	'Leased',
	'Community Land',
	'Rented',
	'Gift',
]  # Added Inherited
LAND_ACQUISITION_METHODS = [
	'Inheritance',
	'Purchase',
	'Lease',
	'Gift',
	'Community Grant',
	'Family Allocation',
	'Rental',
]

PEST_DISEASE_CONTROL_METHODS = [
	'Modern Chemical',
	'Organic',
	'Traditional',
	'Integrated Pest Management',
	'None',
]
UTILITY_PAYMENT_TIMELINESS_CATS = ['Excellent', 'Good', 'Fair', 'Poor']
MOBILE_MONEY_USAGE_CATS = ['Daily', 'Weekly', 'Monthly', 'Rarely', 'Never']
SOCIAL_MEDIA_USAGE_CATS = ['None', 'Low', 'Medium', 'High']
YIELD_CONSISTENCY_CATS = ['High', 'Medium', 'Low', 'Very Low']

LOAN_PRODUCTS_PLATFORM = [
	'Input Loan',
	'Mechanization Loan',
	'Bundled Services Loan',
]  # e.g., Zowasel
LOAN_PURPOSES_GENERAL = [
	'Working Capital',
	'Asset Acquisition',
	'Land Expansion',
	'Processing Equipment',
	'Storage Construction',
]
PRIOR_LOAN_REPAYMENT_HISTORY_CATS = ['None', 'Poor', 'Fair', 'Good', 'Excellent']

# Base yields (tons/hectare) - Added missing major crops
BASE_YIELDS_TONS_PER_HA = {
	'Maize': 2.5,
	'Rice': 2.8,
	'Yam': 10.0,
	'Cassava': 15.0,
	'Sorghum': 2.0,
	'Millet': 1.8,
	'Cowpea': 1.0,
	'Beans': 1.0,
	'Groundnut': 1.2,
	'Cotton': 1.5,
	'Vegetables': 18.0,
	'Oil Palm': 5.0,
	'Plantain': 12.0,
	'Cocoa': 0.7,
	'Rubber': 1.5,
	'Soybean': 1.5,
	'Sesame': 0.8,
	'Tomato': 20.0,
	'Guinea Corn': 2.0,  # Alias for Sorghum
}
# Average crop prices (Naira/ton) - Added missing major crops
CROP_PRICES_NAIRA_PER_TON = {
	'Maize': 200000,
	'Rice': 350000,
	'Yam': 280000,
	'Cassava': 120000,
	'Sorghum': 190000,
	'Millet': 180000,
	'Cowpea': 400000,
	'Beans': 400000,
	'Groundnut': 450000,
	'Cotton': 550000,
	'Vegetables': 320000,
	'Oil Palm': 500000,
	'Plantain': 220000,
	'Cocoa': 1500000,
	'Rubber': 700000,
	'Soybean': 380000,
	'Sesame': 600000,
	'Tomato': 250000,
	'Guinea Corn': 190000,  # Alias for Sorghum
}
# Base cost per hectare (Naira) - simplified
BASE_COST_PER_HA = {
	crop: price * 0.50 for crop, price in CROP_PRICES_NAIRA_PER_TON.items()
}  # Adjusted cost ratio slightly


# --- Helper Functions ---
def weighted_choice(choices_weights):
	choices, weights = zip(*choices_weights)
	# Normalize weights if they don't sum to 1 (or close enough)
	total_weight = sum(weights)
	if not np.isclose(total_weight, 1.0):
		weights = [w / total_weight for w in weights]
	return random.choices(choices, weights=weights, k=1)[0]


# --- Data Generation Functions (Adapted & Updated) ---
def calculate_yield_tons_per_ha(row):
	base = BASE_YIELDS_TONS_PER_HA.get(row['primary_crop'], 1.0)
	education_factor = {
		'No Formal Education': 0.8,
		'Primary Incomplete': 0.85,
		'Primary Complete': 0.9,
		'Secondary Incomplete': 0.95,
		'Secondary Complete': 1.0,
		'OND/NCE': 1.1,
		'HND/BSc': 1.15,
		'Masters/PhD': 1.2,
	}.get(row['education_category'], 1.0)

	modern_practices_factor = 1.0
	if row['uses_improved_seeds']:
		modern_practices_factor += 0.15  # Impact of improved seeds
	if row['uses_fertilizer']:
		modern_practices_factor += 0.20  # Impact of fertilizer
	if row['uses_irrigation']:
		modern_practices_factor += 0.35  # Higher impact for rare irrigation
	if row['pest_disease_control_method'] in ['Modern Chemical', 'Integrated Pest Management']:
		modern_practices_factor += 0.10
	if row['uses_extension_services']:
		modern_practices_factor += 0.05  # Small boost from extension

	experience_factor = min(1.0 + (row['farming_experience_years'] * 0.015), 1.25)
	random_factor = random.uniform(0.70, 1.30)  # Wider range for weather/local conditions

	return round(
		base * education_factor * modern_practices_factor * experience_factor * random_factor, 2
	)


def calculate_annual_farm_expenses_ngn(row):
	base_cost = BASE_COST_PER_HA.get(row['primary_crop'], 100000) * row['farm_size_ha']
	# Costs increase with modern inputs
	if row['uses_improved_seeds']:
		base_cost *= 1.15
	if row['uses_fertilizer']:
		base_cost *= 1.20
	if row['uses_irrigation']:
		base_cost *= 1.30
	# Consider hired labor cost (more likely for larger farms or female HOH)
	labor_factor = 1.0
	if row['farm_size_ha'] > 2.0:
		labor_factor += 0.1
	if row['gender'] == 'Female' and row['farm_size_ha'] > 1.0:
		labor_factor += 0.05  # May hire more labor
	base_cost *= labor_factor

	return round(base_cost * random.uniform(0.80, 1.20), -3)  # Round to nearest thousand


def generate_off_farm_income_ngn(row):
	if row['has_off_farm_income']:
		education_base = {
			'No Formal Education': 80000,
			'Primary Incomplete': 100000,
			'Primary Complete': 150000,
			'Secondary Incomplete': 200000,
			'Secondary Complete': 300000,
			'OND/NCE': 400000,
			'HND/BSc': 500000,
			'Masters/PhD': 700000,
		}.get(row['education_category'], 100000)
		return round(education_base * random.uniform(0.6, 1.4), -3)
	return 0


def generate_prior_loan_details(row):
	if row['has_prior_loan']:
		# Loan amount more tied to income/profit potential
		potential_revenue = row['annual_farm_revenue_ngn']
		loan_amount = min(
			potential_revenue * random.uniform(0.10, 0.35),  # Lower % of revenue
			200000 + (row['farm_size_ha'] * 60000),
		)  # Lower base + per ha amount
		loan_amount = round(max(20000, loan_amount), -3)  # Min loan amount, rounded

		base_repayment_prob = 0.60  # Slightly lower base
		if row['education_category'] in ['Secondary Complete', 'OND/NCE', 'HND/BSc', 'Masters/PhD']:
			base_repayment_prob += 0.1
		if row['cooperative_member']:
			base_repayment_prob += 0.07  # Slightly higher impact
		if row['has_off_farm_income']:
			base_repayment_prob += 0.08  # Higher impact
		if row['farm_profit_ngn'] > loan_amount * 0.5:
			base_repayment_prob += 0.1  # Higher profit buffer needed

		repayment_prob = min(base_repayment_prob, 0.90)
		actual_repayment_rate = random.uniform(
			max(0.20, repayment_prob - 0.30), min(1.0, repayment_prob + 0.1)
		)  # Wider variance

		repayment_history = 'None'
		if actual_repayment_rate >= 0.95:
			repayment_history = 'Excellent'
		elif actual_repayment_rate >= 0.80:
			repayment_history = 'Good'
		elif actual_repayment_rate >= 0.55:
			repayment_history = 'Fair'  # Adjusted threshold
		else:
			repayment_history = 'Poor'

		return pd.Series(
			{
				'prior_loan_amount_ngn': loan_amount,
				'prior_loan_repayment_rate': round(actual_repayment_rate, 2),
				'prior_loan_repayment_history': repayment_history,
				'prior_loan_purpose': random.choice(LOAN_PURPOSES_GENERAL + LOAN_PRODUCTS_PLATFORM),
			}
		)
	return pd.Series(
		{
			'prior_loan_amount_ngn': 0,
			'prior_loan_repayment_rate': 0,
			'prior_loan_repayment_history': 'None',
			'prior_loan_purpose': 'N/A',
		}
	)


def calculate_credit_score(row):  # Scale 300-850
	score = 350
	# Education
	edu_points = {
		'No Formal Education': 0,
		'Primary Incomplete': 10,
		'Primary Complete': 20,
		'Secondary Incomplete': 30,
		'Secondary Complete': 50,
		'OND/NCE': 60,
		'HND/BSc': 70,
		'Masters/PhD': 80,
	}
	score += edu_points.get(row['education_category'], 0)
	# Financial Inclusion
	if row['has_bank_account']:
		score += 35
	if row['has_formal_id']:
		score += 25
	if row['mobile_money_usage_frequency'] not in ['Never', 'Rarely']:
		score += 20
	# Income & Stability
	score += min(row['farming_experience_years'] * 3, 30)  # Reduced points per year
	if row['has_off_farm_income']:
		score += 50  # Increased impact
	if row['yield_consistency_rating'] == 'High':
		score += 20
	elif row['yield_consistency_rating'] == 'Medium':
		score += 10
	elif row['yield_consistency_rating'] == 'Low':
		score -= 10  # Penalty for low consistency
	# Alternative Payments
	score += (row['utility_bill_payment_score_1_10'] - 1) * 4  # Max 36
	score += (row['mobile_money_activity_score_1_10'] - 1) * 3  # Max 27
	if row['phone_bill_timeliness'] == 'Excellent':
		score += 15
	elif row['phone_bill_timeliness'] == 'Good':
		score += 8
	# Land Security
	land_pts = {
		'Inherited': 25,
		'Family Owned': 30,
		'Purchased': 40,
		'Leased': 15,
		'Community Land': 10,
		'Rented': 5,
		'Gift': 20,
	}
	score += land_pts.get(row['land_acquisition_method'], 10)  # Use acquisition method
	if row['has_land_title']:
		score += 25  # Bonus for title
	# Prior Loan History
	if row['has_prior_loan']:
		history_pts = {
			'Excellent': 70,
			'Good': 40,
			'Fair': -10,
			'Poor': -70,
			'None': 0,
		}  # Increased penalty
		score += history_pts.get(row['prior_loan_repayment_history'], 0)
		score += int(
			(row['prior_loan_repayment_rate'] - 0.6) * 100
		)  # Adjusted baseline, scale -48 to +32
	# Social Capital
	if row['cooperative_member']:
		score += 40  # Increased impact
	if row['uses_extension_services']:
		score += 15  # Added extension service impact
	# Modern Farming Practices (Lower impact reflecting lower adoption)
	if row['uses_improved_seeds']:
		score += 10
	if row['uses_fertilizer']:
		score += 10
	if row['uses_irrigation']:
		score += 15  # Irrigation still valuable if present
	# Risk Mitigation
	if row['has_weather_insurance']:
		score += 35  # Higher impact for rare insurance
	if row['has_storage_facility']:
		score += 15
	# Digital Footprint
	if row['smartphone_owner']:
		score += 20
	score += (row['digital_footprint_score_1_10'] - 1) * 2  # Max 18
	if row['value_chain_platform_registered'] and row['years_on_platform'] > 0:
		score += 30  # Increased impact
	# Profitability
	profit_margin = row['farm_profit_ngn'] / max(row['annual_farm_revenue_ngn'], 1)
	if profit_margin > 0.30:
		score += 35  # Adjusted thresholds
	elif profit_margin > 0.15:
		score += 20
	elif profit_margin > 0.0:
		score += 5
	else:
		score -= 30  # Increased penalty

	# Asset Ownership (Basic tools common, machinery rare)
	if row['owns_tractor']:
		score += 25
	if row['owns_plow']:
		score += 15
	if row['owns_sprayer']:
		score += 10

	return max(300, min(850, int(score)))


def determine_creditworthiness_category(score):
	if score >= 700:
		return 'Excellent'
	elif score >= 660:
		return 'Very Good'
	elif score >= 620:
		return 'Good'
	elif score >= 560:
		return 'Fair'
	elif score >= 480:
		return 'Poor'
	else:
		return 'Very Poor'


def calculate_max_recommended_loan_ngn(row):
	multiplier = 0.05  # Base for very poor
	if row['credit_score'] >= 700:
		multiplier = 0.7
	elif row['credit_score'] >= 660:
		multiplier = 0.55
	elif row['credit_score'] >= 620:
		multiplier = 0.4
	elif row['credit_score'] >= 560:
		multiplier = 0.25
	elif row['credit_score'] >= 480:
		multiplier = 0.15

	base_amount = row['total_annual_income_ngn'] * multiplier
	# Profit factor adjusted
	profit_factor = (
		min(1.0 + (row['farm_profit_ngn'] / max(row['total_annual_income_ngn'], 1)) * 0.5, 1.5)
		if row['farm_profit_ngn'] > 0
		else 0.5
	)
	max_loan = base_amount * profit_factor * random.uniform(0.80, 1.20)
	return round(max(10000, max_loan), -3)  # Min recommended loan 10k


def determine_suitable_loan_products(row):
	products = []
	# Adjusted thresholds based on new credit score distribution
	if row['credit_score'] >= 480:
		products.append('Microfinance Starter')
	if row['credit_score'] >= 560:
		products.append('Input Finance')
	if row['credit_score'] >= 620 and row['farm_size_ha'] >= 0.5:
		products.append('Equipment Loan (Small)')
	if row['credit_score'] >= 620:
		products.append('Working Capital')
	if row['credit_score'] >= 660 and row['farming_experience_years'] >= 4:
		products.append('Land Expansion Loan')
	if row['credit_score'] >= 660 and row['total_annual_income_ngn'] >= 600000:
		products.append('Processing Equipment Loan')
	if row['farm_size_ha'] >= 0.8 and row['credit_score'] >= 560:
		products.append('Crop Insurance Partnership')
	if row['smartphone_owner'] and row['digital_footprint_score_1_10'] >= 3:
		products.append('Digital Finance Solutions')
	return ', '.join(sorted(list(set(products)))) if products else 'Not Currently Eligible'


def calculate_predicted_default_probability(row):  # For current loan request
	base_risk = 0.40  # Slightly higher base risk
	credit_factor = 1.0 - ((row['credit_score'] - 300) / 550)
	income_stability_factor = 0.75 if row['has_off_farm_income'] else 1.0  # Higher impact
	experience_factor = max(
		0.70, 1.0 - (row['farming_experience_years'] * 0.02)
	)  # More impact from experience

	modern_practices_factor = 1.0
	if row['uses_improved_seeds']:
		modern_practices_factor -= 0.05  # Slightly more impact
	if row['uses_fertilizer']:
		modern_practices_factor -= 0.05
	if row['uses_irrigation']:
		modern_practices_factor -= 0.10
	if row['has_weather_insurance']:
		modern_practices_factor -= 0.15

	social_factor = 0.80 if row['cooperative_member'] else 1.0  # Higher impact
	social_factor = (
		social_factor * 0.95 if row['uses_extension_services'] else social_factor
	)  # Extension impact

	prior_history_factor = 1.0
	if row['has_prior_loan']:
		history_map = {
			'Excellent': 0.65,
			'Good': 0.80,
			'Fair': 1.05,
			'Poor': 1.35,
			'None': 1.0,
		}  # Adjusted map
		prior_history_factor = history_map.get(row['prior_loan_repayment_history'], 1.0)

	# Consider requested loan vs capacity
	loan_to_income_ratio = row['loan_amount_requested_ngn'] / max(row['total_annual_income_ngn'], 1)
	capacity_factor = 1.0 + min(
		max(0, loan_to_income_ratio - 0.25) * 2.5, 0.6
	)  # Penalize earlier, higher penalty

	default_prob = (
		base_risk
		* credit_factor
		* income_stability_factor
		* experience_factor
		* modern_practices_factor
		* social_factor
		* prior_history_factor
		* capacity_factor
	)
	default_prob = default_prob * random.uniform(0.75, 1.25)  # Wider random range
	return round(max(0.02, min(0.98, default_prob)), 4)  # Adjusted bounds


# --- Main Data Generation Loop ---
all_farmer_data = []
for i in range(NUM_FARMERS):
	farmer_id = f'NGF{i + 1:06d}'
	age = random.randint(16, 65) #

	possible_education_levels = []
	if age < 18: # Too young for anything beyond some secondary
		possible_education_levels = [
			('No Formal Education', 0.4),
			('Primary Incomplete', 0.3),
			('Primary Complete', 0.2),
			('Secondary Incomplete', 0.1)
		]
	elif age < 22: # Potentially up to Secondary Complete, maybe some early tertiary
		possible_education_levels = [
			('No Formal Education', 0.20),
			('Primary Incomplete', 0.10),
			('Primary Complete', 0.20),
			('Secondary Incomplete', 0.20),
			('Secondary Complete', 0.25),
			('OND/NCE', 0.05) # Less likely but possible
		]
	elif age < 25: # Potentially up to OND/NCE or early BSc
		possible_education_levels = [
			('No Formal Education', 0.15),
			('Primary Incomplete', 0.10),
			('Primary Complete', 0.15),
			('Secondary Incomplete', 0.15),
			('Secondary Complete', 0.25),
			('OND/NCE', 0.15),
			('HND/BSc', 0.05) # Less likely but possible
		]
	else: # Can access all levels
		possible_education_levels = [
			('No Formal Education', 0.25),
			('Primary Incomplete', 0.15),
			('Primary Complete', 0.25),
			('Secondary Incomplete', 0.10),
			('Secondary Complete', 0.18),
			('OND/NCE', 0.04),
			('HND/BSc', 0.02),
			('Masters/PhD', 0.01),
		]

	# Ensure education years don't exceed (age - typical_starting_school_age)
	# e.g. typical_starting_school_age = 6
	max_possible_edu_years = age - 6
	filtered_education_choices = []
	for edu_cat, weight in possible_education_levels:
		if EDUCATION_LEVELS_MAPPING[edu_cat] <= max_possible_edu_years:
			filtered_education_choices.append((edu_cat, weight))
		# If highest education for age bracket is still too high, it will be excluded.
		# If all are excluded (e.g. for age 6, no formal edu is 0, <= 6-6=0),
		# you might need a fallback like 'No Formal Education'.

	if not filtered_education_choices: # Fallback if all get filtered out
		# This might happen if age is very low and all defined education levels exceed max_possible_edu_years
		# Or if weights are such that no valid option remains after filtering.
		# A robust fallback would be 'No Formal Education' or the lowest possible valid one.
		education_category = 'No Formal Education'
	else:
		education_category = weighted_choice(filtered_education_choices)

	education_level_years = EDUCATION_LEVELS_MAPPING[education_category]
	gender = random.choices(['Male', 'Female'], weights=[0.75, 0.25])[
		0
	]  # Reflecting HOH stats more

	# education_category = weighted_choice(
	# 	[
	# 		('No Formal Education', 0.25),
	# 		('Primary Incomplete', 0.15),
	# 		('Primary Complete', 0.25),  # Higher no/primary
	# 		('Secondary Incomplete', 0.10),
	# 		('Secondary Complete', 0.18),
	# 		('OND/NCE', 0.04),
	# 		('HND/BSc', 0.02),
	# 		('Masters/PhD', 0.01),  # Lower tertiary
	# 	]
	# )
	# education_level_years = EDUCATION_LEVELS_MAPPING[education_category]

# --- Inside the main loop ---
# age is already generated

	if age < 18: # Very young
		marital_status_weights = [
			('Single', 0.95),
			('Married', 0.05), # Very low chance
			('Divorced', 0.00),
			('Widowed', 0.00)
		]
	elif age < 22:
		marital_status_weights = [
			('Single', 0.60),
			('Married', 0.38),
			('Divorced', 0.01),
			('Widowed', 0.01)
		]
	elif age < 30:
		marital_status_weights = [
			('Single', 0.25),
			('Married', 0.70),
			('Divorced', 0.02),
			('Widowed', 0.03)
		]
	else: # 30+
		marital_status_weights = [
			('Single', 0.05),
			('Married', 0.75), #
			('Divorced', 0.05), # Slightly higher chance than current
			('Widowed', 0.15)  # Higher chance for older individuals
		]
	marital_status = weighted_choice(marital_status_weights)


	if marital_status == 'Single':
		if age < 22:
			household_size = random.randint(1, 3) # Likely living with parents or alone/few roommates
		elif age < 30:
			household_size = random.randint(1, 5) # (original logic for this bracket)
		else: # Older single individual
			household_size = random.randint(1, 4)
	elif marital_status == 'Married':
		# For younger married individuals, household size might start smaller
		min_hh_size = 2 # Self and spouse
		if age < 22:
			# Less likely to have many children immediately
			household_size = random.randint(min_hh_size, min_hh_size + 2) # e.g., 2-4
		elif age < 30:
			household_size = random.randint(min_hh_size, min_hh_size + 4) # e.g., 2-6
		else: # 30+
			household_size = random.randint(min_hh_size, 14) # Can be larger (similar to original upper range)
	elif marital_status == 'Widowed':
		# Could be 1 (if no children/dependents) or more
		# Consider age for likelihood of having dependent children
		if age < 30:
			household_size = random.randint(1, 3) # Less likely to have many older children
		else:
			household_size = random.randint(1, 10) # Can have dependents
	elif marital_status == 'Divorced':
		if age < 30:
			household_size = random.randint(1, 4)
		else:
			household_size = random.randint(1, 8)

	# Ensure household_size is at least 1
	household_size = max(1, household_size)
	# household_size = (
	# 	random.randint(1, 5) if marital_status == 'Single' and age < 30 else random.randint(3, 14)
	# )  # Typical range 4-6 mentioned

	state = random.choice(NIGERIAN_STATES)
	region = STATE_TO_REGION[state]

	has_off_farm_income = random.choices([True, False], weights=[0.45, 0.55])[
		0
	]  # Slightly lower off-farm

	farming_experience_years = max(1, min(age - 16, random.randint(1, 45)))  # Allow more experience

	# Generate farm size skewed towards national average of ~1.28ha
	farm_size_min, farm_size_max = FARM_SIZE_RANGES_HA[region]
	# Use a distribution that peaks lower, like beta or log-normal, simplified here with power
	farm_size_ha = round(
		farm_size_min + (farm_size_max - farm_size_min) * (random.random() ** 2.5), 2
	)  # Power concentrates smaller values
	farm_size_ha = round(max(0.05, farm_size_ha), 2)  # Min farm size

	# Select primary crop, giving weight to major national crops
	regional_crops = CROPS_BY_REGION.get(region, ALL_CROPS)
	crop_weights = [3 if crop in MAJOR_NATIONAL_CROPS else 1 for crop in regional_crops]
	primary_crop = random.choices(regional_crops, weights=crop_weights, k=1)[0]

	secondary_crop_options = [c for c in regional_crops if c != primary_crop] + ['None']
	secondary_crop = random.choice(secondary_crop_options) if secondary_crop_options else 'None'

	# Livestock Ownership
	owns_livestock = random.choices([True, False], weights=[0.47, 0.53])[0]
	livestock_type = 'None'
	primary_livestock_use = 'N/A'
	if owns_livestock:
		region_weights = LIVESTOCK_WEIGHTS_BY_REGION.get(region, NATIONAL_LIVESTOCK_WEIGHTS)
		livestock_type = weighted_choice(list(region_weights.items()))
		if livestock_type != 'None':
			primary_livestock_use = weighted_choice(
				list(zip(PRIMARY_LIVESTOCK_USES, LIVESTOCK_USE_WEIGHTS))
			)
		else:
			owns_livestock = False  # Correct if 'None' is chosen despite owning flag

	# Farm practices reflecting national averages
	uses_fertilizer = random.choices([True, False], weights=[0.354, 1 - 0.354])[0]
	uses_improved_seeds = random.choices([True, False], weights=[0.101, 1 - 0.101])[0]
	uses_irrigation = random.choices([True, False], weights=[0.022, 1 - 0.022])[0]
	# Adjust input use slightly based on gender context
	if gender == 'Female':
		uses_fertilizer = (
			uses_fertilizer if random.random() < 0.9 else False
		)  # Slightly less likely
		# uses_improved_seeds = uses_improved_seeds # Context says female use similar/more seeds
	else:  # Male
		uses_fertilizer = uses_fertilizer if random.random() < 1.1 else True  # Slightly more likely

	pest_disease_control_method = random.choice(PEST_DISEASE_CONTROL_METHODS)
	soil_type_known = random.choices([True, False], weights=[0.5, 0.5])[0]
	yield_consistency_rating = random.choice(YIELD_CONSISTENCY_CATS)
	post_harvest_loss_perc = round(random.uniform(5, 45), 2)  # Context: Table 6.12 shows some loss
	has_storage_facility = random.choices([True, False], weights=[0.35, 0.65])[0]
	has_weather_insurance = random.choices([True, False], weights=[0.05, 0.95])[
		0
	]  # Even lower insurance rate

	# Land Tenure
	land_acquisition_method = weighted_choice(
		[
			('Inheritance', 0.65),
			('Family Allocation', 0.15),
			('Purchase', 0.08),  # ~10% purchase overall
			('Lease', 0.05),
			('Rental', 0.03),
			('Community Grant', 0.02),
			('Gift', 0.02),
		]
	)
	# Lower title probability based on context
	has_land_title = False
	if land_acquisition_method == 'Purchase':
		has_land_title = random.choices([True, False], weights=[0.20, 0.80])[
			0
		]  # Higher chance if purchased
	else:
		has_land_title = random.choices([True, False], weights=[0.05, 0.95])[
			0
		]  # Low chance otherwise

	# Agricultural Assets Ownership (Based on Table 6.21)
	owns_tractor = random.choices([True, False], weights=[0.001, 0.999])[0]
	owns_plow = random.choices([True, False], weights=[0.051, 1 - 0.051])[0]
	owns_sprayer = random.choices([True, False], weights=[0.142, 1 - 0.142])[0]
	owns_wheelbarrow = random.choices([True, False], weights=[0.233, 1 - 0.233])[0]
	owns_cutlass = random.choices([True, False], weights=[0.904, 1 - 0.904])[0]  # Very common
	owns_sickle = random.choices([True, False], weights=[0.325, 1 - 0.325])[0]

	# Extension Services
	uses_extension_services = random.choices([True, False], weights=[0.207, 1 - 0.207])[0]

	# Financial Inclusion & Digital Footprint
	has_bank_account = random.choices([True, False], weights=[0.55, 0.45])[
		0
	]  # Slightly lower formal access
	has_formal_id = random.choices([True, False], weights=[0.65, 0.35])[0]
	smartphone_owner = random.choices([True, False], weights=[0.60, 0.40])[
		0
	]  # Lower smartphone penetration assumed
	mobile_money_usage_frequency = 'Never'
	if smartphone_owner:
		mobile_money_usage_frequency = weighted_choice(
			[
				('Daily', 0.10),
				('Weekly', 0.30),
				('Monthly', 0.35),
				('Rarely', 0.20),
				('Never', 0.05),
			]
		)
	monthly_mobile_spend_naira = (
		random.randint(300, 6000) if smartphone_owner else random.randint(100, 1200)
	)
	social_media_usage = random.choice(SOCIAL_MEDIA_USAGE_CATS) if smartphone_owner else 'None'
	ecommerce_activity = (
		random.choices([True, False], weights=[0.15, 0.85])[0] if smartphone_owner else False
	)
	active_on_agri_forums = (
		random.choices([True, False], weights=[0.15, 0.85])[0] if smartphone_owner else False
	)
	digital_footprint_score_1_10 = random.randint(1, 10)

	# Alternative Payment Data
	utility_bill_payment_score_1_10 = random.randint(1, 10)
	mobile_money_activity_score_1_10 = (
		random.randint(1, 10) if mobile_money_usage_frequency != 'Never' else 1
	)
	utility_payment_timeliness = random.choice(UTILITY_PAYMENT_TIMELINESS_CATS)
	rent_payment_timeliness = (
		random.choice(UTILITY_PAYMENT_TIMELINESS_CATS + ['N/A'])
		if land_acquisition_method in ['Lease', 'Rental']
		else 'N/A'
	)
	phone_bill_timeliness = random.choice(UTILITY_PAYMENT_TIMELINESS_CATS)
	last_utility_payment_date = fake.date_between(start_date='-100d', end_date='today')
	last_rent_payment_date = (
		fake.date_between(start_date='-70d', end_date='today')
		if rent_payment_timeliness != 'N/A'
		else None
	)

	# Value Chain Platform
	value_chain_platform_registered = random.choices([True, False], weights=[0.25, 0.75])[
		0
	]  # Lower registration rate
	years_on_platform = 0
	marketplace_sales_ngn_last_year = 0
	if value_chain_platform_registered:
		years_on_platform = random.randint(0, 4)
		if years_on_platform > 0:
			marketplace_sales_ngn_last_year = random.uniform(
				0.1, 0.6
			)  # Factor of potential revenue

	# Cooperative
	cooperative_member = random.choices([True, False], weights=[0.40, 0.60])[
		0
	]  # Keep as is, distinct from extension
	cooperative_repayment_rate_percent = random.randint(60, 100) if cooperative_member else 0

	# Distances
	distance_to_market_km = round(random.uniform(0.5, 70), 1)  # Wider range possible
	distance_to_bank_km = (
		round(random.uniform(1, 100), 1) if has_bank_account else round(random.uniform(10, 150), 1)
	)

	# --- Calculations requiring generated data ---
	temp_row_for_calc = {
		'primary_crop': primary_crop,
		'education_category': education_category,
		'uses_improved_seeds': uses_improved_seeds,
		'uses_fertilizer': uses_fertilizer,
		'uses_irrigation': uses_irrigation,
		'farming_experience_years': farming_experience_years,
		'farm_size_ha': farm_size_ha,
		'pest_disease_control_method': pest_disease_control_method,
		'has_off_farm_income': has_off_farm_income,
		'cooperative_member': cooperative_member,
		'gender': gender,
		'uses_extension_services': uses_extension_services,  # Pass gender for expense calc
	}

	annual_farm_yield_tons_per_ha = calculate_yield_tons_per_ha(temp_row_for_calc)
	total_production_tons = round(farm_size_ha * annual_farm_yield_tons_per_ha, 2)
	crop_price_per_ton = CROP_PRICES_NAIRA_PER_TON.get(primary_crop, 150000)
	annual_farm_revenue_ngn = round(total_production_tons * crop_price_per_ton, -3)

	annual_farm_expenses_ngn = calculate_annual_farm_expenses_ngn(temp_row_for_calc)
	farm_profit_ngn = annual_farm_revenue_ngn - annual_farm_expenses_ngn

	annual_off_farm_income_ngn = generate_off_farm_income_ngn(temp_row_for_calc)
	total_annual_income_ngn = annual_farm_revenue_ngn + annual_off_farm_income_ngn
	income_per_capita_ngn = round(total_annual_income_ngn / max(1, household_size), 0)

	if value_chain_platform_registered and years_on_platform > 0:
		marketplace_sales_ngn_last_year = round(
			marketplace_sales_ngn_last_year * annual_farm_revenue_ngn, -3
		)
	else:
		marketplace_sales_ngn_last_year = 0

	# Crop Disposition Estimation (Simplified based on Table 6.12 averages)
	crop_disposition = {
		'Stored': 0.40,
		'Sold Unprocessed': 0.25,
		'Sold Processed': 0.05,
		'Consumed': 0.25,
		'Given Out': 0.04,
		'Lost': 0.01,
	}  # Generic average
	if primary_crop == 'Cassava':
		crop_disposition = {
			'Stored': 0.10,
			'Sold Unprocessed': 0.28,
			'Sold Processed': 0.17,
			'Consumed': 0.36,
			'Given Out': 0.06,
			'Lost': 0.005,
		}
	elif primary_crop == 'Yam':
		crop_disposition = {
			'Stored': 0.41,
			'Sold Unprocessed': 0.20,
			'Sold Processed': 0.01,
			'Consumed': 0.31,
			'Given Out': 0.05,
			'Lost': 0.01,
		}
	elif primary_crop == 'Maize':
		crop_disposition = {
			'Stored': 0.41,
			'Sold Unprocessed': 0.25,
			'Sold Processed': 0.00,
			'Consumed': 0.24,
			'Given Out': 0.05,
			'Lost': 0.003,
		}
	elif primary_crop in ['Sorghum', 'Millet', 'Guinea Corn']:
		crop_disposition = {
			'Stored': 0.66,
			'Sold Unprocessed': 0.07,
			'Sold Processed': 0.00,
			'Consumed': 0.19,
			'Given Out': 0.04,
			'Lost': 0.001,
		}
	elif primary_crop == 'Rice':
		crop_disposition = {
			'Stored': 0.56,
			'Sold Unprocessed': 0.27,
			'Sold Processed': 0.01,
			'Consumed': 0.10,
			'Given Out': 0.03,
			'Lost': 0.001,
		}
	elif primary_crop == 'Groundnut':
		crop_disposition = {
			'Stored': 0.54,
			'Sold Unprocessed': 0.32,
			'Sold Processed': 0.01,
			'Consumed': 0.09,
			'Given Out': 0.03,
			'Lost': 0.001,
		}
	elif primary_crop in ['Cowpea', 'Beans']:
		crop_disposition = {
			'Stored': 0.47,
			'Sold Unprocessed': 0.22,
			'Sold Processed': 0.01,
			'Consumed': 0.24,
			'Given Out': 0.03,
			'Lost': 0.001,
		}
	percentage_sold_unprocessed = round(
		crop_disposition['Sold Unprocessed'] * 100 * random.uniform(0.8, 1.2), 1
	)
	percentage_consumed = round(crop_disposition['Consumed'] * 100 * random.uniform(0.8, 1.2), 1)

	# Prior Loan (using calculated revenues)
	has_prior_loan = random.choices([True, False], weights=[0.25, 0.75])[0]  # Lower prior loan rate
	prior_loan_data = generate_prior_loan_details(
		{
			**temp_row_for_calc,
			'has_prior_loan': has_prior_loan,
			'annual_farm_revenue_ngn': annual_farm_revenue_ngn,
			'farm_profit_ngn': farm_profit_ngn,
		}
	)

	# Current Loan Request
	requests_loan_now = random.choices([True, False], weights=[0.5, 0.5])[
		0
	]  # Lower request rate maybe
	loan_amount_requested_ngn = 0
	current_loan_purpose = 'N/A'
	current_loan_tenure_months = 0

	if requests_loan_now:
		# Request amount based on need/capacity, maybe related to expenses or desired investment
		max_sensible_request = max(annual_farm_expenses_ngn * 0.8, total_annual_income_ngn * 0.5)
		loan_amount_requested_ngn = (
			round(random.uniform(20000, max(50000, max_sensible_request * 1.5)) / 5000, 0) * 5000
		)  # Round to 5k
		if value_chain_platform_registered and random.random() < 0.7:
			current_loan_purpose = random.choice(LOAN_PRODUCTS_PLATFORM)
		else:
			current_loan_purpose = random.choice(LOAN_PRODUCTS_PLATFORM + LOAN_PURPOSES_GENERAL)
		current_loan_tenure_months = random.choice([3, 6, 9, 12, 18, 24])

	# Full row for credit score and other final calculations
	full_row_for_scoring = {
		'education_category': education_category,
		'has_bank_account': has_bank_account,
		'has_formal_id': has_formal_id,
		'mobile_money_usage_frequency': mobile_money_usage_frequency,
		'farming_experience_years': farming_experience_years,
		'has_off_farm_income': has_off_farm_income,
		'yield_consistency_rating': yield_consistency_rating,
		'utility_bill_payment_score_1_10': utility_bill_payment_score_1_10,
		'mobile_money_activity_score_1_10': mobile_money_activity_score_1_10,
		'phone_bill_timeliness': phone_bill_timeliness,
		'land_acquisition_method': land_acquisition_method,
		'has_land_title': has_land_title,
		'has_prior_loan': has_prior_loan,
		'prior_loan_repayment_history': prior_loan_data['prior_loan_repayment_history'],
		'prior_loan_repayment_rate': prior_loan_data['prior_loan_repayment_rate'],
		'cooperative_member': cooperative_member,
		'uses_improved_seeds': uses_improved_seeds,
		'uses_fertilizer': uses_fertilizer,
		'uses_irrigation': uses_irrigation,
		'has_weather_insurance': has_weather_insurance,
		'has_storage_facility': has_storage_facility,
		'smartphone_owner': smartphone_owner,
		'digital_footprint_score_1_10': digital_footprint_score_1_10,
		'value_chain_platform_registered': value_chain_platform_registered,
		'years_on_platform': years_on_platform,
		'farm_profit_ngn': farm_profit_ngn,
		'annual_farm_revenue_ngn': annual_farm_revenue_ngn,
		'total_annual_income_ngn': total_annual_income_ngn,
		'loan_amount_requested_ngn': loan_amount_requested_ngn,
		'uses_extension_services': uses_extension_services,
		'owns_tractor': owns_tractor,
		'owns_plow': owns_plow,
		'owns_sprayer': owns_sprayer,
	}
	credit_score = calculate_credit_score(full_row_for_scoring)
	full_row_for_scoring['credit_score'] = credit_score  # Add this line
	creditworthiness_category = determine_creditworthiness_category(credit_score)
	max_recommended_loan_ngn = calculate_max_recommended_loan_ngn(full_row_for_scoring)
	suitable_loan_products = determine_suitable_loan_products(
		{**full_row_for_scoring, 'credit_score': credit_score, 'farm_size_ha': farm_size_ha}
	)

	predicted_default_prob = 0.0
	predicted_loan_repayment_outcome = 'N/A'
	if requests_loan_now:
		predicted_default_prob = calculate_predicted_default_probability(
			{**full_row_for_scoring, 'credit_score': credit_score}
		)
		# Assign outcome based on probability bands
		if predicted_default_prob < 0.12:
			predicted_loan_repayment_outcome = 'Likely Full Repayment'
		elif predicted_default_prob < 0.30:
			predicted_loan_repayment_outcome = 'Likely Partial Repayment'
		elif predicted_default_prob < 0.55:
			predicted_loan_repayment_outcome = 'High Risk of Default'
		else:
			predicted_loan_repayment_outcome = 'Very High Risk of Default'

	farm_size_category = pd.cut(
		[farm_size_ha],
		bins=[0, 1, 5, 10, float('inf')],
		labels=['Subsistence (<1ha)', 'Small (1-5ha)', 'Medium (5-10ha)', 'Large (>10ha)'],
		right=False,
	)[0]

	all_farmer_data.append(
		{
			'farmer_id': farmer_id,
			'age': age,
			'gender': gender,
			'education_category': education_category,
			'education_level_years': education_level_years,
			'marital_status': marital_status,
			'household_size': household_size,
			'state': state,
			'region': region,
			'has_off_farm_income': has_off_farm_income,
			'annual_off_farm_income_ngn': annual_off_farm_income_ngn,
			'farming_experience_years': farming_experience_years,
			'farm_size_ha': farm_size_ha,
			'farm_size_category': farm_size_category,
			'land_acquisition_method': land_acquisition_method,
			'has_land_title': has_land_title,
			'primary_crop': primary_crop,
			'secondary_crop': secondary_crop,
			'owns_livestock': owns_livestock,
			'livestock_type': livestock_type,
			'primary_livestock_use': primary_livestock_use,
			'uses_improved_seeds': uses_improved_seeds,
			'uses_fertilizer': uses_fertilizer,
			'uses_irrigation': uses_irrigation,
			'pest_disease_control_method': pest_disease_control_method,
			'soil_type_known': soil_type_known,
			'uses_extension_services': uses_extension_services,
			'annual_farm_yield_tons_per_ha': annual_farm_yield_tons_per_ha,
			'total_production_tons': total_production_tons,
			'crop_price_per_ton_ngn': crop_price_per_ton,
			'annual_farm_revenue_ngn': annual_farm_revenue_ngn,
			'annual_farm_expenses_ngn': annual_farm_expenses_ngn,
			'farm_profit_ngn': farm_profit_ngn,
			'total_annual_income_ngn': total_annual_income_ngn,
			'income_per_capita_ngn': income_per_capita_ngn,
			'yield_consistency_rating': yield_consistency_rating,
			'post_harvest_loss_perc': post_harvest_loss_perc,
			'percentage_sold_unprocessed': percentage_sold_unprocessed,
			'percentage_consumed': percentage_consumed,
			'has_storage_facility': has_storage_facility,
			'has_weather_insurance': has_weather_insurance,
			'owns_tractor': owns_tractor,
			'owns_plow': owns_plow,
			'owns_sprayer': owns_sprayer,
			'owns_wheelbarrow': owns_wheelbarrow,
			'owns_cutlass': owns_cutlass,
			'owns_sickle': owns_sickle,
			'has_bank_account': has_bank_account,
			'has_formal_id': has_formal_id,
			'smartphone_owner': smartphone_owner,
			'mobile_money_usage_frequency': mobile_money_usage_frequency,
			'monthly_mobile_spend_naira': monthly_mobile_spend_naira,
			'social_media_usage': social_media_usage,
			'ecommerce_activity': ecommerce_activity,
			'active_on_agri_forums': active_on_agri_forums,
			'digital_footprint_score_1_10': digital_footprint_score_1_10,
			'utility_bill_payment_score_1_10': utility_bill_payment_score_1_10,
			'mobile_money_activity_score_1_10': mobile_money_activity_score_1_10,
			'utility_payment_timeliness': utility_payment_timeliness,
			'rent_payment_timeliness': rent_payment_timeliness,
			'phone_bill_timeliness': phone_bill_timeliness,
			'last_utility_payment_date': last_utility_payment_date,
			'last_rent_payment_date': last_rent_payment_date,
			'cooperative_member': cooperative_member,
			'cooperative_repayment_rate_percent': cooperative_repayment_rate_percent,
			'value_chain_platform_registered': value_chain_platform_registered,
			'years_on_platform': years_on_platform,
			'marketplace_sales_ngn_last_year': marketplace_sales_ngn_last_year,
			'distance_to_market_km': distance_to_market_km,
			'distance_to_bank_km': distance_to_bank_km,
			'has_prior_loan': has_prior_loan,
			'prior_loan_amount_ngn': prior_loan_data['prior_loan_amount_ngn'],
			'prior_loan_repayment_rate': prior_loan_data['prior_loan_repayment_rate'],
			'prior_loan_repayment_history': prior_loan_data['prior_loan_repayment_history'],
			'prior_loan_purpose': prior_loan_data['prior_loan_purpose'],
			'requests_loan_now': requests_loan_now,
			'loan_amount_requested_ngn': loan_amount_requested_ngn,
			'current_loan_purpose': current_loan_purpose,
			'current_loan_tenure_months': current_loan_tenure_months,
			'credit_score': credit_score,
			'creditworthiness_category': creditworthiness_category,
			'max_recommended_loan_ngn': max_recommended_loan_ngn,
			'suitable_loan_products': suitable_loan_products,
			'predicted_default_probability_current_loan': predicted_default_prob
			if requests_loan_now
			else 0.0,
			'predicted_loan_repayment_outcome': predicted_loan_repayment_outcome
			if requests_loan_now
			else 'N/A',
		}
	)

df_farmers = pd.DataFrame(all_farmer_data)

# --- Post-Generation Analysis & Output ---
print(f'Generated dataset with {len(df_farmers)} farmers.')

# Save to CSV
df_farmers.to_csv(OUTPUT_FILENAME, index=False)
print(f'Master data saved to {OUTPUT_FILENAME}')

# # Example Summaries
# print('\n--- Data Summary ---')
# print(f'Average credit score: {df_farmers["credit_score"].mean():.0f}')
# print(f'Creditworthiness distribution:\n{df_farmers["creditworthiness_category"].value_counts(normalize=True).apply(lambda x: f"{x:.1%}")}')
# print(f'Average farm size: {df_farmers["farm_size_ha"].mean():.2f} hectares')
# print(f'Average total annual income: ₦{df_farmers["total_annual_income_ngn"].mean():,.0f}')
# print(f'Average predicted default probability (for loan requesters): {df_farmers[df_farmers["requests_loan_now"]]["predicted_default_probability_current_loan"].mean():.2%}')
# print(f'Input Usage: Fertilizer: {df_farmers["uses_fertilizer"].mean():.1%}, Improved Seeds: {df_farmers["uses_improved_seeds"].mean():.1%}, Irrigation: {df_farmers["uses_irrigation"].mean():.1%}')
# print(f'Land Acquisition Method Distribution:\n{df_farmers["land_acquisition_method"].value_counts(normalize=True).apply(lambda x: f"{x:.1%}")}')
# print(f'Livestock Ownership: {df_farmers["owns_livestock"].mean():.1%}')
# print(f'Extension Service Usage: {df_farmers["uses_extension_services"].mean():.1%}')
# print(f'Distribution of primary crops (Top 5):\n{df_farmers["primary_crop"].value_counts(normalize=True).head().apply(lambda x: f"{x:.1%}")}')
# print(f'Distribution of livestock types (Top 5 for owners):\n{df_farmers[df_farmers["owns_livestock"]]["livestock_type"].value_counts(normalize=True).head().apply(lambda x: f"{x:.1%}")}')
