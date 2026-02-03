"""
Hospital Management System - Flask Backend
Main application file with REST APIs for:
- Authentication (Login)
- Patient Dashboard
- Doctor Dashboard
- Diagnosis Prediction
- Blood Test Analysis
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
from mysql.connector import Error
import pickle
import numpy as np
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'hospital_secret_key_2024'  # Change this in production

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Change to your MySQL username
    'password': 'Mohan@2006',  # Change to your MySQL password
    'database': 'hospital_management'
}

# Load ML Models
try:
    with open('models/diabetes_model.pkl', 'rb') as f:
        diabetes_model = pickle.load(f)
    with open('models/diabetes_scaler.pkl', 'rb') as f:
        diabetes_scaler = pickle.load(f)
    with open('models/blood_test_model.pkl', 'rb') as f:
        blood_test_model = pickle.load(f)
    with open('models/blood_test_scaler.pkl', 'rb') as f:
        blood_test_scaler = pickle.load(f)
    print("✓ ML Models loaded successfully")
except Exception as e:
    print(f"⚠ Warning: ML Models not found. Please run train_models.py first!")
    print(f"Error: {e}")

# Database connection helper
def get_db_connection():
    """Create and return database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None

# Generate explanations for predictions
def get_diabetes_explanation(prediction, glucose, bmi, age):
    """Generate patient-friendly explanation for diabetes prediction"""
    if prediction == 1:  # Diabetic
        line1 = "Your test results suggest elevated diabetes risk factors that need medical attention."
        line2 = "Please schedule a consultation with an endocrinologist for proper diagnosis and treatment plan."
    else:  # Non-Diabetic
        if glucose > 125 or bmi > 30:
            line1 = "Your glucose levels are within acceptable range, but some parameters need monitoring."
            line2 = "Maintain a balanced diet, exercise regularly, and get checkups every 6 months."
        else:
            line1 = "Your test results show healthy glucose metabolism and low diabetes risk."
            line2 = "Continue your current lifestyle with regular exercise and healthy eating habits."
    
    return f"{line1} {line2}"

def get_blood_test_explanation(prediction, hemoglobin, wbc, cholesterol):
    """Generate patient-friendly explanation for blood test results"""
    if prediction == 1:  # Abnormal
        line1 = "Some blood parameters are outside the normal range and require medical review."
        line2 = "Consult your doctor to discuss these results and potential treatment or lifestyle changes."
    else:  # Normal
        if cholesterol > 200:
            line1 = "Most blood values are normal, but cholesterol levels should be monitored closely."
            line2 = "Focus on heart-healthy diet and regular physical activity to maintain good health."
        else:
            line1 = "All your blood test parameters are within healthy limits, indicating good overall health."
            line2 = "Keep up with regular health checkups every 6-12 months to maintain wellness."
    
    return f"{line1} {line2}"

# Routes

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and authentication"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            cursor.close()
            connection.close()
            
            if user:
                # Store user info in session
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['role'] = user['role']
                session['full_name'] = user['full_name']
                
                # Redirect based on role
                if user['role'] == 'doctor':
                    return redirect(url_for('doctor_dashboard'))
                else:
                    return redirect(url_for('patient_dashboard'))
            else:
                return render_template('login.html', error="Invalid username or password")
        else:
            return render_template('login.html', error="Database connection error")
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/facilities')
def facilities():
    """Hospital facilities page"""
    connection = get_db_connection()
    departments = []
    doctors = []
    
    if connection:
        cursor = connection.cursor(dictionary=True)
        
        # Get departments
        cursor.execute("SELECT * FROM departments")
        departments = cursor.fetchall()
        
        # Get all doctors
        cursor.execute("SELECT * FROM users WHERE role = 'doctor'")
        doctors = cursor.fetchall()
        
        cursor.close()
        connection.close()
    
    return render_template('facilities.html', departments=departments, doctors=doctors)

@app.route('/patient/dashboard')
def patient_dashboard():
    """Patient dashboard - view own reports"""
    if 'user_id' not in session or session['role'] != 'patient':
        return redirect(url_for('login'))
    
    connection = get_db_connection()
    diagnosis_reports = []
    blood_tests = []
    
    if connection:
        cursor = connection.cursor(dictionary=True)
        
        # Get diagnosis reports
        query = """
            SELECT dr.*, u.full_name as doctor_name 
            FROM diagnosis_reports dr
            LEFT JOIN users u ON dr.doctor_id = u.id
            WHERE dr.patient_id = %s
            ORDER BY dr.report_date DESC
        """
        cursor.execute(query, (session['user_id'],))
        diagnosis_reports = cursor.fetchall()
        
        # Get blood test reports
        query = """
            SELECT bt.*, u.full_name as doctor_name 
            FROM blood_tests bt
            LEFT JOIN users u ON bt.doctor_id = u.id
            WHERE bt.patient_id = %s
            ORDER BY bt.test_date DESC
        """
        cursor.execute(query, (session['user_id'],))
        blood_tests = cursor.fetchall()
        
        cursor.close()
        connection.close()
    
    return render_template('patient_dashboard.html', 
                         diagnosis_reports=diagnosis_reports,
                         blood_tests=blood_tests)

