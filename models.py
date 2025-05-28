import os
import joblib
import numpy as np
import pandas as pd
import pickle

# ----- Cancer Model Setup -----
MODEL_PATH = os.path.join("cancer_models", "cancer_prediction_model.pkl")
SCALER_PATH = os.path.join("cancer_models", "scaler.pkl")

model_cancer = joblib.load(MODEL_PATH)
scaler_cancer = joblib.load(SCALER_PATH)

def predict_cancer(data):
    """
    Predict cancer diagnosis and return detailed information.
    """
    data_array = np.array([data])
    scaled_data = scaler_cancer.transform(data_array)

    prediction = model_cancer.predict(scaled_data)[0]
    probabilities = model_cancer.predict_proba(scaled_data)[0]  # [neg_prob, pos_prob]
    pos_prob = float(probabilities[1])

    # Determine confidence level
    if pos_prob >= 0.75 or pos_prob <= 0.25:
        confidence = "High"
    elif 0.5 <= pos_prob < 0.75 or 0.25 < pos_prob < 0.5:
        confidence = "Medium"
    else:
        confidence = "Low"

    result = {
        "prediction": int(prediction),
        "probability_negative": float(probabilities[0]),
        "probability_positive": pos_prob,
        "confidence": confidence,
        "status": "Cancer Positive" if prediction == 1 else "Cancer Negative"
    }
    return result


# ----- Genetic Disorder Model Setup -----
model = joblib.load("genetic_disease_rf_model.pkl")
reference_df = pd.read_csv("cleaned_train_data.csv")
expected_columns = reference_df.drop(columns=["Genetic Disorder"]).columns

disorder_labels = {
    0: "Mitochondrial genetic inheritance disorders",
    1: "Multifactorial genetic inheritance disorders",
    2: "Other"
}

def predict_disorder(input_data):
    try:
        essential_input = {
            'Age': int(input_data.get('Age', 0)),
            'Gender': int(input_data.get('Gender', 0)),
            'Blood Cell Count (mcL)': float(input_data.get('Blood Cell Count (mcL)', 0)),
            'White Blood Cell Count (WBC)': float(input_data.get('White Blood Cell Count (WBC)', 0)),
            'Parental Consent': int(input_data.get('Parental Consent', 0)),
            'History of Genetic Disorder': int(input_data.get('History of Genetic Disorder', 0)),
            'Congenital anomalies': int(input_data.get('Congenital anomalies', 0))
        }

        manual_df = pd.DataFrame([{col: 0 for col in expected_columns}])
        for key, value in essential_input.items():
            if key in manual_df.columns:
                manual_df.at[0, key] = value

        prediction = model.predict(manual_df)[0]
        disorder = disorder_labels.get(prediction, "Unknown")

        return {'prediction': int(prediction), 'disorder': disorder}

    except Exception as e:
        return {'error': str(e)}

model_path = os.path.join("heart_failure_models", "heart_failure_log_model.pkl")
scaler_path = os.path.join("heart_failure_models", "heart_failure_scaler.pkl")
selector_path = os.path.join("heart_failure_models", "heart_failure_feature_selector.pkl")

model_heart = joblib.load(model_path)
scaler_heart = joblib.load(scaler_path)
selector_heart = joblib.load(selector_path)

def predict_heart_failure(input_data):
    """
    Predict heart failure (DEATH_EVENT) given raw input data.
    Input: list of 12 features
    Output: 0 or 1
    """
    try:
        input_array = np.array(input_data).reshape(1, -1)
        selected_input = selector_heart.transform(input_array)
        scaled_input = scaler_heart.transform(selected_input)
        prediction = model_heart.predict(scaled_input)
        return int(prediction[0])
    except Exception as e:
        raise ValueError(f"Prediction failed: {str(e)}")



# Define path to the models folder
MODEL_DIR = os.path.join(os.path.dirname(__file__), "diabetes_models")

# Load model components from diabetes_models/
model_diabetes = joblib.load(os.path.join(MODEL_DIR, "diabetes_model.pkl"))
scaler_diabetes = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
selector_diabetes = joblib.load(os.path.join(MODEL_DIR, "selector.pkl"))

def predict_diabetes(data: dict):
    """
    Takes in user data as a dictionary, preprocesses it, and returns prediction details.
    """
    try:
        input_df = pd.DataFrame([data])

        # Ensure data types
        input_df["age"] = input_df["age"].astype(float)
        input_df["bmi"] = input_df["bmi"].astype(float)
        input_df["HbA1c_level"] = input_df["HbA1c_level"].astype(float)
        input_df["blood_glucose_level"] = input_df["blood_glucose_level"].astype(float)
        input_df["hypertension"] = input_df["hypertension"].astype(int)
        input_df["heart_disease"] = input_df["heart_disease"].astype(int)
        input_df["gender"] = input_df["gender"].astype(str)
        input_df["smoking_history"] = input_df["smoking_history"].astype(str)

        selected = selector_diabetes.transform(input_df)
        scaled = scaler_diabetes.transform(selected)

        prediction = model_diabetes.predict(scaled)[0]
        prob = model_diabetes.predict_proba(scaled)[0]

        prob_negative = float(prob[0])
        prob_positive = float(prob[1])

        confidence = "High" if max(prob_positive, prob_negative) > 0.85 else "Medium" if max(prob_positive, prob_negative) > 0.6 else "Low"

        return {
            "prediction": int(prediction),
            "label": "Diabetic" if prediction == 1 else "Not Diabetic",
            "probability_positive": round(prob_positive, 3),
            "probability_negative": round(prob_negative, 3),
            "confidence": confidence
        }

    except Exception as e:
        return {"error": str(e)}


