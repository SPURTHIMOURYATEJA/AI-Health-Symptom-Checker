# ============================================================
# visualizations.py
# Chart Generation using Matplotlib and Seaborn
# AI Health Symptom Checker - THINK CHAMP PVT LTD
# ============================================================

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for Flask

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

# Charts output directory
CHARTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'charts')
os.makedirs(CHARTS_DIR, exist_ok=True)

# Color palette
PALETTE = ['#00b894', '#0984e3', '#6c5ce7', '#fdcb6e', '#e17055', '#00cec9', '#fd79a8', '#55efc4', '#74b9ff']

def set_style():
    """Apply a consistent dark-health style to all charts."""
    plt.rcParams.update({
        'figure.facecolor': '#0f172a',
        'axes.facecolor':   '#1e293b',
        'axes.edgecolor':   '#334155',
        'axes.labelcolor':  '#e2e8f0',
        'xtick.color':      '#94a3b8',
        'ytick.color':      '#94a3b8',
        'text.color':       '#e2e8f0',
        'grid.color':       '#334155',
        'grid.linestyle':   '--',
        'grid.alpha':       0.5,
        'font.family':      'DejaVu Sans',
    })


def generate_confidence_chart(disease: str, confidence: float, filename='confidence_chart.png'):
    """Donut chart showing confidence score."""
    set_style()
    fig, ax = plt.subplots(figsize=(5, 5), facecolor='#0f172a')
    values = [confidence, 100 - confidence]
    colors = ['#00b894', '#1e293b']
    wedge_props = {'width': 0.45, 'edgecolor': '#0f172a', 'linewidth': 3}
    ax.pie(values, colors=colors, wedgeprops=wedge_props, startangle=90)
    ax.text(0, 0, f"{confidence}%", ha='center', va='center',
            fontsize=28, fontweight='bold', color='#00b894')
    ax.text(0, -0.35, 'Confidence', ha='center', fontsize=11, color='#94a3b8')
    ax.set_title(f'Prediction: {disease}', color='#e2e8f0', fontsize=13, pad=15)
    path = os.path.join(CHARTS_DIR, filename)
    plt.tight_layout()
    plt.savefig(path, dpi=120, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    return filename


def generate_symptom_bar_chart(user_symptoms: list, all_symptoms: list, filename='symptom_bar.png'):
    """Horizontal bar chart of entered symptoms."""
    set_style()
    labels = [s.replace('_', ' ').title() for s in all_symptoms]
    values = [1 if s in user_symptoms else 0 for s in all_symptoms]
    colors = ['#00b894' if v else '#334155' for v in values]

    fig, ax = plt.subplots(figsize=(7, 5.5), facecolor='#0f172a')
    bars = ax.barh(labels, values, color=colors, edgecolor='#0f172a', height=0.6)
    ax.set_xlim(0, 1.3)
    ax.set_xlabel('Present (1) / Absent (0)', color='#94a3b8')
    ax.set_title('Symptom Analysis', color='#e2e8f0', fontsize=13, pad=12)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Absent', 'Present'])
    ax.grid(axis='x', alpha=0.3)
    for bar, val in zip(bars, values):
        if val:
            ax.text(bar.get_width() + 0.03, bar.get_y() + bar.get_height()/2,
                    '✓', va='center', color='#00b894', fontsize=10)
    path = os.path.join(CHARTS_DIR, filename)
    plt.tight_layout()
    plt.savefig(path, dpi=120, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    return filename


def generate_disease_distribution_chart(filename='disease_dist.png'):
    """Pie chart of disease distribution in the dataset."""
    set_style()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(base_dir, 'dataset.csv'))
    counts = df['disease'].value_counts()

    fig, ax = plt.subplots(figsize=(6, 6), facecolor='#0f172a')
    wedges, texts, autotexts = ax.pie(
        counts.values,
        labels=counts.index,
        autopct='%1.0f%%',
        colors=PALETTE[:len(counts)],
        startangle=140,
        pctdistance=0.82,
        wedgeprops={'edgecolor': '#0f172a', 'linewidth': 2}
    )
    for t in texts:    t.set_color('#e2e8f0'); t.set_fontsize(9)
    for t in autotexts: t.set_color('#0f172a'); t.set_fontweight('bold'); t.set_fontsize(8)
    ax.set_title('Disease Distribution in Dataset', color='#e2e8f0', fontsize=13, pad=15)
    path = os.path.join(CHARTS_DIR, filename)
    plt.tight_layout()
    plt.savefig(path, dpi=120, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    return filename


def generate_symptom_heatmap(filename='symptom_heatmap.png'):
    """Heatmap of symptom frequency per disease."""
    set_style()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(base_dir, 'dataset.csv'))

    symptom_cols = [c for c in df.columns if c != 'disease']
    heat_data = df.groupby('disease')[symptom_cols].mean()
    heat_data.columns = [c.replace('_', ' ').title() for c in heat_data.columns]

    fig, ax = plt.subplots(figsize=(12, 5), facecolor='#0f172a')
    sns.heatmap(
        heat_data, annot=True, fmt='.1f', cmap='YlGn',
        linewidths=0.5, linecolor='#0f172a',
        cbar_kws={'label': 'Avg Presence'},
        ax=ax
    )
    ax.set_title('Symptom Frequency per Disease', color='#e2e8f0', fontsize=13, pad=12)
    ax.tick_params(colors='#e2e8f0', labelsize=8)
    ax.set_ylabel('')
    path = os.path.join(CHARTS_DIR, filename)
    plt.tight_layout()
    plt.savefig(path, dpi=120, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    return filename


def generate_all_charts(disease, confidence, user_symptoms, all_symptoms):
    """Generate all charts and return their filenames."""
    charts = {}
    try: charts['confidence'] = generate_confidence_chart(disease, confidence)
    except Exception as e: print(f"Confidence chart error: {e}")
    try: charts['symptom_bar'] = generate_symptom_bar_chart(user_symptoms, all_symptoms)
    except Exception as e: print(f"Symptom bar error: {e}")
    try: charts['disease_dist'] = generate_disease_distribution_chart()
    except Exception as e: print(f"Disease dist error: {e}")
    try: charts['heatmap'] = generate_symptom_heatmap()
    except Exception as e: print(f"Heatmap error: {e}")
    return charts