@app.route('/doctor/dashboard')
def doctor_dashboard():
    """Doctor dashboard - view assigned patients"""
    if 'user_id' not in session or session['role'] != 'doctor':
        return redirect(url_for('login'))
    
    connection = get_db_connection()
    patients = []
    my_reports = []
    
    if connection:
        cursor = connection.cursor(dictionary=True)
        
        # Get all patients
        cursor.execute("SELECT * FROM users WHERE role = 'patient'")
        patients = cursor.fetchall()
        
        # Get reports created by this doctor
        query = """
            SELECT dr.*, u.full_name as patient_name 
            FROM diagnosis_reports dr
            JOIN users u ON dr.patient_id = u.id
            WHERE dr.doctor_id = %s
            ORDER BY dr.report_date DESC
            LIMIT 10
        """
        cursor.execute(query, (session['user_id'],))
        my_reports = cursor.fetchall()
        
        cursor.close()
        connection.close()
    
    return render_template('doctor_dashboard.html', 
                         patients=patients,
                         my_reports=my_reports)

@app.route('/doctor/diagnosis', methods=['GET', 'POST'])
def doctor_diagnosis():
    """Doctor creates diagnosis for patient"""
    if 'user_id' not in session or session['role'] != 'doctor':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Get form data
        patient_id = request.form['patient_id']
        pregnancies = float(request.form['pregnancies'])
        glucose = float(request.form['glucose'])
        blood_pressure = float(request.form['blood_pressure'])
        skin_thickness = float(request.form['skin_thickness'])
        insulin = float(request.form['insulin'])
        bmi = float(request.form['bmi'])
        dpf = float(request.form['dpf'])
        age = float(request.form['age'])
        
        # Prepare data for prediction
        input_data = np.array([[pregnancies, glucose, blood_pressure, skin_thickness, 
                               insulin, bmi, dpf, age]])
        input_scaled = diabetes_scaler.transform(input_data)
        
        # Make prediction
        prediction = diabetes_model.predict(input_scaled)[0]
        result = "Diabetic" if prediction == 1 else "Non-Diabetic"
        
        # Generate explanation
        explanation = get_diabetes_explanation(prediction, glucose, bmi, age)
        
        # Save to database
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            query = """
                INSERT INTO diagnosis_reports 
                (patient_id, doctor_id, pregnancies, glucose, blood_pressure, 
                 skin_thickness, insulin, bmi, diabetes_pedigree_function, age,
                 diabetes_prediction, diabetes_explanation)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (patient_id, session['user_id'], pregnancies, glucose, 
                                 blood_pressure, skin_thickness, insulin, bmi, dpf, age,
                                 result, explanation))
            connection.commit()
            cursor.close()
            connection.close()
        
        return render_template('diagnosis_result.html', 
                             result=result, 
                             explanation=explanation,
                             test_type='Diabetes')
    
    # GET request - show form
    connection = get_db_connection()
    patients = []
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, full_name FROM users WHERE role = 'patient'")
        patients = cursor.fetchall()
        cursor.close()
        connection.close()
    
    return render_template('diagnosis_form.html', patients=patients)

@app.route('/doctor/blood_test', methods=['GET', 'POST'])
def doctor_blood_test():
    """Doctor creates blood test analysis for patient"""
    if 'user_id' not in session or session['role'] != 'doctor':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Get form data
        patient_id = request.form['patient_id']
        hemoglobin = float(request.form['hemoglobin'])
        wbc_count = float(request.form['wbc_count'])
        rbc_count = float(request.form['rbc_count'])
        platelets = float(request.form['platelets'])
        cholesterol = float(request.form['cholesterol'])
        
        # Prepare data for prediction
        input_data = np.array([[hemoglobin, wbc_count, rbc_count, platelets, cholesterol]])
        input_scaled = blood_test_scaler.transform(input_data)
        
        # Make prediction
        prediction = blood_test_model.predict(input_scaled)[0]
        result = "Abnormal" if prediction == 1 else "Normal"
        
        # Generate explanation
        explanation = get_blood_test_explanation(prediction, hemoglobin, wbc_count, cholesterol)
        
        # Save to database
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            query = """
                INSERT INTO blood_tests 
                (patient_id, doctor_id, hemoglobin, wbc_count, rbc_count, 
                 platelets, cholesterol, test_result, test_explanation)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (patient_id, session['user_id'], hemoglobin, wbc_count,
                                 rbc_count, platelets, cholesterol, result, explanation))
            connection.commit()
            cursor.close()
            connection.close()
        
        return render_template('diagnosis_result.html', 
                             result=result, 
                             explanation=explanation,
                             test_type='Blood Test')
    
    # GET request - show form
    connection = get_db_connection()
    patients = []
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, full_name FROM users WHERE role = 'patient'")
        patients = cursor.fetchall()
        cursor.close()
        connection.close()
    
    return render_template('blood_test_form.html', patients=patients)

if __name__ == '__main__':
    print("\n🏥 Hospital Management System Starting... 🏥")
    print("=" * 50)
    print("Make sure to:")
    print("1. Create MySQL database using database_schema.sql")
    print("2. Train ML models using: python train_models.py")
    print("3. Update DB_CONFIG with your MySQL credentials")
    print("=" * 50)
    app.run(debug=True, port=5000)
