 # 🩺 AI Health Symptom Checker

**Internship Major Project — THINK CHAMP PVT LTD**

---

## Project Overview

An AI-powered health symptom checker web application built with Python Flask and Machine Learning. Users can select symptoms, get a predicted health condition with confidence score, view data visualizations, and download a health report.

---

## Features

- ✅ Interactive symptom selection form (18 symptoms)
- 🤖 Random Forest ML model for disease prediction
- 📊 Confidence score with animated progress bar
- 💡 AI-generated health recommendations
- 📈 4 data visualizations (donut chart, bar chart, pie chart, heatmap)
- 📄 Downloadable health report (.txt)
- 📱 Responsive design (mobile + desktop)
- ⚠️ Medical disclaimer on every page
- 🏠 Home, Result, and About pages

---

## Project Structure

```
AI_Health_Symptom_Checker/
├── app.py                  ← Flask web application (routes)
├── symptom_checker.py      ← ML model training & prediction
├── visualizations.py       ← Chart generation (Matplotlib/Seaborn)
├── report_generator.py     ← Health report generation
├── dataset.csv             ← Symptom-disease training dataset
├── requirements.txt        ← Python dependencies
├── README.md               ← This file
├── templates/
│   ├── index.html          ← Home page
│   ├── result.html         ← Result page
│   └── about.html          ← About page
├── static/
│   ├── style.css           ← Stylesheet
│   ├── script.js           ← JavaScript
│   └── charts/             ← Generated chart images
├── reports/                ← Generated health reports
└── screenshots/            ← Project screenshots
```

---

## How to Run (Windows PowerShell)

### Step 1 — Navigate to project folder
```powershell
cd "C:\path\to\AI_Health_Symptom_Checker"
```

### Step 2 — Create a virtual environment (recommended)
```powershell
python -m venv venv
venv\Scripts\activate
```

### Step 3 — Install dependencies
```powershell
pip install -r requirements.txt
```

### Step 4 — Run the Flask app
```powershell
python app.py
```

### Step 5 — Open in browser
```
http://127.0.0.1:5000
```

---

## Technologies Used

| Technology    | Purpose                              |
|---------------|--------------------------------------|
| Python        | Core programming language            |
| Flask         | Web framework                        |
| Scikit-learn  | Random Forest ML model               |
| Pandas        | Dataset processing                   |
| NumPy         | Numerical operations                 |
| Matplotlib    | Chart generation                     |
| Seaborn       | Heatmap visualization                |
| HTML5/CSS3    | Frontend UI                          |
| JavaScript    | Form validation & interactivity      |

---

## Diseases Covered

Flu, Common Cold, Migraine, Food Poisoning, Allergy, Dengue, COVID-19, Acidity, Stress

---

## Module Explanations

- **app.py** — Flask routes: home `/`, predict `/predict`, download `/download`, about `/about`
- **symptom_checker.py** — Loads dataset, trains Random Forest, returns prediction + confidence
- **visualizations.py** — Generates 4 charts saved to `static/charts/`
- **report_generator.py** — Creates timestamped `.txt` health reports in `reports/`
- **dataset.csv** — 45 records, 18 symptom features, 9 disease labels

---

## Sample Output

**Input:** Fever, Cough, Headache

**Result:**
- Possible Condition: **Flu**
- Confidence Score: **85%**
- Recommendation: Rest at home, stay hydrated, consult a doctor if symptoms worsen.

---

## Git Info

**Repository Description:**
> AI Health Symptom Checker — A Flask web application using Machine Learning (Random Forest) to predict health conditions from user-selected symptoms, with data visualizations and downloadable health reports. Built as an internship project for THINK CHAMP PVT LTD.

**Commit Message:**
```
feat: Add AI Health Symptom Checker Flask web app with ML prediction, charts, and report generation
```

---

## Medical Disclaimer

> ⚠️ This project is for **educational purposes only** and is **not a substitute for professional medical advice**. Always consult a qualified healthcare professional for proper diagnosis and treatment.

---

*© 2024 THINK CHAMP PVT LTD — Internship Major Project*
