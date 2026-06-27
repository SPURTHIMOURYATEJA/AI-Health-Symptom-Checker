# ============================================================
# symptom_checker.py
# ML Model Training and Prediction Logic
# AI Health Symptom Checker - THINK CHAMP PVT LTD
# ============================================================

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import os

# All possible symptoms (must match dataset columns)
SYMPTOMS = [
    'fever', 'cough', 'headache', 'sore_throat', 'runny_nose',
    'body_pain', 'fatigue', 'nausea', 'vomiting', 'diarrhea',
    'rash', 'sneezing', 'chills', 'loss_of_taste',
    'shortness_of_breath', 'acidity', 'stress', 'eye_pain'
]

# AI-style health recommendations for each disease
RECOMMENDATIONS = {
    'Flu': (
        "Rest at home and stay hydrated. Take fever-reducing medication if needed. "
        "Avoid contact with others to prevent spreading. Consult a doctor if symptoms worsen."
    ),
    'Common Cold': (
        "Stay warm and drink plenty of fluids like warm water and herbal tea. "
        "Use a humidifier if available. Rest well and avoid cold environments. "
        "See a doctor if symptoms last more than 10 days."
    ),
    'Migraine': (
        "Rest in a quiet, dark room. Apply a cold or warm compress to your forehead. "
        "Avoid triggers like bright lights, loud sounds, or strong smells. "
        "Consult a neurologist if migraines are frequent."
    ),
    'Food Poisoning': (
        "Stay hydrated with ORS (Oral Rehydration Solution) or clean water. "
        "Avoid solid foods until vomiting/diarrhea subsides. "
        "Seek immediate medical attention if symptoms are severe or last over 48 hours."
    ),
    'Allergy': (
        "Identify and avoid the allergen causing the reaction. "
        "Take antihistamines as needed. Keep windows closed during high pollen seasons. "
        "Consult an allergist for proper allergy testing."
    ),
    'Dengue': (
        "Seek immediate medical attention — Dengue can be serious. "
        "Rest and stay well hydrated. Avoid aspirin or ibuprofen. "
        "Monitor platelet levels as advised by your doctor."
    ),
    'COVID-19': (
        "Isolate immediately and inform close contacts. Monitor oxygen levels. "
        "Stay hydrated and rest. Consult a doctor if breathing difficulty occurs. "
        "Follow local health authority guidelines."
    ),
    'Acidity': (
        "Avoid spicy, oily, and acidic foods. Eat smaller meals more frequently. "
        "Don't lie down immediately after eating. Drink cold milk for relief. "
        "See a gastroenterologist if symptoms persist."
    ),
    'Stress': (
        "Practice deep breathing, meditation, or yoga. Take regular breaks and sleep 7-8 hours. "
        "Talk to someone you trust about your feelings. "
        "Consult a mental health professional if stress is affecting daily life."
    ),
}


class SymptomChecker:
    """Handles ML model training and disease prediction."""

    def __init__(self):
        self.model = None
        self.label_encoder = LabelEncoder()
        self.accuracy = 0
        self._train_model()

    def _load_data(self):
        """Load and preprocess the dataset."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(base_dir, 'dataset.csv')
        df = pd.read_csv(csv_path)
        X = df[SYMPTOMS]
        y = self.label_encoder.fit_transform(df['disease'])
        return X, y

    def _train_model(self):
        """Train a Random Forest Classifier on the dataset."""
        try:
            X, y = self._load_data()
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            self.model = RandomForestClassifier(
                n_estimators=100, random_state=42
            )
            self.model.fit(X_train, y_train)
            y_pred = self.model.predict(X_test)
            self.accuracy = round(accuracy_score(y_test, y_pred) * 100, 2)
            print(f"[✓] Model trained successfully. Accuracy: {self.accuracy}%")
        except Exception as e:
            print(f"[✗] Model training failed: {e}")

    def predict(self, user_symptoms: list):
        """
        Predict disease from a list of symptom strings.
        Returns: dict with disease, confidence, recommendation
        """
        if self.model is None:
            return {"error": "Model not trained. Please check the dataset."}

        # Build feature vector
        input_vector = [1 if s in user_symptoms else 0 for s in SYMPTOMS]
        input_df = pd.DataFrame([input_vector], columns=SYMPTOMS)

        # Predict
        prediction_encoded = self.model.predict(input_df)[0]
        probabilities = self.model.predict_proba(input_df)[0]
        confidence = round(max(probabilities) * 100, 1)

        disease = self.label_encoder.inverse_transform([prediction_encoded])[0]
        recommendation = RECOMMENDATIONS.get(
            disease,
            "Please consult a qualified healthcare professional for proper diagnosis."
        )

        return {
            "disease": disease,
            "confidence": confidence,
            "recommendation": recommendation,
            "symptoms_entered": user_symptoms,
            "model_accuracy": self.accuracy,
        }

    def get_all_symptoms(self):
        """Return the list of all supported symptoms."""
        return SYMPTOMS