EARLY_MODEL_PATH = os.path.join("early_diabetes_models", "diabetes_model.pkl")
EARLY_SCALER_PATH = os.path.join("early_diabetes_models", "scaler.pkl")

# Load the model and scaler
model_diabetes_early = joblib.load(EARLY_MODEL_PATH)
scaler_diabetes_early = joblib.load(EARLY_SCALER_PATH)

def predict_diabetes_early(data):
    # Create the DataFrame with the incoming data
    new_data = pd.DataFrame([data])

    # Update the column names to match frontend camelCase field names
    columns_map = {
        'suddenWeightLoss': 'sudden weight loss',
        'genitalThrush': 'genital thrush',
        'visualBlurring': 'visual blurring',
        'delayedHealing': 'delayed healing',
        'partialParesis': 'partial paresis',
        'muscleStiffness': 'muscle stiffness'
    }

    # Update the column names dynamically in the DataFrame
    new_data.rename(columns=columns_map, inplace=True)

    # Preprocess the categorical columns: mapping 'Yes'/'No' to 1/0 and 'Male'/'Female' to 1/0
    for col in ['gender', 'polyuria', 'polydipsia', 'sudden weight loss', 'weakness',
                'polyphagia', 'genital thrush', 'visual blurring', 'itching',
                'irritability', 'delayed healing', 'partial paresis',
                'muscle stiffness', 'alopecia', 'obesity']:
        new_data[col] = new_data[col].map({'Yes': 1, 'No': 0, 'Male': 1, 'Female': 0})

    # Feature scaling
    scaled_data = scaler_diabetes_early.transform(new_data)

    # Predict using the model
    prediction = model_diabetes_early.predict(scaled_data)
    prediction_proba = model_diabetes_early.predict_proba(scaled_data)[0]  # Get the first (and only) sample

    # Map prediction to label
    prediction_label = 'Diabetic' if prediction[0] == 1 else 'Not Diabetic'

    # Extract probabilities
    negative_prob = prediction_proba[0]  # Probability of Not Diabetic (class 0)
    positive_prob = prediction_proba[1]  # Probability of Diabetic (class 1)

    # Calculate confidence level (highest of the two)
    confidence = max(positive_prob, negative_prob) * 100

    # Map confidence to a category
    if confidence <= 40:
        confidence_label = 'Low'
    elif confidence <= 70:
        confidence_label = 'Medium'
    else:
        confidence_label = 'High'

    # Return detailed result
    result = {
        'prediction': prediction_label,
        'positive_probability': round(positive_prob * 100, 2),  # as percentage
        'negative_probability': round(negative_prob * 100, 2),  # as percentage
        'confidence_level': confidence_label
    }

    return result


MODEL_PATH_HYPER = os.path.join('hypertension_modells', 'hypertension_model.pkl')
SCALER_PATH_HYPER = os.path.join('hypertension_modells', 'scaler.pkl')

with open(MODEL_PATH_HYPER, 'rb') as f:
    model_hyper = pickle.load(f)

with open(SCALER_PATH_HYPER, 'rb') as f:
    scaler_hyper = pickle.load(f)

# Prediction function
def predict_hypertension(data):
    try:
        input_data = np.array(data).reshape(1, -1)
        input_data_scaled = scaler_hyper.transform(input_data)

        prediction = model_hyper.predict(input_data_scaled)[0]
        probability = model_hyper.predict_proba(input_data_scaled)[0]

        negative_proba = float(probability[0]) * 100
        positive_proba = float(probability[1]) * 100

        # Determine confidence level based on max probability
        max_proba = max(negative_proba, positive_proba)
        if max_proba >= 80:
            confidence = 'High'
        elif max_proba >= 60:
            confidence = 'Medium'
        else:
            confidence = 'Low'

        # Friendly message
        if prediction == 1:
            result_message = 'Positive for Hypertension'
        else:
            result_message = 'Negative for Hypertension'

        return {
            'prediction': int(prediction),
            'result_message': result_message,
            'negative_probability': round(negative_proba, 2),
            'positive_probability': round(positive_proba, 2),
            'confidence_level': confidence
        }

    except Exception as e:
        return {'error': str(e)}



