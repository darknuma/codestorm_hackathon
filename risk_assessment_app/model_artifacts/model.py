import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import shap 
import matplotlib.pyplot as plt 
import joblib 
import os

# --- Configuration ---
DATA_FILE = 'data/master_nigerian_farmer_data.csv' 
MODEL_OUTPUT_DIR = 'model_artifacts'
RISK_ASSESSMENT_DIR = 'risk_assessment_app'

os.makedirs(MODEL_OUTPUT_DIR, exist_ok=True)
os.makedirs(RISK_ASSESSMENT_DIR, exist_ok=True)

FULL_MODEL_DIR = os.path.join(RISK_ASSESSMENT_DIR, MODEL_OUTPUT_DIR)
os.makedirs(FULL_MODEL_DIR, exist_ok=True)

# Paths
MODEL_PATH = os.path.join(FULL_MODEL_DIR, 'xgb_risk_model.joblib')
PREPROCESSOR_PATH = os.path.join(FULL_MODEL_DIR, 'preprocessor.joblib')
FEATURE_NAMES_PATH = os.path.join(FULL_MODEL_DIR, 'feature_names.joblib')
MITIGATION_KB_PATH = os.path.join(FULL_MODEL_DIR, 'mitigation_kb.joblib')  # Stays in base dir
ORIGINAL_COLUMNS_PATH = os.path.join(FULL_MODEL_DIR, 'original_columns.joblib')


print(f"Loading data from {DATA_FILE}...")
try:
    df = pd.read_csv(DATA_FILE)
except FileNotFoundError:
    print(f"Error: The data file '{DATA_FILE}' was not found.")
    print("Please ensure the dataset is available at the specified path.")
    exit()

print("Data loaded successfully.")
print(f"Original dataset shape: {df.shape}")

# --- Preprocessing & Feature Engineering ---
print("\n--- Preprocessing and Feature Engineering ---")

# Filter for farmers who are currently requesting a loan
df_loan_requests = df[df['requests_loan_now'] == True].copy()
print(f"Dataset shape after filtering for loan requests: {df_loan_requests.shape}")

if df_loan_requests.empty:
    print("No farmers found who are requesting a loan. Exiting.")
    exit()

df_loan_requests['is_high_risk_default'] = df_loan_requests['predicted_loan_repayment_outcome'].apply(
    lambda x: 1 if x in ['High Risk of Default', 'Very High Risk of Default'] else 0
)

print("\nTarget variable 'is_high_risk_default' distribution:")
print(df_loan_requests['is_high_risk_default'].value_counts(normalize=True))

features_to_drop = [
    'farmer_id', 'requests_loan_now', 'predicted_loan_repayment_outcome',
    'credit_score', 'creditworthiness_category', 'max_recommended_loan_ngn',
    'suitable_loan_products', 'predicted_default_probability_current_loan',
    'state', 'region',
    'last_utility_payment_date', 'last_rent_payment_date',
    'is_high_risk_default'
]

X = df_loan_requests.drop(columns=features_to_drop, errors='ignore')
y = df_loan_requests['is_high_risk_default']



# Save original column order for the Streamlit app
original_columns = X.columns.tolist()
joblib.dump(original_columns, ORIGINAL_COLUMNS_PATH)
print(f"Original feature column names saved to {ORIGINAL_COLUMNS_PATH}")


print(f"\nShape of features (X): {X.shape}")
print(f"Shape of target (y): {y.shape}")

categorical_features = X.select_dtypes(include=['object', 'category']).columns.tolist()
boolean_features = X.select_dtypes(include=['bool']).columns.tolist()
numerical_features = X.select_dtypes(include=np.number).columns.tolist()

for bf in boolean_features:
    X[bf] = X[bf].astype(int)

numerical_features.extend(boolean_features) # Add converted booleans to numerical

