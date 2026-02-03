# Hospital Management System 🏥

A complete web-based Hospital Management System with AI-powered diagnosis using Machine Learning.

## 🌟 Features

### Authentication System
- **Two-role login system**: Patient and Doctor
- Secure username/password authentication
- Role-based dashboards
- Session management

### Patient Features
- Login and view personal medical reports
- Access diabetes screening results
- View blood test reports online


### Doctor Features
- View all assigned patients
- Create diabetes screening reports
- Upload and analyze blood test results
- AI-powered diagnosis prediction
- Patient management dashboard

### Hospital Features
- Hospital departments information
- Doctor directory with specializations
- Laboratory services
- Pharmacy information

### AI/ML Diagnosis Module
- **Diabetes Prediction**:
  - Input: Pregnancies, Glucose, Blood Pressure, Skin Thickness, Insulin, BMI, Diabetes Pedigree Function, Age
  - Output: Diabetic / Non-Diabetic with explanation
  
- **Blood Test Analysis**:
  - Input: Hemoglobin, WBC Count, RBC Count, Platelets, Cholesterol
  - Output: Normal / Abnormal with explanation

### Machine Learning
- Uses **Support Vector Machine (SVM)**
- **StandardScaler** for data normalization
- **train_test_split** for model validation
- **accuracy_score** for performance measurement
- Trained on real medical datasets

## 📂 Project Structure

```
hospital_system/
│
├── app.py                          # Main Flask application
├── train_models.py                 # ML model training script
├── database_schema.sql             # MySQL database schema
│
├── templates/                      # HTML templates
│   ├── base.html                  # Base template
│   ├── index.html                 # Home page
│   ├── login.html                 # Login page
│   ├── facilities.html            # Hospital facilities
│   ├── patient_dashboard.html     # Patient dashboard
│   ├── doctor_dashboard.html      # Doctor dashboard
│   ├── diagnosis_form.html        # Diabetes screening form
│   ├── blood_test_form.html       # Blood test form
│   └── diagnosis_result.html      # Result display
│
├── static/
│   └── css/
│       └── style.css              # Main stylesheet
│
├── models/                         # Trained ML models (generated)
│   ├── diabetes_model.pkl
│   ├── diabetes_scaler.pkl
│   ├── blood_test_model.pkl
│   └── blood_test_scaler.pkl
│
└── data/                          # Training datasets
    ├── diabetes_dataset.csv
    └── blood_test_dataset.csv
```

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript (for interactive elements)

### Backend
- Python 3.x
- Flask (Web framework)
- REST APIs

### Database
- MySQL

### Machine Learning
- scikit-learn (sklearn)
- pandas (data handling)
- numpy (numerical operations)
- pickle (model serialization)

## 📋 Prerequisites

Before running this project, ensure you have:

1. **Python 3.7+** installed
2. **MySQL Server** installed and running
3. **pip** (Python package manager)

## 🚀 Installation & Setup

### Step 1: Install Required Python Packages

```bash
pip install flask mysql-connector-python scikit-learn pandas numpy pickle5
```

### Step 2: Setup MySQL Database

1. Open MySQL command line or MySQL Workbench
2. Run the database schema:

```bash
mysql -u root -p < database_schema.sql
```

Or manually:
- Open `database_schema.sql`
- Copy and execute all SQL commands in MySQL

3. Update database credentials in `app.py`:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_mysql_username',    # Change this
    'password': 'your_mysql_password', # Change this
    'database': 'hospital_management'
}
```

### Step 3: Train Machine Learning Models

```bash
python train_models.py
```

This will:
- Load training datasets
- Train diabetes prediction model
- Train blood test analysis model
- Save models to `models/` directory
- Display accuracy scores

Expected output:
```
🏥 HOSPITAL MANAGEMENT SYSTEM - ML MODEL TRAINING 🏥

==================================================
TRAINING DIABETES PREDICTION MODEL
==================================================
Dataset loaded: 100 samples
...
Model Accuracy: 75-80%

==================================================
TRAINING BLOOD TEST ANALYSIS MODEL
==================================================
Dataset loaded: 95 samples
...
Model Accuracy: 95-100%
```

### Step 4: Run the Application

```bash
python app.py
```

The server will start on `http://127.0.0.1:5000/`

## 👥 Demo Credentials

### Patient Login
- **Username**: `patient1`
- **Password**: `patient123`

### Doctor Login
- **Username**: `dr.smith`
- **Password**: `doctor123`

Additional accounts:
- Patients: patient2, patient3 (password: patient123)
- Doctors: dr.jones, dr.brown (password: doctor123)

## 📊 Database Schema

### Tables

1. **users** - Stores both patients and doctors
   - id, username, password, full_name, email, phone, role, specialization

2. **diagnosis_reports** - Diabetes screening results
   - patient_id, doctor_id, pregnancies, glucose, blood_pressure, etc.

