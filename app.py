import pickle as pkl
import os
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import database
import healthrecord
import models
import health_functions.forecast
from health_functions.insights import get_insights_data
import actionplan
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Load scaler and model
script_dir = os.path.dirname(os.path.abspath(__file__))
scaler_path = os.path.join(script_dir, 'scaler.pkl')
scaler = pkl.load(open(scaler_path, 'rb'))

file_path = os.path.join(script_dir, 'nb.pkl')
with open(file_path, 'rb') as f:
    model = pkl.load(f)


# Define health risks function

@app.route("/predict-diabetes", methods=["POST"])
def predict_diabetes_route():
    try:
        input_data = request.get_json()
        if not input_data:
            return jsonify({"error": "No input data provided"}), 400

        result = models.predict_diabetes(input_data)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Prediction function
def predict(Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, Bmi, Dpf, Age):
    input_data = pd.DataFrame([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, Bmi, Dpf, Age]])
    input_data = scaler.transform(input_data)
    prediction = model.predict(input_data)

    # Get health risks
    health_risks = health_functions.forecast.check_health_risks(Glucose, BloodPressure)

    if prediction == 1:
        result = {
            
            'prediction': health_risks,
            'gif_url': "https://media1.tenor.com/m/DhY-eiVMAZgAAAAd/chi-wow-nice-chii.gif",
            'health_risks': health_risks  # Include risks dictionary
        }
    else:
        result = {
            'prediction': "You have low chances of Diabetes. Please maintain a healthy lifestyle.",
            'gif_url': "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExd2txb242N3pkMmp0ODRiangydm9raDY5OHBhYmw1Y2NobjM0cGZtNSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/W1GG6RYUcWxoHl3jV9/giphy.gif",
            'health_risks': health_risks  # Include risks dictionary
        }

    return result

@app.route('/predict', methods=['POST'])
def predictions():
    if request.method == 'POST':
        data = request.get_json()
        Age = data.get('Age')
        Pregnancies = data.get('Pregnancies')
        Glucose = data.get('Glucose')
        BloodPressure = data.get('BloodPressure')
        Insulin = data.get('Insulin')
        Bmi = data.get('BMI')
        SkinThickness = data.get('SkinThickness')
        Dpf = data.get('DPF')
        
        result = predict(Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, Bmi, Dpf, Age)
        return jsonify(result)
    
    return "Invalid request method"

# Educational Resources API
@app.route('/api/insights', methods=['GET'])
def get_insights():
    return jsonify(get_insights_data())

