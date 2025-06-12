import pandas as pd
import numpy as np
import joblib

MODEL_PATH = "artifacts/model_data.joblib"

# Load the model and its components
model_data = joblib.load(MODEL_PATH)
model = model_data['model']
scaler = model_data['scaler']
features = model_data['features']
cols_to_scale = model_data['cols_to_scale']

# Function to predict risk based on input features
def preprocess_input(age, income, loan_amount, loan_tenure,
                avg_dpd, delinquency_ratio, 
                credit_utilization_ratio, open_loan_accounts, 
                residence_type, loan_purpose, loan_type):
   
    # Create one-hot encoded variables for categorical features
    residence_type_owned = 1 if residence_type == 'Owned' else 0
    residence_type_rented = 1 if residence_type == 'Rented' else 0

    loan_purpose_education = 1 if loan_purpose == 'Education' else 0
    loan_purpose_home = 1 if loan_purpose == 'Home' else 0
    loan_purpose_personal = 1 if loan_purpose == 'Personal' else 0

    loan_type_unsecured = 1 if loan_type == 'Unsecured' else 0

    # Create the input DataFrame with all required columns
    input_data = pd.DataFrame({
        'age': [age],
        'loan_tenure_months': [loan_tenure],
        'number_of_open_accounts': [open_loan_accounts],  # renamed from open_loan_accounts
        'credit_utilization_ratio': [credit_utilization_ratio],
        'loan_to_income': [loan_amount / income if income > 0 else 0],  # renamed from loan_to_income_ratio
        'delinquent_ratio': [delinquency_ratio],  # renamed from delinquency_ratio
        'avg_dpd_per_deliquency': [avg_dpd],  # renamed from avg_dpd
        'residence_type_Owned': [residence_type_owned],
        'residence_type_Rented': [residence_type_rented],
        'loan_purpose_Education': [loan_purpose_education],
        'loan_purpose_Home': [loan_purpose_home],
        'loan_purpose_Personal': [loan_purpose_personal],
        'loan_type_Unsecured': [loan_type_unsecured],

        # Add dummy variables
        'number_of_dependants': [0],
        'years_at_current_address': [0],
        'zipcode': [0],
        'sanction_amount': [0],
        'processing_fee': [0],
        'gst': [0],
        'net_disbursement': [0],
        'principal_outstanding': [0],
        'bank_balance_at_application': [0],
        'number_of_closed_accounts': [0],
        'enquiry_count': [0],

    })

    # Scale the numerical features
    input_data[cols_to_scale] = scaler.transform(input_data[cols_to_scale])
    input_data = input_data[features]  # Ensure the input data has the same columns as the model expects
    
    return input_data

def calculate_credit_score(input_df, base_score=300, scale_length=300):
    x = np.dot(input_df.values, model.coef_.T) + model.intercept_
    
    default_probability = 1 / (1 + np.exp(-x))
    non_default_probability = 1 - default_probability
    
    credit_score = base_score + non_default_probability.flatten() * scale_length
    rating = get_credit_rating(credit_score[0])
    
    return default_probability.flatten()[0] * 100, int(credit_score), rating
# Function to get credit rating based on credit score
    
def get_credit_rating(credit_score):
    if 300 <= credit_score < 500:
        return 'Poor'
    elif 500 <= credit_score < 650:
        return 'Average'
    elif 650 <= credit_score < 750:
        return 'Good'
    elif 750 <= credit_score < 950:
        return 'Excellent'
    else:
        return 'Undefined'

    
# Function to predict risk and return probability, credit score, and rating
def predict_risk(age, income, loan_amount, loan_tenure,
                avg_dpd, delinquency_ratio, 
                credit_utilization_ratio, open_loan_accounts, 
                residence_type, loan_purpose, loan_type):
    
    # Preprocess the input data
    input_data = preprocess_input(age, income, loan_amount, loan_tenure,
                                  avg_dpd, delinquency_ratio, 
                                  credit_utilization_ratio, open_loan_accounts, 
                                  residence_type, loan_purpose, loan_type)
    probability, credit_score, rating = calculate_credit_score(input_data)
    # Return the results
    return probability, credit_score, rating


if __name__ == "__main__":
    # Example usage
    age = 30
    income = 50000
    loan_amount = 100000
    loan_tenure = 12
    avg_dpd = 5
    delinquency_ratio = 0.1
    credit_utilization_ratio = 0.3
    open_loan_accounts = 2
    residence_type = 'Owned'
    loan_purpose = 'Personal'
    loan_type = 'Secured'

    probability, credit_score, rating = predict_risk(age, income, loan_amount, loan_tenure,
                                                     avg_dpd, delinquency_ratio, 
                                                     credit_utilization_ratio, open_loan_accounts, 
                                                     residence_type, loan_purpose, loan_type)
    
    print(f"Default Probability: {probability:.2f}%")
    print(f"Credit Score: {credit_score}")
    print(f"Credit Rating: {rating}")