numerical_pipeline = Pipeline([('scaler', StandardScaler())])
categorical_pipeline = Pipeline([('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_pipeline, numerical_features),
        ('cat', categorical_pipeline, categorical_features)
    ],
    remainder='drop' # Explicitly drop other columns if any, or use 'passthrough' if sure
)

# --- Train-Test Split ---
print("\n--- Splitting data into Training and Test sets ---")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
print(f"X_train shape: {X_train.shape}, X_test shape: {X_test.shape}")

# -- Process Model
X_train_processed = preprocessor.fit_transform(X_train)
X_test_processed = preprocessor.transform(X_test)

try:
    feature_names_from_preprocessor = preprocessor.get_feature_names_out()
except AttributeError:
    feature_names_from_preprocessor = []
    for name, trans, cols_list in preprocessor.transformers_: 
        if name == 'num':
            feature_names_from_preprocessor.extend(cols_list)
        elif name == 'cat':
            if hasattr(trans, 'get_feature_names_out'):
                 feature_names_from_preprocessor.extend(trans.get_feature_names_out(cols_list))
            elif hasattr(trans.named_steps['onehot'], 'get_feature_names_out'): # if pipeline
                 feature_names_from_preprocessor.extend(trans.named_steps['onehot'].get_feature_names_out(cols_list))
            else:
                 ohe_categories = trans.named_steps['onehot'].categories_
                 for i, col_name in enumerate(cols_list): # Corrected variable name
                     for cat_val in ohe_categories[i]:
                         feature_names_from_preprocessor.append(f"{col_name}__{cat_val}")


X_train_processed_df = pd.DataFrame(X_train_processed, columns=feature_names_from_preprocessor, index=X_train.index)
X_test_processed_df = pd.DataFrame(X_test_processed, columns=feature_names_from_preprocessor, index=X_test.index)

X_train_processed_df.columns = X_train_processed_df.columns.str.replace(r"[\[\]<>]", "_", regex=True)
X_test_processed_df.columns = X_test_processed_df.columns.str.replace(r"[\[\]<>]", "_", regex=True)

final_model_feature_names = list(X_train_processed_df.columns)

assert all(isinstance(col, str) and not any(c in col for c in '[]<') for col in X_train_processed_df.columns)

print("\n--- Training XGBoost Classifier ---")


scale_pos_weight_val = y_train.value_counts()[0] / y_train.value_counts()[1] if y_train.value_counts()[1] != 0 else 1

xgb_model = xgb.XGBClassifier(
    objective='binary:logistic',
    eval_metric='logloss',
    use_label_encoder=False, 
    random_state=42,
    scale_pos_weight=scale_pos_weight_val
)

xgb_model.fit(X_train_processed_df, y_train) 
print("XGBoost model trained.")


# --- 5. Model Evaluation ---
print("\n--- Model Evaluation ---")
y_pred_train = xgb_model.predict(X_train_processed_df)
y_pred_test = xgb_model.predict(X_test_processed_df)

print("\nTraining Set Performance:")
print(f"Accuracy: {accuracy_score(y_train, y_pred_train):.4f}")
print(classification_report(y_train, y_pred_train))

print("\nTest Set Performance:")
print(f"Accuracy: {accuracy_score(y_test, y_pred_test):.4f}")
print(classification_report(y_test, y_pred_test))
print("\nConfusion Matrix (Test Set):")
print(confusion_matrix(y_test, y_pred_test))

# ---  Risk Factor Identification (SHAP) ---
print("\n--- Risk Factor Identification ---")
print("\nCalculating SHAP values...")
explainer = shap.TreeExplainer(xgb_model)
shap_values = explainer.shap_values(X_test_processed_df)

print("Generating SHAP summary plot...")
shap.summary_plot(shap_values, X_test_processed_df, plot_type="bar", show=False)
plt.title("SHAP Feature Importance (Test Set)")
plt.savefig(os.path.join(FULL_MODEL_DIR, "shap_summary_bar_plot.png"), bbox_inches='tight')
plt.close()
print(f"SHAP summary bar plot saved to {os.path.join(FULL_MODEL_DIR, 'shap_summary_bar_plot.png')}")

shap.summary_plot(shap_values, X_test_processed_df, show=False)
plt.title("SHAP Feature Contributions (Test Set)")
plt.savefig(os.path.join(FULL_MODEL_DIR, "shap_summary_dot_plot.png"), bbox_inches='tight')
plt.close()
print(f"SHAP summary dot plot saved to {os.path.join(FULL_MODEL_DIR, 'shap_summary_dot_plot.png')}")

# --- Mitigation Strategy Outline (Conceptual) ---
# This knowledge base will be saved and used by the Streamlit app
mitigation_knowledge_base = {
    # Socio-Economic
    'education_level_years': "Consider adult literacy programs or agricultural training to improve financial understanding and farm management skills.",
    'education_category__No Formal Education': "Enroll in basic literacy and numeracy programs. Seek simplified financial education.", # Example for one-hot encoded feature
    'household_size': "For large households with low income per capita, explore income diversification for other adult members or family planning resources.",
    # Farm Characteristics & Practices
    'annual_farm_yield_tons_per_ha': "Improve yields by adopting better agronomic practices, using improved seeds, or soil testing.",
    # Matching one-hot encoded boolean features (original_feature__Value)
    # The one-hot encoder will create features like 'uses_improved_seeds_0' and 'uses_improved_seeds_1' if it was object/category
    # Since we converted booleans to int (0/1) and scaled them, their names will be like 'uses_improved_seeds'
    # If a boolean feature 'uses_improved_seeds' (0 for False, 1 for True) has a high SHAP value pushing towards risk,
    # it means either its 0 value is risky or its 1 value is risky.
    # For boolean features converted to int and scaled:
    # A positive SHAP for 'uses_improved_seeds' means higher value (1=True) increases risk (counterintuitive, check model)
    # A negative SHAP for 'uses_improved_seeds' means higher value (1=True) decreases risk.
    # So, if 'uses_improved_seeds' has a positive SHAP and its value is 1 (True), it's an anomaly.
    # If 'uses_improved_seeds' has a positive SHAP and its value is 0 (False), then 'uses_improved_seeds__False' is the risk.
    'uses_improved_seeds': "If not currently using improved seeds (value is low/0), adopt certified improved seed varieties suitable for your region to potentially boost yields and resilience.",
    'uses_fertilizer': "If not currently using fertilizer (value is low/0), conduct soil testing and apply appropriate fertilizers to improve soil fertility and crop output.",
    'uses_irrigation': "If not currently using irrigation (value is low/0), explore water harvesting techniques or affordable micro-irrigation options if water scarcity impacts your yields.",
    'pest_disease_control_method__None': "Implement basic pest and disease scouting and consider integrated pest management (IPM) strategies.",
    'pest_disease_control_method__Traditional': "While respecting traditional knowledge, explore combining it with proven IPM techniques for better efficacy.",
    'post_harvest_loss_perc': "Reduce post-harvest losses through training on improved harvesting, drying, and storage techniques. Consider investing in better on-farm storage. (If value is high)",
    'has_storage_facility': "If no storage facility (value is low/0), explore options for constructing or accessing affordable local storage solutions to reduce post-harvest losses and enable better market timing.",
    'uses_extension_services': "If not using extension services (value is low/0), connect with local agricultural extension services for advice on best practices, new technologies, and market information.",
    'yield_consistency_rating__Low': "Identify causes of yield inconsistency (e.g., weather, pests, soil) and adopt practices like crop rotation, soil conservation, or resilient varieties.",
    'yield_consistency_rating__Very Low': "Urgently address factors causing severe yield inconsistency. This might involve significant changes in farming practices or seeking expert advice.",
    # Financials
    'farm_profit_ngn': "If farm profit is low or negative, improve farm profitability by optimizing input costs, improving yields, reducing losses, or seeking better market prices.",
    'has_off_farm_income': "If no off-farm income (value is low/0), explore opportunities for off-farm income generation to diversify revenue streams and improve financial resilience.",
    # Financial Inclusion & Digital Footprint
    'has_bank_account': "If no bank account (value is low/0), open a formal bank account (even a basic one) to build a financial history and access formal financial services.",
    'mobile_money_usage_frequency__Never': "Start using mobile money for payments and transfers to build a digital transaction history and for convenience.",
    'mobile_money_usage_frequency__Rarely': "Increase the use of mobile money for regular transactions to build a stronger digital financial footprint.",
    # Alternative Payment Data
    'utility_payment_timeliness__Poor': "Prioritize timely payment of utility bills to demonstrate responsible financial management.",
    'utility_payment_timeliness__Fair': "Aim for consistent, on-time payment of all utility bills.",
    'phone_bill_timeliness__Poor': "Ensure phone bills are paid on time. This is an accessible way to show financial discipline.",
    # Social Capital
    'cooperative_member': "If not a cooperative member (value is low/0), consider joining a local farmer cooperative or association for benefits like group input purchasing, collective marketing, training, and peer support.",
    # Value Chain Integration
    'value_chain_platform_registered': "If not registered on a value chain platform (value is low/0), explore registering with agricultural value chain platforms for better market access, input sourcing, or potential financing opportunities.",
    'marketplace_sales_ngn_last_year': "If registered on a platform but sales are low, seek training on how to effectively use the marketplace or improve product quality/consistency for platform sales.",
    # Loan Characteristics
    'loan_amount_requested_ngn': "If the requested loan amount significantly strains your repayment capacity (high loan-to-income, check if value is high), consider starting with a smaller loan to build a positive repayment history.",
    'current_loan_purpose': "Ensure the loan is used for productive purposes that can generate returns to cover repayment. Avoid diverting funds to non-income-generating activities." # This is more general advice
}


# --- Save Model, Preprocessor, Feature Names, and Mitigation KB ---
print("\n--- Saving Model Artifacts ---")
joblib.dump(xgb_model, MODEL_PATH)
print(f"Trained XGBoost model saved to {MODEL_PATH}")

joblib.dump(preprocessor, PREPROCESSOR_PATH)
print(f"Preprocessor saved to {PREPROCESSOR_PATH}")

# Save the FINALIZED feature names that the model was trained on
joblib.dump(final_model_feature_names, FEATURE_NAMES_PATH) 
print(f"Final model feature names saved to {FEATURE_NAMES_PATH}") 

joblib.dump(mitigation_knowledge_base, MITIGATION_KB_PATH)
print(f"Mitigation knowledge base saved to {MITIGATION_KB_PATH}")

joblib.dump(final_model_feature_names, os.path.join(FULL_MODEL_DIR, "cleaned_columns.joblib"))


# --- Example: Suggest mitigation for a few high-risk farmers (from training script) ---
# This part is for demonstration within the training script; the Streamlit app will do this live.
def suggest_mitigation_for_farmer_demo(farmer_index, top_n_factors=3, X_processed_df_demo=X_test_processed_df, X_original_df_demo=X_test):
    # ... (It would use the globally defined xgb_model, explainer, feature_names_out, mitigation_knowledge_base)
    print(f"\n--- Mitigation Suggestions for Farmer (Test Set Index: {farmer_index}) ---")
    if farmer_index < 0 or farmer_index >= len(X_processed_df_demo):
        print(f"Error: Farmer index {farmer_index} is out of bounds.")
        return

    farmer_data_processed = X_processed_df_demo.iloc[[farmer_index]]
    farmer_original_data = X_original_df_demo.iloc[[farmer_index]]
    prediction = xgb_model.predict(farmer_data_processed)[0]
    prediction_proba = xgb_model.predict_proba(farmer_data_processed)[0][1]

    print("Original Farmer Data (sample features):")
    print(farmer_original_data[['age', 'education_category', 'farm_size_ha', 'primary_crop', 'farm_profit_ngn', 'cooperative_member']].to_string())
    print(f"Predicted Risk Status: {'High Risk' if prediction == 1 else 'Lower Risk'} (Probability of High Risk: {prediction_proba:.4f})")

    if prediction == 1:
        print("\nKey Factors Contributing to High Risk (from SHAP values):")
        current_shap_values = explainer.shap_values(farmer_data_processed)
        if isinstance(current_shap_values, list): current_shap_values = current_shap_values[1]

        shap_df = pd.DataFrame({
            'feature': final_model_feature_names,
            'shap_value': current_shap_values.flatten(),
            'feature_value': farmer_data_processed.values.flatten()
        })
        risk_driving_features = shap_df[shap_df['shap_value'] > 0.01].sort_values(by='shap_value', ascending=False) # Threshold for SHAP

        suggested_count = 0
        for _, row_shap in risk_driving_features.head(top_n_factors * 2).iterrows():
            if suggested_count >= top_n_factors: break
            feature_name = row_shap['feature']
            strategy = None
            
            # Direct match for processed feature name
            if feature_name in mitigation_knowledge_base:
                strategy = mitigation_knowledge_base[feature_name]
            
            elif '__' in feature_name: # One-hot encoded
                original_base_feature = feature_name.split('__')[0]
                # If the feature value is 1 (meaning this category is true for the farmer)
                # and this category being true is a risk factor
                if row_shap['feature_value'] == 1 and feature_name in mitigation_knowledge_base:
                    strategy = mitigation_knowledge_base[feature_name]
                elif original_base_feature in mitigation_knowledge_base: 
                    strategy = mitigation_knowledge_base[original_base_feature]

            elif X[feature_name].dtype == 'int' and (X[feature_name].isin([0,1]).all()): #
                if row_shap['feature_value'] == 0 and f"{feature_name}__False" in mitigation_knowledge_base:
                    strategy = mitigation_knowledge_base[f"{feature_name}__False"]
                elif row_shap['feature_value'] == 1 and f"{feature_name}__True" in mitigation_knowledge_base:
                     strategy = mitigation_knowledge_base[f"{feature_name}__True"]
                elif feature_name in mitigation_knowledge_base:
                    strategy = mitigation_knowledge_base[feature_name]


            if strategy:
                print(f"- Factor: {feature_name} (Processed Value: {row_shap['feature_value']:.2f})")
                original_col_name_candidate = feature_name.split('__')[0] if '__' in feature_name else feature_name
                if original_col_name_candidate in farmer_original_data.columns:
                    print(f"  Farmer's original value for '{original_col_name_candidate}': {farmer_original_data[original_col_name_candidate].iloc[0]}")
                print(f"  Suggestion: {strategy}")
                suggested_count += 1

        if suggested_count == 0:
            print("No specific actionable mitigation strategies found for the top risk factors based on the current knowledge base. General financial literacy and improved farm management are always beneficial.")
    else:
        print("Farmer is predicted as Lower Risk. Maintain good practices and explore opportunities for growth.")


if not X_test_processed_df.empty:
    y_test_reset = y_test.reset_index(drop=True)
    high_risk_indices_test = y_test_reset[y_test_reset == 1].index
    if not high_risk_indices_test.empty:
        print(f"\nFound {len(high_risk_indices_test)} high-risk farmers in the test set for demo.")
        sample_indices_to_explain = high_risk_indices_test[:min(2, len(high_risk_indices_test))] # Demo for 2 farmers
        for farmer_idx in sample_indices_to_explain:
            suggest_mitigation_for_farmer_demo(farmer_idx)
    else:
        print("\nNo high-risk farmers found in the test set for demo.")

print("\n--- Training and Artifact Saving Process Complete ---")
