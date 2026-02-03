"""
Machine Learning Model Training Script
This script trains two simple ML models:
1. Diabetes Prediction Model (SVM)
2. Blood Test Analysis Model (SVM)

Uses beginner-friendly ML concepts:
- StandardScaler: Normalizes data to same scale
- train_test_split: Divides data into training and testing sets
- SVM: Support Vector Machine classifier
- accuracy_score: Measures model performance
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import pickle
import os

def train_diabetes_model():
    """
    Train the diabetes prediction model
    Returns: trained model, scaler, and accuracy score
    """
    print("=" * 50)
    print("TRAINING DIABETES PREDICTION MODEL")
    print("=" * 50)
    
    # Load dataset
    df = pd.read_csv('diabetes_dataset.csv')
    print(f"Dataset loaded: {len(df)} samples")
    
    # Separate features (X) and target (y)
    X = df.drop('outcome', axis=1)  # All columns except outcome
    y = df['outcome']  # The outcome column (0 or 1)
    
    print(f"Features: {list(X.columns)}")
    print(f"Target distribution - Non-Diabetic (0): {sum(y==0)}, Diabetic (1): {sum(y==1)}")
    
    # Split data into training (80%) and testing (20%)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"\nTraining samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")
    
    # Standardize the features (make them same scale)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print("\nData standardized using StandardScaler")
    
    # Train SVM model
    model = SVC(kernel='rbf', random_state=42)
    model.fit(X_train_scaled, y_train)
    
    print("SVM Model trained successfully!")
    
    # Test the model
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nModel Accuracy: {accuracy * 100:.2f}%")
    
    # Save the model and scaler
    os.makedirs('models', exist_ok=True)
    with open('models/diabetes_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('models/diabetes_scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    print("Model saved to 'models/diabetes_model.pkl'")
    print("Scaler saved to 'models/diabetes_scaler.pkl'")
    
    return model, scaler, accuracy

def train_blood_test_model():
    """
    Train the blood test analysis model
    Returns: trained model, scaler, and accuracy score
    """
    print("\n" + "=" * 50)
    print("TRAINING BLOOD TEST ANALYSIS MODEL")
    print("=" * 50)
    
    # Load dataset
    df = pd.read_csv('blood_test_dataset.csv')
    print(f"Dataset loaded: {len(df)} samples")
    
    # Separate features (X) and target (y)
    X = df.drop('outcome', axis=1)
    y = df['outcome']
    
    print(f"Features: {list(X.columns)}")
    print(f"Target distribution - Normal (0): {sum(y==0)}, Abnormal (1): {sum(y==1)}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"\nTraining samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")
    
    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print("\nData standardized using StandardScaler")
    
    # Train SVM model
    model = SVC(kernel='rbf', random_state=42)
    model.fit(X_train_scaled, y_train)
    
    print("SVM Model trained successfully!")
    
    # Test the model
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nModel Accuracy: {accuracy * 100:.2f}%")
    
    # Save the model and scaler
    with open('models/blood_test_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('models/blood_test_scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    print("Model saved to 'models/blood_test_model.pkl'")
    print("Scaler saved to 'models/blood_test_scaler.pkl'")
    
    return model, scaler, accuracy

if __name__ == "__main__":
    print("\n🏥 HOSPITAL MANAGEMENT SYSTEM - ML MODEL TRAINING 🏥\n")
    
    # Train both models
    diabetes_model, diabetes_scaler, diabetes_acc = train_diabetes_model()
    blood_model, blood_scaler, blood_acc = train_blood_test_model()
    
    print("\n" + "=" * 50)
    print("TRAINING COMPLETE!")
    print("=" * 50)
    print(f"Diabetes Model Accuracy: {diabetes_acc * 100:.2f}%")
    print(f"Blood Test Model Accuracy: {blood_acc * 100:.2f}%")
    print("\nModels are ready to use in the Flask application!")
    print("=" * 50)
