"""Data generation module for the AgriFinance project.

This module is responsible for generating synthetic data for testing and
development purposes. It creates realistic datasets that mimic agricultural
and financial data patterns.
"""

import pandas as pd
import numpy as np


# Constants
NUMBER_OF_RECORDS = 1000
np.random.seed(42)  # For reproducibility


def generate_farmer_data():
    """Generate synthetic farmer data for analysis.

    Returns:
            pandas.DataFrame: A DataFrame containing synthetic farmer data with
            relevant features for credit scoring and analysis.
    """
    # Generate random data for demonstration
    data = {
        "age": np.random.randint(18, 65, NUMBER_OF_RECORDS),
        "gender": np.random.choice(["Male", "Female"], NUMBER_OF_RECORDS),
        "education_years": np.random.normal(10, 2, NUMBER_OF_RECORDS)
        .clip(0, 18)
        .astype(int),
        "household_size": np.random.randint(2, 10, NUMBER_OF_RECORDS),
        "farming_experience": np.random.randint(0, 20, NUMBER_OF_RECORDS),
        "farm_size": np.random.normal(2, 1, NUMBER_OF_RECORDS).clip(0.5, 10).round(2),
        "loan_amount": np.random.randint(50000, 500000, NUMBER_OF_RECORDS),
        "distance_to_bank": np.random.normal(10, 5, NUMBER_OF_RECORDS).clip(1, 30),
        "loan_supervision": np.random.poisson(2, NUMBER_OF_RECORDS),
        "disbursement_lag": np.random.randint(1, 6, NUMBER_OF_RECORDS),
        "farm_income": np.random.randint(10000, 300000, NUMBER_OF_RECORDS),
        "loan_diversion": np.random.choice(
            [0, 0.1, 0.2, 0.3], NUMBER_OF_RECORDS, p=[0.7, 0.15, 0.1, 0.05]
        ),
        "interest_rate": np.random.normal(10, 2, NUMBER_OF_RECORDS).clip(5, 20),
        "crop_type": np.random.choice(
            ["Maize", "Rice", "Cassava", "Yam"], NUMBER_OF_RECORDS
        ),
    }

    df = pd.DataFrame(data)

    # Calculate loan repayment based on weighted conditions
    df["loan_repaid"] = (
        (
            df["loan_amount"]
            * (1 - df["loan_diversion"])
            * (df["farm_income"] / df["loan_amount"])
            * np.where(df["disbursement_lag"] <= 3, 1, 0.8)
        )
        .clip(0, df["loan_amount"])
        .astype(int)
    )

    # Binary label for credit worthiness
    df["credit_worthy"] = (df["loan_repaid"] / df["loan_amount"] >= 0.5).astype(int)

    return df


if __name__ == "__main__":
    df = generate_farmer_data()
    print(df.head())
    print("\nCredit Worthiness Distribution:")
    print(df["credit_worthy"].value_counts(normalize=True))
