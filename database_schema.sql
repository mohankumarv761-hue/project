-- Hospital Management System Database Schema
-- Create Database
CREATE DATABASE IF NOT EXISTS hospital_management;
USE hospital_management;

-- Users Table (Both Patients and Doctors)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(15),
    role ENUM('patient', 'doctor') NOT NULL,
    specialization VARCHAR(100), -- For doctors
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Diagnosis Reports Table
CREATE TABLE IF NOT EXISTS diagnosis_reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT,
    pregnancies INT,
    glucose FLOAT,
    blood_pressure FLOAT,
    skin_thickness FLOAT,
    insulin FLOAT,
    bmi FLOAT,
    diabetes_pedigree_function FLOAT,
    age INT,
    diabetes_prediction VARCHAR(20),
    diabetes_explanation TEXT,
    report_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES users(id),
    FOREIGN KEY (doctor_id) REFERENCES users(id)
);

-- Blood Test Results Table
CREATE TABLE IF NOT EXISTS blood_tests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT,
    hemoglobin FLOAT,
    wbc_count FLOAT,
    rbc_count FLOAT,
    platelets FLOAT,
    cholesterol FLOAT,
    test_result VARCHAR(20),
    test_explanation TEXT,
    test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES users(id),
    FOREIGN KEY (doctor_id) REFERENCES users(id)
);

-- Hospital Departments Table
CREATE TABLE IF NOT EXISTS departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    head_doctor_id INT,
    FOREIGN KEY (head_doctor_id) REFERENCES users(id)
);

-- Insert Sample Data

-- Sample Doctors
INSERT INTO users (username, password, full_name, email, phone, role, specialization) VALUES
('dr.smith', 'doctor123', 'Dr. John Smith', 'john.smith@hospital.com', '1234567890', 'doctor', 'Cardiology'),
('dr.jones', 'doctor123', 'Dr. Sarah Jones', 'sarah.jones@hospital.com', '1234567891', 'doctor', 'Endocrinology'),
('dr.brown', 'doctor123', 'Dr. Michael Brown', 'michael.brown@hospital.com', '1234567892', 'doctor', 'General Medicine');

-- Sample Patients
INSERT INTO users (username, password, full_name, email, phone, role) VALUES
('patient1', 'patient123', 'Alice Johnson', 'alice.j@email.com', '9876543210', 'patient'),
('patient2', 'patient123', 'Bob Williams', 'bob.w@email.com', '9876543211', 'patient'),
('patient3', 'patient123', 'Carol Davis', 'carol.d@email.com', '9876543212', 'patient');

-- Sample Departments
INSERT INTO departments (name, description, head_doctor_id) VALUES
('Cardiology', 'Heart and cardiovascular system care', 1),
('Endocrinology', 'Diabetes and hormone disorders', 2),
('General Medicine', 'Primary healthcare and general illnesses', 3),
('Laboratory', 'Medical testing and diagnostics', NULL),
('Pharmacy', 'Medication dispensing and consultation', NULL);

-- Sample Diagnosis Report
INSERT INTO diagnosis_reports (patient_id, doctor_id, pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree_function, age, diabetes_prediction, diabetes_explanation) VALUES
(4, 2, 2, 120, 80, 25, 85, 28.5, 0.35, 45, 'Non-Diabetic', 'Your glucose levels are within normal range. Continue maintaining a healthy diet and regular exercise routine.');

-- Sample Blood Test
INSERT INTO blood_tests (patient_id, doctor_id, hemoglobin, wbc_count, rbc_count, platelets, cholesterol, test_result, test_explanation) VALUES
(4, 1, 14.5, 7500, 5.2, 250000, 180, 'Normal', 'All blood parameters are within healthy limits. Keep up with regular health checkups every 6 months.');
