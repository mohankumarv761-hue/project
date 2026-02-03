# Quick Setup Guide 🚀

## For Complete Beginners

### Prerequisites Check
Before starting, make sure you have:
- [ ] Python 3.7 or higher installed
- [ ] MySQL Server installed
- [ ] Basic knowledge of command line

### Installation Steps (Windows)

#### 1. Install Python Packages
Open Command Prompt and navigate to project folder:
```bash
cd path\to\hospital_system
pip install -r requirements.txt
```

#### 2. Setup MySQL Database

**Option A: Using MySQL Workbench (GUI)**
1. Open MySQL Workbench
2. Connect to your local server
3. Go to File → Open SQL Script
4. Select `database_schema.sql`
5. Click Execute (⚡ icon)

**Option B: Using Command Line**
```bash
mysql -u root -p
# Enter your MySQL password
```

Then paste the contents of `database_schema.sql` or:
```bash
mysql -u root -p < database_schema.sql
```

#### 3. Configure Database Connection
Open `app.py` and update these lines (around line 20):
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',              # Your MySQL username
    'password': 'your_password', # Your MySQL password
    'database': 'hospital_management'
}
```

#### 4. Train ML Models
```bash
python train_models.py
```

Expected output:
```
🏥 HOSPITAL MANAGEMENT SYSTEM - ML MODEL TRAINING 🏥
...
Diabetes Model Accuracy: 75-80%
Blood Test Model Accuracy: 95-100%
```

#### 5. Run the Application
```bash
python app.py
```

You should see:
```
🏥 Hospital Management System Starting... 🏥
...
* Running on http://127.0.0.1:5000
```

#### 6. Open in Browser
Go to: http://127.0.0.1:5000

---

### Installation Steps (Mac/Linux)

#### 1. Install Python Packages
```bash
cd path/to/hospital_system
pip3 install -r requirements.txt
```

#### 2. Setup MySQL
```bash
mysql -u root -p < database_schema.sql
```

#### 3. Configure Database
Edit `app.py`:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'hospital_management'
}
```

#### 4. Train Models
```bash
python3 train_models.py
```

#### 5. Run Application
```bash
python3 app.py
```

---

## Testing the System

### 1. Test Patient Login
- Go to http://127.0.0.1:5000
- Click "Patient Login"
- Username: `patient1`
- Password: `patient123`
- You should see your dashboard with reports

### 2. Test Doctor Login
- Logout
- Login with:
  - Username: `dr.smith`
  - Password: `doctor123`
- You should see doctor dashboard
- Try creating a new diagnosis

---

## Troubleshooting

### Problem: "Module not found"
**Solution**: Install missing package
```bash
pip install [package-name]
```

### Problem: "Can't connect to MySQL server"
**Solution**: 
1. Check if MySQL is running
2. Verify username/password in `app.py`
3. Check if database exists:
```bash
mysql -u root -p
SHOW DATABASES;
```

### Problem: "ML models not found"
**Solution**: Run training script
```bash
python train_models.py
```

### Problem: "Port 5000 already in use"
**Solution**: Change port in `app.py`:
```python
app.run(debug=True, port=5001)  # Use 5001 instead
```

### Problem: "Import Error: pandas"
**Solution**: Install all requirements
```bash
pip install -r requirements.txt
```

---

## Quick Command Reference

### Windows
```bash
# Install packages
pip install -r requirements.txt

# Train models
python train_models.py

# Run app
python app.py
```

### Mac/Linux
```bash
# Install packages
pip3 install -r requirements.txt

# Train models
python3 train_models.py

# Run app
python3 app.py
```

---

## Project Checklist

Before running:
- [ ] Python installed
- [ ] MySQL installed and running
- [ ] All packages installed (`requirements.txt`)
- [ ] Database created (`database_schema.sql`)
- [ ] Database credentials updated in `app.py`
- [ ] ML models trained (`train_models.py`)

---

## Demo Accounts

### Patients
| Username | Password | Name |
|----------|----------|------|
| patient1 | patient123 | Alice Johnson |
| patient2 | patient123 | Bob Williams |
| patient3 | patient123 | Carol Davis |

### Doctors
| Username | Password | Name | Specialization |
|----------|----------|------|----------------|
| dr.smith | doctor123 | Dr. John Smith | Cardiology |
| dr.jones | doctor123 | Dr. Sarah Jones | Endocrinology |
| dr.brown | doctor123 | Dr. Michael Brown | General Medicine |

---

## First Time Using?

1. **Start here**: http://127.0.0.1:5000
2. **Login as patient**: See existing reports
3. **Login as doctor**: Create new diagnosis
4. **Check Facilities**: View hospital departments

---

## Need Help?

- Check `README.md` for detailed documentation
- Read `ML_EXPLANATION.md` for ML concepts
- Review code comments for understanding

---

## Next Steps

After getting it running:
1. ✅ Test all features
2. ✅ Read code comments
3. ✅ Understand ML workflow
4. ✅ Try modifying UI
5. ✅ Add new features

---

**Happy Coding! 🎉**
