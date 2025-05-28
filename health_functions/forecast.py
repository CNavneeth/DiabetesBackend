def check_health_risks(glucose, blood_pressure, cholesterol, bmi, age):
    risks = {}

    # Glucose checks
    if glucose > 180:
        risks["High Blood Sugar Risk"] = "High chance of diabetes complications"
    elif glucose < 70:
        risks["Low Blood Sugar Risk"] = "Risk of hypoglycemia"
    elif glucose < 50:
        risks["Critical Low Blood Sugar"] = "Immediate medical attention required"
    elif glucose > 125:
        risks["Prediabetes Risk"] = "Pre-diabetic condition, lifestyle changes needed"

    # Blood Pressure checks
    if blood_pressure > 180:
        risks["Hypertensive Crisis"] = "Requires immediate medical attention"
    elif blood_pressure > 140:
        risks["Hypertension"] = "Risk of heart diseases"
    elif blood_pressure < 60:
        risks["Low Blood Pressure"] = "Risk of dizziness and fatigue"
    elif blood_pressure < 30:
        risks["Critical Low Blood Pressure"] = "Can be life-threatening"
    elif blood_pressure > 120:
        risks["Prehypertension"] = "Risk of developing hypertension, monitor regularly"

    # Cholesterol checks
    if cholesterol > 240:
        risks["Very High Cholesterol"] = "Very high risk for heart disease and stroke"
    elif cholesterol > 200:
        risks["High Cholesterol"] = "Risk of cardiovascular diseases"
    elif cholesterol < 50:
        risks["Low Cholesterol"] = "Possible malnutrition or liver problems"
    elif cholesterol < 150:
        risks["Very Low Cholesterol"] = "Associated with certain types of cancer"

    # BMI checks
    if bmi < 18.5:
        risks["Underweight"] = "Risk of malnutrition and weakened immune system"
    elif 18.5 <= bmi <= 24.9:
        risks["Normal Weight"] = "Healthy weight range"
    elif 25 <= bmi <= 29.9:
        risks["Overweight"] = "Increased risk of heart disease, type 2 diabetes"
    elif 30 <= bmi <= 34.9:
        risks["Obesity (Class 1)"] = "Higher risk of heart disease, stroke, type 2 diabetes"
    elif 35 <= bmi <= 39.9:
        risks["Obesity (Class 2)"] = "Severe risk of heart disease, stroke, diabetes, sleep apnea"
    elif bmi >= 40:
        risks["Obesity (Class 3)"] = "Extremely high risk for heart disease, stroke, type 2 diabetes"

    # Age-related risks
    if age < 18:
        risks["Age Risk"] = "Child or adolescent: consult pediatrician for proper care"
    elif age >= 60:
        risks["Senior Age Risk"] = "Increased risk of chronic conditions, monitor health regularly"

    # Additional Risk Factors
    if glucose > 140 and cholesterol > 240:
        risks["Metabolic Syndrome"] = "Combination of high blood sugar, high cholesterol, and hypertension, increased risk of heart disease"
    if blood_pressure > 180 and glucose > 200:
        risks["Hypertensive Diabetes Risk"] = "High risk of complications due to hypertension and uncontrolled diabetes"

    # Debug log
    print("Final Risk Assessment:", risks)

    return risks if risks else {"Message": "No significant risks detected."}