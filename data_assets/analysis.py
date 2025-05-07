import os
import random
import pandas as pd
import numpy as np
from faker import Faker
import datetime

# --- Configuration & Constants ---
NUM_FARMERS = 10000  # Number of unique farmers to generate. Adjust as needed.
MAX_ENTERPRISES_PER_FARMER = 3
MAX_LOANS_PER_ENTERPRISE = 2
OUTPUT_DIR = 'simplified_farmer_data_output'

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize Faker
fake = Faker() # Using Nigerian locale for names

# Set seeds for reproducibility
np.random.seed(42)
random.seed(42)

# --- Data Definitions (Adapted from original script and PDF) ---
NIGERIAN_STATES = [
    'Abia', 'Adamawa', 'Akwa Ibom', 'Anambra', 'Bauchi', 'Bayelsa', 'Benue', 'Borno',
    'Cross River', 'Delta', 'Ebonyi', 'Edo', 'Ekiti', 'Enugu', 'Gombe', 'Imo',
    'Jigawa', 'Kaduna', 'Kano', 'Katsina', 'Kebbi', 'Kogi', 'Kwara', 'Lagos',
    'Nasarawa', 'Niger', 'Ogun', 'Ondo', 'Osun', 'Oyo', 'Plateau', 'Rivers',
    'Sokoto', 'Taraba', 'Yobe', 'Zamfara', 'FCT',
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

EDUCATION_LEVELS_MAPPING = { # From original script, maps category to years
    'No Formal Education': 0,
    'Primary Incomplete': 3,
    'Primary Complete': 6,
    'Secondary Incomplete': 9,
    'Secondary Complete': 12,
    'OND/NCE': 14,
    'HND/BSc': 16,
    'Masters/PhD': 18,
}
# We will directly generate years of education, but these categories help define realistic ranges.

MARITAL_STATUSES = ['Single', 'Married', 'Divorced', 'Widowed']
YES_NO = ['Yes', 'No']
GENDERS = ['Male', 'Female']

ENTERPRISE_TYPES = ['Crop', 'Livestock', 'Fish Farming']
PRIMARY_CROPS_LIST = ['Maize', 'Cassava', 'Sorghum', 'Yam', 'Cowpea', 'Rice', 'Millet', 'Groundnut', 'Vegetables', 'Oil Palm', 'Cocoa', 'Plantain', 'Soybean', 'Sesame', 'Tomato']
SECONDARY_CROPS_LIST = PRIMARY_CROPS_LIST + ['None'] # 'None' indicates no secondary crop
LIVESTOCK_TYPES_LIST = ['Poultry', 'Goats', 'Sheep', 'Cattle', 'Pigs']
# For Fish Farming, we can just note the type as 'Fish' or specific fish types if needed.

FARM_SIZE_CATEGORIES = ['Subsistence', 'Small', 'Medium', 'Large']
FARMING_EQUIPMENT_TYPES = ['Traditional', 'Modern', 'Integrated']

LOAN_SOURCES = ['Commercial Bank', 'Microfinance Bank', 'Cooperative', 'Bank of Agriculture', 'Informal Lender', 'Family/Friends', 'Government Program']
DEFAULT_REASONS = ['Market Loss', 'Low/Poor Yield', 'Illness of Farmer', 'Pest Attack', 'Drought/Flood', 'Diversion of Funds', 'Input Price Hike', 'Policy Change', 'Other']
CREDIT_WORTHINESS_STATUSES = ['Creditworthy', 'Non-creditworthy']
LOAN_USE_STATUSES = ['Yes', 'No'] # Used as intended?

# --- Helper Function ---
def weighted_choice(choices_weights):
    """Selects an item based on weights."""
    choices, weights = zip(*choices_weights)
    total_weight = sum(weights)
    if not np.isclose(total_weight, 1.0) and total_weight > 0: # Normalize if not already
        weights = [w / total_weight for w in weights]
    elif total_weight == 0: # If all weights are zero, choose uniformly or handle error
        return random.choice(choices) if choices else None
    return random.choices(choices, weights=weights, k=1)[0]

def get_realistic_education_years(age):
    """Generates a realistic number of education years based on age."""
    if age < 6: return 0 # Too young for formal schooling
    
    max_possible_schooling_years = age - 6 # Assuming schooling starts at 6
    
    # Define education categories and their typical year ranges for realism
    # These are illustrative weights for different age groups
    if age < 18: # Young, likely still in or just finished secondary
        possible_education_weights = [
            (0, 0.3), (3, 0.2), (6, 0.2), (9, 0.2), (12, 0.1) # No formal to Secondary Complete
        ]
    elif age < 25: # Young adult, could have some tertiary
        possible_education_weights = [
            (0, 0.1), (6, 0.15), (9, 0.15), (12, 0.3), (14, 0.2), (16, 0.1) # Up to HND/BSc
        ]
    else: # Older adults, wider range of possibilities
        possible_education_weights = [
            (0, 0.20), (3, 0.10), (6, 0.20), (9, 0.10), (12, 0.20), 
            (14, 0.10), (16, 0.07), (18, 0.03) # Full range
        ]
        
    # Filter choices to be within max_possible_schooling_years
    valid_choices = [(years, weight) for years, weight in possible_education_weights if years <= max_possible_schooling_years]
    
    if not valid_choices: # Fallback if age is too low for any defined levels
        return 0 
        
    return weighted_choice(valid_choices)

def get_farm_size_category(enterprise_type, farm_size_value):
    """Determines farm size category based on type and value."""
    if enterprise_type == 'Crop':
        if farm_size_value < 1: return 'Subsistence'
        if farm_size_value < 5: return 'Small'
        if farm_size_value < 10: return 'Medium'
        return 'Large'
    elif enterprise_type == 'Livestock': # Example thresholds for livestock (e.g., head count)
        if farm_size_value < 10: return 'Subsistence' # e.g. <10 poultry or <5 goats
        if farm_size_value < 50: return 'Small'
        if farm_size_value < 200: return 'Medium'
        return 'Large'
    elif enterprise_type == 'Fish Farming': # Example thresholds for fish (e.g., number of ponds or stock)
        if farm_size_value < 100: return 'Subsistence' # e.g. <100 fish in a small pond
        if farm_size_value < 500: return 'Small'
        if farm_size_value < 2000: return 'Medium'
        return 'Large'
    return 'Unknown'


# --- Data Storage ---
farmer_profiles_data = []
farm_enterprises_data = []
loan_records_data = []

# --- Counters for IDs ---
enterprise_id_counter = 1
loan_id_counter = 1

print(f"Generating data for {NUM_FARMERS} farmers...")

# --- Main Generation Loop ---
for i in range(NUM_FARMERS):
    farmer_id = f"FARMER_{i+1:05d}"
    
    # 1. Farmer_Profile Generation
    age = random.randint(18, 70) # Farmers typically start a bit older
    gender = random.choice(GENDERS)
    # name = fake.name_male() if gender == 'Male' else fake.name_female()
    
    education_level_years = get_realistic_education_years(age)

    # Marital Status (age-dependent)
    if age < 20:
        marital_status = weighted_choice([('Single', 0.9), ('Married', 0.1)])
    elif age < 30:
        marital_status = weighted_choice([('Single', 0.4), ('Married', 0.55), ('Divorced', 0.03), ('Widowed', 0.02)])
    else: # age >= 30
        marital_status = weighted_choice([('Single', 0.1), ('Married', 0.7), ('Divorced', 0.05), ('Widowed', 0.15)])

    # Household Size (dependent on marital status and age)
    if marital_status == 'Single':
        household_size = random.randint(1, 3) if age < 25 else random.randint(1, 5)
    elif marital_status == 'Married':
        min_hh = 2
        if age < 25: household_size = random.randint(min_hh, min_hh + 2) # 2-4
        elif age < 40: household_size = random.randint(min_hh, min_hh + 5) # 2-7
        else: household_size = random.randint(min_hh, min_hh + 8) # 2-10
    else: # Divorced/Widowed
        household_size = random.randint(1, 6)
    household_size = max(1, household_size) # Ensure at least 1

    off_farm_income = 0
    if random.random() < 0.45: # 45% have off-farm income
        # Income can be related to education
        if education_level_years == 0: base_off_farm = 50000
        elif education_level_years <= 6: base_off_farm = 100000
        elif education_level_years <= 12: base_off_farm = 200000
        else: base_off_farm = 350000
        off_farm_income = round(random.uniform(0.5, 1.5) * base_off_farm / 1000) * 1000 # Annual

    state = random.choice(NIGERIAN_STATES)
    region = STATE_TO_REGION[state]
    has_bank_account = random.choices(YES_NO, weights=[0.6, 0.4])[0] # 60% have bank account
    owns_smartphone = random.choices(YES_NO, weights=[0.55, 0.45])[0] # 55% own smartphone
    uses_mobile_money = 'No'
    if owns_smartphone == 'Yes':
        uses_mobile_money = random.choices(YES_NO, weights=[0.7, 0.3])[0] # 70% of smartphone owners use mobile money

    farmer_profiles_data.append({
        "Farmer_ID": farmer_id,
        "Age": age,
        "Gender": gender,
        "Education_Level": education_level_years, # This is years of schooling
        "Marital_Status": marital_status,
        "Household_Size": household_size,
        "Offfarm_Income": off_farm_income,
        "Region": region,
        "State": state,
        "Has_Bank_Account": has_bank_account,
        "Owns_Smartphone": owns_smartphone,
        "Uses_Mobile_Money": uses_mobile_money
    })

    # 2. Farm_Enterprise Generation (1 to MAX_ENTERPRISES_PER_FARMER per farmer)
    num_enterprises = random.randint(1, MAX_ENTERPRISES_PER_FARMER)
    farmer_total_farm_assets = 0 # Accumulate for this farmer

    for _ in range(num_enterprises):
        enterprise_id = f"ENT_{enterprise_id_counter:06d}"
        enterprise_id_counter += 1
        
        enterprise_type = random.choice(ENTERPRISE_TYPES)
        primary_crop_name = "N/A"
        secondary_crop_name = "N/A"
        uses_fertilizer_val = "N/A"
        uses_improved_seeds_val = "N/A"
        yield_per_hectare_val = 0
        farm_size_value = 0 # This will be ha for crop, count for livestock/fish

        if enterprise_type == 'Crop':
            primary_crop_name = random.choice(PRIMARY_CROPS_LIST)
            if random.random() > 0.4: # 60% chance of secondary crop
                secondary_crop_name = random.choice([c for c in SECONDARY_CROPS_LIST if c != primary_crop_name])
            else:
                secondary_crop_name = "None"
            
            farm_size_value = round(random.uniform(0.2, 15.0), 2) # Hectares
            uses_fertilizer_val = random.choices(YES_NO, weights=[0.4, 0.6])[0] # 40% use fertilizer
            uses_improved_seeds_val = random.choices(YES_NO, weights=[0.3, 0.7])[0] # 30% use improved seeds
            # Base yield (tons/ha), can be more specific per crop later
            base_yield = random.uniform(0.5, 5.0) 
            # Adjust yield based on inputs
            if uses_fertilizer_val == 'Yes': base_yield *= random.uniform(1.1, 1.3)
            if uses_improved_seeds_val == 'Yes': base_yield *= random.uniform(1.1, 1.4)
            yield_per_hectare_val = round(base_yield, 2)

        elif enterprise_type == 'Livestock':
            primary_crop_name = random.choice(LIVESTOCK_TYPES_LIST) # Using this field for livestock type
            farm_size_value = random.randint(5, 300) # Number of animals
        elif enterprise_type == 'Fish Farming':
            primary_crop_name = "Various Fish" # Placeholder for fish type
            farm_size_value = random.randint(50, 1000) # Number of fish or capacity

        farm_size_category_val = get_farm_size_category(enterprise_type, farm_size_value)
        
        # Farming experience in this specific enterprise type
        max_experience = age - 15 # Assuming farming starts around 15 for this enterprise
        farming_experience_val = random.randint(1, max(1, max_experience))
        
        farming_equipment_type_val = random.choice(FARMING_EQUIPMENT_TYPES)
        uses_irrigation_val = "N/A"
        depends_on_rain_val = "N/A"
        if enterprise_type == 'Crop':
            uses_irrigation_val = random.choices(YES_NO, weights=[0.1, 0.9])[0] # 10% use irrigation
            if uses_irrigation_val == 'Yes':
                depends_on_rain_val = random.choices(['No', 'Partially'], weights=[0.7, 0.3])[0]
            else:
                depends_on_rain_val = 'Yes'

        # Financials for the enterprise (Annual)
        # Simplified: base income on farm size and type
        base_income_factor = 100000 # Naira per unit of farm_size_value (ha or scaled count)
        if enterprise_type == 'Crop':
            # income influenced by yield and area
            farm_income_val = round(farm_size_value * yield_per_hectare_val * random.uniform(150000, 400000) / 1000) * 1000 # Price per ton
        elif enterprise_type == 'Livestock':
            farm_income_val = round(farm_size_value * random.uniform(5000, 20000) / 1000) * 1000 # Price per head over a cycle
        else: # Fish Farming
            farm_income_val = round(farm_size_value * random.uniform(1000, 5000) / 1000) * 1000 # Price per fish over a cycle
        
        farm_income_val = max(50000, farm_income_val) # Ensure some minimal income

        total_operating_expenditure_val = round(farm_income_val * random.uniform(0.4, 0.8) / 1000) * 1000 # OpEx is 40-80% of income
        profit_val = farm_income_val - total_operating_expenditure_val
        
        monthly_income_val = round(farm_income_val / 12 / 1000) * 1000
        monthly_expense_val = round(total_operating_expenditure_val / 12 / 1000) * 1000
        
        # Value of farm assets: can be related to farm size and equipment type
        asset_base = farm_size_value * random.uniform(50000, 200000) # Per ha or per 100 animals etc.
        if farming_equipment_type_val == 'Modern': asset_base *= 1.5
        if farming_equipment_type_val == 'Integrated': asset_base *= 1.2
        value_of_farm_assets_val = round(max(20000, asset_base) / 1000) * 1000
        farmer_total_farm_assets += value_of_farm_assets_val

        current_enterprise_data = {
            "Enterprise_ID": enterprise_id,
            "Farmer_ID": farmer_id,
            "Enterprise_Type": enterprise_type,
            "Primary_Crop": primary_crop_name, # Also used for livestock type
            "Secondary_Crop": secondary_crop_name,
            "Farm_Size": farm_size_value,
            "Farm_Size_Category": farm_size_category_val,
            "Farming_Experience": farming_experience_val,
            "Farming_Equipment_type": farming_equipment_type_val,
            "Uses_Irrigation": uses_irrigation_val,
            "Depends_on_Rain": depends_on_rain_val,
            "Uses_Fertilizer": uses_fertilizer_val,
            "Uses_Improved_Seeds": uses_improved_seeds_val,
            "Yield_per_Hectare": yield_per_hectare_val if enterprise_type == 'Crop' else 0, # Tons per hectare
            "Profit": profit_val,
            "Monthly_Income": monthly_income_val,
            "Monthly_Expense": monthly_expense_val,
            "Value_of_Farm_Assets": value_of_farm_assets_val,
            "Total_Operating_Expenditure": total_operating_expenditure_val,
            "Farm_Income": farm_income_val
        }
        farm_enterprises_data.append(current_enterprise_data)

        # 3. Loan_Record Generation (0 to MAX_LOANS_PER_ENTERPRISE per enterprise)
        num_loans = random.randint(0, MAX_LOANS_PER_ENTERPRISE)
        if profit_val < 20000 and random.random() > 0.3: # Less profitable enterprises less likely to get loans
            num_loans = 0
            
        for _ in range(num_loans):
            loan_id = f"LOAN_{loan_id_counter:07d}"
            loan_id_counter += 1

            # Loan amount related to enterprise assets or income
            max_loan_possible = min(value_of_farm_assets_val * 0.7, farm_income_val * 0.5)
            loan_amount_val = round(random.uniform(0.1, 0.8) * max_loan_possible / 5000) * 5000 # Multiples of 5000
            loan_amount_val = max(20000, loan_amount_val) # Min loan amount

            interest_rate_val = round(random.uniform(5.0, 35.0), 1) # Annual interest rate
            
            # Loan date within farmer's active period and enterprise existence
            # Assume enterprise started some years ago based on experience
            enterprise_start_year = datetime.date.today().year - farming_experience_val
            min_loan_year = max(enterprise_start_year, datetime.date.today().year - 10) # Loan in last 10 years or since enterprise start
            loan_year = random.randint(min_loan_year, datetime.date.today().year -1) # Loan taken in previous years
            loan_month = random.randint(1,12)
            loan_day = random.randint(1,28)
            loan_date_val = datetime.date(loan_year, loan_month, loan_day)

            loan_use_status_val = random.choice(LOAN_USE_STATUSES)
            duration_months_val = random.choice([6, 12, 18, 24, 36])
            
            has_defaulted_val = random.choices(YES_NO, weights=[0.15, 0.85])[0] # 15% default rate
            
            repayment_date_val = None
            loan_repayment_amount_val = 0
            if has_defaulted_val == 'No':
                # Full repayment if not defaulted
                loan_repayment_amount_val = round(loan_amount_val * (1 + (interest_rate_val / 100 * duration_months_val / 12)))
                # Repayment date after loan date + duration
                repayment_date_val = loan_date_val + datetime.timedelta(days=duration_months_val * 30)
                if repayment_date_val > datetime.date.today(): # If repayment is in future
                    repayment_date_val = None # Not yet fully repaid if due date is future
                    loan_repayment_amount_val = round(loan_amount_val * random.uniform(0, 0.8)) # Partially repaid
            else: # Defaulted
                loan_repayment_amount_val = round(loan_amount_val * random.uniform(0.1, 0.7)) # Partial repayment before default
                # Default might occur before full duration
                default_after_months = random.randint(1, duration_months_val -1) if duration_months_val > 1 else 1
                repayment_date_val = loan_date_val + datetime.timedelta(days=default_after_months * 30)


            loan_use_duration_val = random.randint(1, duration_months_val) # Actual time loan was used
            
            # Credit worthiness can be simple for now
            credit_worthiness_val = 'Creditworthy'
            if has_defaulted_val == 'Yes' or profit_val < 50000 : # Example condition
                 credit_worthiness_val = 'Non-creditworthy'
            elif off_farm_income > 100000 and has_bank_account == 'Yes':
                 credit_worthiness_val = 'Creditworthy'
            else:
                 credit_worthiness_val = random.choice(CREDIT_WORTHINESS_STATUSES)


            loan_asset_ratio_val = round(loan_amount_val / max(1, value_of_farm_assets_val), 2) if value_of_farm_assets_val > 0 else 0
            op_ex_income_ratio_val = round(total_operating_expenditure_val / max(1, farm_income_val), 2) if farm_income_val > 0 else 0
            
            loan_source_val = random.choice(LOAN_SOURCES)
            loan_supervision_freq_val = random.randint(0, 5) # Number of monitoring visits
            distance_to_lender_val = round(random.uniform(1, 100), 1) # km
            disbursement_lag_val = random.randint(0, 6) # Months delay
            
            default_reason_val = "N/A"
            if has_defaulted_val == 'Yes':
                default_reason_val = random.choice(DEFAULT_REASONS)

            loan_records_data.append({
                "Loan_ID": loan_id,
                "Farmer_ID": farmer_id,
                "Enterprise_ID": enterprise_id,
                "Loan_Amount": loan_amount_val,
                "Interest_Rate": interest_rate_val,
                "Loan_Date": loan_date_val.strftime('%Y-%m-%d') if loan_date_val else None,
                "Loan_Use_Status": loan_use_status_val,
                "Loan_Repayment_Amount": loan_repayment_amount_val,
                "Repayment_Date": repayment_date_val.strftime('%Y-%m-%d') if repayment_date_val else None,
                "Duration_Months": duration_months_val,
                "Loan_Use_Duration": loan_use_duration_val,
                "Credit_Worthiness_Status": credit_worthiness_val,
                "Loan_Asset_Ratio": loan_asset_ratio_val,
                "OpEx_Income_Ratio": op_ex_income_ratio_val,
                "Loan_Source": loan_source_val,
                "Loan_Supervision_Frequency": loan_supervision_freq_val,
                "Distance_to_Lender": distance_to_lender_val,
                "Disbursement_Lag": disbursement_lag_val,
                "Has_Defaulted": has_defaulted_val,
                "Default_Reason": default_reason_val
            })
    if (i + 1) % (NUM_FARMERS // 10) == 0: # Print progress
        print(f"Generated data for {i+1}/{NUM_FARMERS} farmers...")


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

print(f"\nData generation complete.")
print(f"Farmer Profiles saved to: {farmer_profiles_path} ({len(df_farmer_profiles)} records)")
print(f"Farm Enterprises saved to: {farm_enterprises_path} ({len(df_farm_enterprises)} records)")
print(f"Loan Records saved to: {loan_records_path} ({len(df_loan_records)} records)")

# --- Basic Validation/Summary (Optional) ---
print("\n--- Farmer Profiles Summary ---")
print(df_farmer_profiles.head())
print(f"\nAverage Age: {df_farmer_profiles['Age'].mean():.1f}")
print(f"Gender Distribution:\n{df_farmer_profiles['Gender'].value_counts(normalize=True).apply(lambda x: f'{x:.1%}')}")
print(f"Marital Status Distribution:\n{df_farmer_profiles['Marital_Status'].value_counts(normalize=True).apply(lambda x: f'{x:.1%}')}")

print("\n--- Farm Enterprises Summary ---")
print(df_farm_enterprises.head())
print(f"\nAverage Farm Income: NGN {df_farm_enterprises['Farm_Income'].mean():,.0f}")
print(f"Enterprise Type Distribution:\n{df_farm_enterprises['Enterprise_Type'].value_counts(normalize=True).apply(lambda x: f'{x:.1%}')}")

print("\n--- Loan Records Summary ---")
print(df_loan_records.head())
if not df_loan_records.empty:
    print(f"\nAverage Loan Amount: NGN {df_loan_records['Loan_Amount'].mean():,.0f}")
    print(f"Default Rate: {df_loan_records['Has_Defaulted'].value_counts(normalize=True).get('Yes', 0):.1%}")
    print(f"Credit Worthiness Distribution:\n{df_loan_records['Credit_Worthiness_Status'].value_counts(normalize=True).apply(lambda x: f'{x:.1%}')}")
else:
    print("No loan records generated.")