# Forecast API endpoint
@app.route('/forecast', methods=['POST'])
def forecast():
    try:
        data = request.get_json()
        print("Received Data:", data)  # Debugging
        
        # Ensure data extraction is correct
        glucose = float(data.get('Glucose', 0))
        blood_pressure = float(data.get('BloodPressure', 0))
        cholesterol = float(data.get('Cholesterol', 0))
        bmi = float(data.get('BMI', 0))  # Extract BMI from the request data
        age = int(data.get('Age', 0))  # Extract Age from the request data

        print(f"Parsed values -> Glucose: {glucose}, Blood Pressure: {blood_pressure}, Cholesterol: {cholesterol}, BMI: {bmi}, Age: {age}")

        # Run your prediction logic (you might update this to include BMI and Age in your logic)
        risks = health_functions.forecast.check_health_risks(glucose, blood_pressure, cholesterol, bmi, age)

        print("Computed Risks:", risks)  # Debugging
        return jsonify({'risks': risks})

    except Exception as e:
        print("Error in Forecast API:", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/get_patients', methods=['GET'])
def get_patients():
    try:
        patients = database.get_all_patients()
        return jsonify({"patients": patients})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/create_account', methods=['POST'])
def create_account():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        date_of_birth = data.get('date_of_birth')
        email = data.get('email')
        if not username or not password or not date_of_birth:
            return jsonify({"error": "All fields are required"}), 400

        result = database.create_user(username, password, date_of_birth,email)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required!"}), 400

    auth_response = database.authenticate_user(username, password)

    if "error" in auth_response:
        return jsonify(auth_response), 401

    return jsonify(auth_response), 200

@app.route("/get-profile/<user_id>", methods=["GET"])
def get_profile(user_id):
    """Fetch user profile data."""
    user = database.get_user_profile(user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route("/upload-profile-pic", methods=["POST"])
def upload_profile_pic():
    """Upload and update user profile picture."""
    user_id = request.form.get("user_id")
    image_file = request.files.get("profile_pic")

    if not user_id or not image_file:
        return jsonify({"error": "User ID and image file are required"}), 400

    message = database.update_profile_pic(user_id, image_file)
    return jsonify({"message": message})

@app.route("/update-profile", methods=["PUT"])
def update_profile():
    user_id = request.form.get("user_id")
    username = request.form.get("username")
    dob = request.form.get("dob")
    email = request.form.get("email")  # Get email
    profile_pic = request.files.get("profile_pic")  # Get image file

    if not user_id or not username or not dob or not email:
        return jsonify({"error": "Missing required fields"}), 400

    result = database.update_user_profile(user_id, username, dob, email, profile_pic)
    
    if result:
        return jsonify({"message": "Profile updated successfully!"})
    else:
        return jsonify({"error": "Failed to update profile"}), 500
    
@app.route("/add_record", methods=["POST"])
def add_record():
    data = request.json  # Get data from frontend
    response = healthrecord.add_health_record(data)
    return jsonify(response)

@app.route("/add_cancer_record", methods=["POST"])
def add_cancer_record():
    data = request.json  # Get data from frontend
    response = healthrecord.add_cancer_record(data)
    return jsonify(response)

@app.route("/add_heart_record", methods=["POST"])
def add_heart_record():
    data = request.json  # Get data from frontend
    response = healthrecord.add_heart_record(data)
    return jsonify(response)

@app.route("/get_records/<user_id>", methods=["GET"])
def fetch_records(user_id):
    response = healthrecord.get_user_records(user_id)
    return jsonify(response)

@app.route("/get_cancer_records/<user_id>", methods=["GET"])
def fetch_cancer_records(user_id):
    response = healthrecord.get_cancer_records(user_id)
    return jsonify(response)

@app.route("/get_heart_records/<user_id>", methods=["GET"])
def fetch_heart_records(user_id):
    response = healthrecord.get_heart_records(user_id)
    return jsonify(response)

@app.route("/delete_record/<record_id>", methods=["DELETE"])
def delete_record(record_id):
    print(f"Received delete request for ID: {record_id}")  # Debugging log
    response = healthrecord.delete_user_record(record_id)
    return jsonify(response)

@app.route("/delete_cancer_record/<record_id>", methods=["DELETE"])
def delete_cancer_record(record_id):
    print(f"Received delete request for ID: {record_id}")  # Debugging log
    response = healthrecord.delete_cancer_record(record_id)
    return jsonify(response)

@app.route("/delete_heart_record/<record_id>", methods=["DELETE"])
def delete_heart_record(record_id):
    print(f"Received delete request for ID: {record_id}")  # Debugging log
    response = healthrecord.delete_heart_record(record_id)
    return jsonify(response)

@app.route("/predictdisorder", methods=["POST"])
def disorder_route():
    input_data = request.json
    result = models.predict_disorder(input_data)
    return jsonify(result)

@app.route('/predict_cancer', methods=['POST'])
def cancer_route():
    try:
        data = request.json['data']
        result = models.predict_cancer(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict_heart', methods=['POST'])
def heart_route():
    try:
        data = request.get_json()
        input_data = data.get('input_data')

        if not input_data or len(input_data) != 12:
            return jsonify({"error": "Invalid input data. Exactly 12 features required."}), 400

        prediction = models.predict_heart_failure(input_data)
        return jsonify({"prediction": prediction})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/predictearlydiabetes', methods=['POST'])
def predict():
    # Extract the data from the incoming JSON request
    data = request.json
    
    # Call the controller function to get the prediction result
    result = models.predict_diabetes_early(data)
    
    # Return the result as a JSON response
    return jsonify(result)
@app.route("/save_action_plan", methods=["POST"])
def save_action_plan():
    try:
        data = request.json  # Get data from frontend
        print("Received data:", data)  # Log the received data
        user_id = data.get("user_id")
        plan = data.get("plan")

        # Now pass the data to the function to save it
        response = actionplan.add_action_plan(user_id, plan)
        return jsonify(response)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "message": "An error occurred"}), 500

@app.route("/get_action_plans", methods=["GET"])
def fetch_action_plans():
    # Get user_id from query parameters
    user_id = request.args.get("user_id")
    
    if not user_id:
        return jsonify({"success": False, "message": "User ID is required"}), 400

    # Call the function to get action plans
    response = actionplan.get_action_plans(user_id)

    if response["success"]:
        return jsonify(response), 200
    else:
        return jsonify(response), 500
    
@app.route('/delete-plans', methods=['DELETE'])
def delete_plans():
    # Get the user ID from the request (ensure that the user is authenticated)
    user_id = request.json.get('user_id')

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
    
    # Call a function to delete the plans for this user
    result = actionplan.delete_plans_for_user(user_id)

    if result:
        return jsonify({"message": "All plans deleted successfully"}), 200
    else:
        return jsonify({"error": "Error deleting plans"}), 500

@app.route('/predict_hypertension', methods=['POST'])
def predicthyper():
    data = request.get_json()

    # Validate data
    expected_fields = ['male', 'age', 'currentSmoker', 'cigsPerDay', 'BPMeds', 'diabetes',
                       'totChol', 'sysBP', 'diaBP', 'BMI', 'heartRate', 'glucose']
    input_data = [data.get(field) for field in expected_fields]

    # Check for missing fields
    if None in input_data:
        return jsonify({'error': 'Missing fields or incorrect data format'}), 400

    # Get prediction
    result = models.predict_hypertension(input_data)
    return jsonify(result)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