3. **blood_tests** - Blood test results
   - patient_id, doctor_id, hemoglobin, wbc_count, rbc_count, platelets, cholesterol

4. **departments** - Hospital departments
   - name, description, head_doctor_id

## 🤖 Machine Learning Workflow

### 1. Data Preparation
```python
# Load dataset
df = pd.read_csv('data/diabetes_dataset.csv')

# Separate features and target
X = df.drop('outcome', axis=1)  # Features
y = df['outcome']                # Target (0 or 1)
```

### 2. Data Splitting
```python
# Split into training (80%) and testing (20%)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

### 3. Feature Scaling
```python
# Normalize features to same scale
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

### 4. Model Training
```python
# Train SVM model
model = SVC(kernel='rbf', random_state=42)
model.fit(X_train_scaled, y_train)
```

### 5. Prediction
```python
# Make predictions
y_pred = model.predict(X_test_scaled)

# Measure accuracy
accuracy = accuracy_score(y_test, y_pred)
```

### 6. Saving Models
```python
# Save for later use
with open('models/diabetes_model.pkl', 'wb') as f:
    pickle.dump(model, f)
```

## 🎯 How It Works

### Patient Flow
1. Login with patient credentials
2. View dashboard
3. See diabetes screening reports
4. Check blood test results
5. Read AI-generated explanations

### Doctor Flow
1. Login with doctor credentials
2. View all patients
3. Select patient
4. Create diagnosis (diabetes or blood test)
5. Enter clinical parameters
6. AI generates prediction
7. System saves report with explanation
8. Patient can view in their dashboard

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page |
| `/login` | GET, POST | Login page |
| `/logout` | GET | Logout |
| `/facilities` | GET | Hospital facilities |
| `/patient/dashboard` | GET | Patient dashboard |
| `/doctor/dashboard` | GET | Doctor dashboard |
| `/doctor/diagnosis` | GET, POST | Create diabetes screening |
| `/doctor/blood_test` | GET, POST | Create blood test |

## 🔒 Security Features

- Session-based authentication
- Role-based access control
- Password protection (Note: In production, use password hashing!)
- SQL injection prevention using parameterized queries

## 📈 Model Performance

### Diabetes Prediction Model
- Algorithm: Support Vector Machine (SVM)
- Kernel: RBF (Radial Basis Function)
- Expected Accuracy: 75-80%
- Training Samples: 100

### Blood Test Analysis Model
- Algorithm: Support Vector Machine (SVM)
- Kernel: RBF
- Expected Accuracy: 95-100%
- Training Samples: 95

## 🎨 Design Features

- Clean, modern UI
- Responsive design (mobile-friendly)
- Color-coded results (green for normal, red for abnormal)
- Easy-to-read patient explanations
- Professional medical interface

## 📱 Responsive Design

The system is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones

## 🚨 Important Notes

### For Production Use:
1. **Security**: Implement proper password hashing (bcrypt, pbkdf2)
2. **HTTPS**: Use SSL/TLS certificates
3. **Environment Variables**: Store sensitive data securely
4. **Input Validation**: Add comprehensive validation
5. **Rate Limiting**: Prevent abuse
6. **Logging**: Implement proper logging
7. **Backup**: Regular database backups
8. **HIPAA Compliance**: If handling real medical data

### Disclaimer
This is an educational project. The AI predictions are for demonstration purposes only and should not be used for actual medical diagnosis. Always consult qualified healthcare professionals for medical advice.

## 🐛 Troubleshooting

### Common Issues:

**1. Database Connection Error**
```
Solution: Check MySQL is running and credentials are correct
```

**2. Model Not Found Error**
```
Solution: Run python train_models.py first
```

**3. Port Already in Use**
```
Solution: Change port in app.py: app.run(debug=True, port=5001)
```

**4. Module Not Found**
```
Solution: Install missing packages: pip install [package-name]
```

## 📚 Learning Resources

### ML Concepts Used:
- **StandardScaler**: Normalizes features to mean=0, std=1
- **train_test_split**: Divides data for training/testing
- **SVM**: Creates decision boundary to classify data
- **accuracy_score**: Percentage of correct predictions

### Further Reading:
- Flask Documentation: https://flask.palletsprojects.com/
- scikit-learn: https://scikit-learn.org/
- MySQL: https://dev.mysql.com/doc/

## 👨‍💻 Developer Notes

### Code Structure:
- **Modular Design**: Separate concerns (models, views, controllers)
- **Well Commented**: Easy to understand
- **Beginner Friendly**: Simple ML concepts
- **Scalable**: Easy to add new features

### Future Enhancements:
- Password hashing and security
- Email notifications
- Appointment scheduling
- Prescription management
- Multi-language support
- Advanced analytics dashboard
- Mobile app
- Telemedicine integration

## 📄 License

This project is for educational purposes. Feel free to use and modify.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## 📞 Support

For issues or questions, please refer to the code comments or create an issue.

---

**Made with ❤️ for learning and education**
