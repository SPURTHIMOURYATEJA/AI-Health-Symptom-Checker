# ============================================================
# app.py
# Flask Web Application Entry Point
# AI Health Symptom Checker - THINK CHAMP PVT LTD
# ============================================================

from flask import Flask, render_template, request, send_file, redirect, url_for, session
from symptom_checker import SymptomChecker
from visualizations import generate_all_charts
from report_generator import generate_report
import os

app = Flask(__name__)
app.secret_key = 'thinkchamp_health_ai_2024'

# Initialize the ML model once at startup
checker = SymptomChecker()
ALL_SYMPTOMS = checker.get_all_symptoms()

# ── HOME PAGE ──────────────────────────────────────────────
@app.route('/')
def index():
    """Render the home page with symptom input form."""
    symptoms_display = [s.replace('_', ' ').title() for s in ALL_SYMPTOMS]
    return render_template('index.html',
                           symptoms=ALL_SYMPTOMS,
                           symptoms_display=symptoms_display)


# ── PREDICT / RESULT PAGE ─────────────────────────────────
@app.route('/predict', methods=['POST'])
def predict():
    """Handle form submission, run prediction, generate charts and report."""
    try:
        # Get selected symptoms from form
        selected = request.form.getlist('symptoms')

        # Validation
        if not selected:
            return render_template('index.html',
                                   symptoms=ALL_SYMPTOMS,
                                   symptoms_display=[s.replace('_',' ').title() for s in ALL_SYMPTOMS],
                                   error="⚠ Please select at least one symptom before submitting.")

        # Run ML prediction
        result = checker.predict(selected)

        # Generate charts
        charts = generate_all_charts(
            disease=result['disease'],
            confidence=result['confidence'],
            user_symptoms=selected,
            all_symptoms=ALL_SYMPTOMS
        )

        # Generate downloadable report
        report_file = generate_report(result)

        # Format symptoms for display
        symptoms_display = [s.replace('_', ' ').title() for s in selected]

        # Store report filename in session for download
        session['report_file'] = report_file

        return render_template('result.html',
                               result=result,
                               symptoms_display=symptoms_display,
                               charts=charts,
                               report_file=report_file)

    except Exception as e:
        return render_template('index.html',
                               symptoms=ALL_SYMPTOMS,
                               symptoms_display=[s.replace('_',' ').title() for s in ALL_SYMPTOMS],
                               error=f"An error occurred: {str(e)}")


# ── DOWNLOAD REPORT ───────────────────────────────────────
@app.route('/download/<filename>')
def download_report(filename):
    """Download the generated health report."""
    try:
        reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reports')
        file_path   = os.path.join(reports_dir, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        return "Report not found.", 404
    except Exception as e:
        return f"Download error: {e}", 500


# ── ABOUT PAGE ────────────────────────────────────────────
@app.route('/about')
def about():
    """Render the About page."""
    return render_template('about.html')


# ── MAIN ──────────────────────────────────────────────────
if __name__ == '__main__':
    print("=" * 55)
    print("  AI Health Symptom Checker — THINK CHAMP PVT LTD")
    print("  Visit: http://127.0.0.1:5000")
    print("=" * 55)
    app.run(debug=True)
