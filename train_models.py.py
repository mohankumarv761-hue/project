import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import pickle
import os

def train_diabetes_model():

    print("TRAINING DIABETES PREDICTION")
    
    # Load dataset
    df = pd.read_csv('diabetes_dataset.csv')
    print(f"Dataset loaded: {len(df)} samples")
    
    X = df.drop('outcome', axis=1)  
    y = df['outcome']  
    
    print(f"Columns: {list(X.columns)}")
    print(f"Target Output : Non-Diabetic (0): {sum(y==0)}, Diabetic (1): {sum(y==1)}")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"\nTraining samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    
    # Train
    model = SVC(kernel='linear', random_state=42)
    model.fit(X_train_scaled, y_train)
    
    
    # Test
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    
    print("Model Accuracy: ",accuracy)
    
    # Save model and scaler
    os.makedirs('models', exist_ok=True)
    with open('models/diabetes_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('models/diabetes_scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    return model,scaler,accuracy

def train_blood_test_model():
    print("TRAINING BLOOD TEST ANALYSIS MODEL")
    
    # Load dataset
    df = pd.read_csv('blood_test_dataset.csv')
    print(f"Dataset loaded: {len(df)} samples")
    
    X = df.drop('outcome', axis=1)
    y = df['outcome']
    
    print(f"Features: {list(X.columns)}")
    print(f"Target distribution - Normal (0): {sum(y==0)}, Abnormal (1): {sum(y==1)}")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"\nTraining samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
        
    # Train
    model = SVC(kernel='rbf', random_state=42)
    model.fit(X_train_scaled, y_train)
    
    print("SVM Model trained successfully!")
    
    # Test
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    
    print("Model Accuracy: ",accuracy)
    
    # Save model and scaler
    with open('models/blood_test_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('models/blood_test_scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    print("Model saved to 'models/blood_test_model.pkl'")
    print("Scaler saved to 'models/blood_test_scaler.pkl'")
    
    return model, scaler, accuracy

if __name__ == "__main__":
    print("\n HOSPITAL MANAGEMENT SYSTEM - ML MODEL TRAINING \n")
    
    # Train both models
    diabetes_model, diabetes_scaler, diabetes_acc = train_diabetes_model()
    blood_model, blood_scaler, blood_acc = train_blood_test_model()
    

    print("TRAINING COMPLETE!")
    print(f"Diabetes Model Accuracy: ",diabetes_acc)
    print(f"Blood Test Model Accuracy: ",blood_acc)
    print("Models are ready to use in the Flask application!")