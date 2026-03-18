import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
from django.conf import settings

try:
    BASE_DIR = settings.BASE_DIR
except:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_FILE = os.path.join(BASE_DIR, 'recommender', 'diet_model.pkl')

def generate_synthetic_data(n_samples=3000):
    np.random.seed(42)
    genders = np.random.choice([0, 1, 2], size=n_samples, p=[0.48, 0.48, 0.04]) # 0:male, 1:female, 2:other
    ages = np.random.randint(18, 70, size=n_samples)
    bmis = np.random.uniform(18.0, 40.0, size=n_samples)
    
    lifestyles = np.random.randint(0, 4, size=n_samples)
    
    has_diabetes = np.random.choice([0, 1], size=n_samples, p=[0.8, 0.2])
    has_hypertension = np.random.choice([0, 1], size=n_samples, p=[0.75, 0.25])
    has_heart_disease = np.random.choice([0, 1], size=n_samples, p=[0.9, 0.1])
    has_celiac = np.random.choice([0, 1], size=n_samples, p=[0.95, 0.05])
    has_lactose_intolerance = np.random.choice([0, 1], size=n_samples, p=[0.85, 0.15])
    
    targets = []
    
    for i in range(n_samples):
        # Base Diet logic
        if has_diabetes[i] == 1:
            base_diet = 'Diabetic Friendly (Low Carb/Low Sugar)'
        elif has_heart_disease[i] == 1 or has_hypertension[i] == 1:
            base_diet = 'DASH / Heart Healthy Diet'
        elif bmis[i] > 25.0 and lifestyles[i] < 2:
            base_diet = 'Weight Loss / Calorie Deficit Diet'
        elif lifestyles[i] == 3:
            base_diet = 'High Protein Athlete Diet'
        else:
            base_diet = 'Mediterranean Balanced Diet'
            
        # Add modifiers based on intolerances
        modifiers = []
        if has_celiac[i] == 1:
            modifiers.append("Gluten-Free")
        if has_lactose_intolerance[i] == 1:
            modifiers.append("Lactose-Free")
            
        if modifiers:
            targets.append(f"{base_diet} ({' & '.join(modifiers)})")
        else:
            targets.append(base_diet)
            
    df = pd.DataFrame({
        'gender': genders,
        'age': ages,
        'bmi': bmis,
        'lifestyle': lifestyles,
        'has_diabetes': has_diabetes,
        'has_hypertension': has_hypertension,
        'has_heart_disease': has_heart_disease,
        'has_celiac': has_celiac,
        'has_lactose_intolerance': has_lactose_intolerance,
        'target': targets
    })
    return df

def train_model():
    df = generate_synthetic_data(3000)
    X = df.drop('target', axis=1)
    y = df['target']
    
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, y)
    
    joblib.dump(clf, MODEL_FILE)
    print(f"Model saved to {MODEL_FILE}")
    return clf

def predict_diet(gender_str, age, bmi, lifestyle_str, diab, hyper, heart, celiac, lactose):
    if not os.path.exists(MODEL_FILE):
        train_model()
        
    clf = joblib.load(MODEL_FILE)
    
    gender_mapping = {
        'male': 0,
        'female': 1,
        'other': 2
    }
    gen_val = gender_mapping.get(gender_str, 2)
    
    lifestyle_mapping = {
        'sedentary': 0,
        'lightly_active': 1,
        'moderately_active': 2,
        'very_active': 3
    }
    ls_val = lifestyle_mapping.get(lifestyle_str, 0)
    
    features = pd.DataFrame([{
        'gender': gen_val,
        'age': age,
        'bmi': bmi,
        'lifestyle': ls_val,
        'has_diabetes': int(diab),
        'has_hypertension': int(hyper),
        'has_heart_disease': int(heart),
        'has_celiac': int(celiac),
        'has_lactose_intolerance': int(lactose)
    }])
    
    prediction = clf.predict(features)[0]
    return prediction

if __name__ == "__main__":
    train_model()
