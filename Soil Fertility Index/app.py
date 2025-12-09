from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import pandas as pd
import numpy as np
from soil_fertility_model import SoilFertilityModel
import os
import json
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-change-me')

# --- Auth / DB Helpers ---
DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_user_table():
    conn = get_db_connection()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()
    finally:
        conn.close()

def create_user(email: str, password: str) -> bool:
    password_hash = generate_password_hash(password)
    try:
        conn = get_db_connection()
        conn.execute("INSERT INTO users (email, password_hash) VALUES (?, ?)", (email.lower().strip(), password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def find_user_by_email(email: str):
    conn = get_db_connection()
    try:
        cur = conn.execute("SELECT * FROM users WHERE email = ?", (email.lower().strip(),))
        return cur.fetchone()
    finally:
        conn.close()

def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('login', next=request.path))
        return view_func(*args, **kwargs)
    return wrapper

# Global model instance
model = None

# --- Dataset column helpers ---
def find_column(df: pd.DataFrame, aliases):
    """Return the first matching existing column from a list of aliases (case-insensitive, tolerant to extra spaces)."""
    normalized = {str(c).strip().lower(): c for c in df.columns}
    for alias in aliases:
        key = str(alias).strip().lower()
        if key in normalized:
            return normalized[key]
    # fuzzy: remove spaces and dots
    simplified = {str(c).replace(' ', '').replace('.', '').lower(): c for c in df.columns}
    for alias in aliases:
        key = str(alias).replace(' ', '').replace('.', '').lower()
        if key in simplified:
            return simplified[key]
    return None

def to_float_safe(value, default=None):
    try:
        if isinstance(value, str):
            # remove any non-numeric trailing chars
            token = value.split()[0].replace('%', '')
            return float(token)
        return float(value)
    except Exception:
        return default

def minmax_scale(series, default=0.0):
    try:
        s = pd.to_numeric(series, errors='coerce')
        vmin = s.min()
        vmax = s.max()
        if pd.isna(vmin) or pd.isna(vmax) or vmax == vmin:
            return s.fillna(default).tolist()
        return ((s - vmin) / (vmax - vmin)).fillna(default).tolist()
    except Exception:
        return [default for _ in range(len(series))]

def load_or_train_model():
    """Load existing model or train a new one"""
    global model
    if os.path.exists('soil_fertility_model.pkl'):
        print("Loading existing model...")
        model = SoilFertilityModel()
        model.load_model('soil_fertility_model.pkl')
    else:
        print("Training new model...")
        df = pd.read_excel('soil_nutrients.xlsx')
        model = SoilFertilityModel()
        model.train_model(df)
        model.save_model('soil_fertility_model.pkl')
    print("Model ready!")

@app.route('/api/train', methods=['POST'])
@login_required
def api_train():
    """Retrain model on soil_nutrients.xlsx and return evaluation metrics."""
    global model
    try:
        df = pd.read_excel('soil_nutrients.xlsx')
        if model is None:
            model = SoilFertilityModel()
        # Use all data with K-Fold CV for evaluation, then fit final model
        metrics = model.evaluate_full(df, n_splits=5)
        model.save_model('soil_fertility_model.pkl')
        return jsonify({'ok': True, 'metrics': metrics}), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400

def _fig_to_data_url(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return f"data:image/png;base64,{b64}"

@app.route('/api/train/plots', methods=['POST'])
@login_required
def api_train_plots():
    """Retrain and return images for confusion matrix and accuracy-per-fold as data URLs."""
    global model
    try:
        df = pd.read_excel('soil_nutrients.xlsx')
        if model is None:
            model = SoilFertilityModel()
        metrics = model.evaluate_full(df, n_splits=5)
        model.save_model('soil_fertility_model.pkl')

        cls = metrics.get('classification', {})
        labels = cls.get('labels', [])
        cm = np.array(cls.get('confusion_matrix', []))
        acc = metrics.get('accuracy_per_fold', {})
        train = np.array(acc.get('train', []))
        val = np.array(acc.get('val', []))

        # Confusion matrix figure
        fig_cm, ax = plt.subplots(figsize=(6, 5))
        im = ax.imshow(cm, cmap='Blues')
        ax.set_title('Confusion Matrix (Categories)')
        ax.set_xlabel('Predicted')
        ax.set_ylabel('True')
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=45, ha='right')
        ax.set_yticks(range(len(labels)))
        ax.set_yticklabels(labels)
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(j, i, f"{int(cm[i, j])}", ha='center', va='center', color='black')
        fig_cm.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cm_url = _fig_to_data_url(fig_cm)

        # Accuracy per fold figure
        fig_acc, ax2 = plt.subplots(figsize=(6, 4))
        if train.size and val.size:
            ax2.plot(range(1, len(train)+1), train, marker='o', label='Train', color='#10b981')
            ax2.plot(range(1, len(val)+1), val, marker='o', label='Val', color='#3b82f6')
            ax2.set_ylim(0, 1)
        ax2.set_xlabel('Fold')
        ax2.set_ylabel('Accuracy')
        ax2.set_title('Accuracy per Fold')
        ax2.legend()
        acc_url = _fig_to_data_url(fig_acc)

        return jsonify({'ok': True, 'metrics': metrics, 'plots': {'confusion_matrix': cm_url, 'accuracy': acc_url}}), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400

@app.route('/api/train/save-plots', methods=['POST'])
@login_required
def api_train_save_plots():
    """Retrain, generate evaluation plots, and save to static/evaluation folder. Returns saved file paths."""
    global model
    try:
        df = pd.read_excel('soil_nutrients.xlsx')
        if model is None:
            model = SoilFertilityModel()
        metrics = model.evaluate_full(df, n_splits=5)
        model.save_model('soil_fertility_model.pkl')

        # Ensure output directory exists
        out_dir = os.path.join(os.path.dirname(__file__), 'static', 'evaluation')
        os.makedirs(out_dir, exist_ok=True)

        # Confusion matrix
        cls = metrics.get('classification', {})
        labels = cls.get('labels', [])
        cm = np.array(cls.get('confusion_matrix', []))
        fig_cm, ax = plt.subplots(figsize=(6, 5))
        im = ax.imshow(cm, cmap='Blues')
        ax.set_title('Confusion Matrix (Categories)')
        ax.set_xlabel('Predicted')
        ax.set_ylabel('True')
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=45, ha='right')
        ax.set_yticks(range(len(labels)))
        ax.set_yticklabels(labels)
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(j, i, f"{int(cm[i, j])}", ha='center', va='center', color='black')
        fig_cm.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cm_path = os.path.join(out_dir, 'confusion_matrix.png')
        fig_cm.savefig(cm_path, bbox_inches='tight')
        plt.close(fig_cm)

        # Accuracy per fold
        acc = metrics.get('accuracy_per_fold', {})
        train = np.array(acc.get('train', []))
        val = np.array(acc.get('val', []))
        fig_acc, ax2 = plt.subplots(figsize=(6, 4))
        if train.size:
            ax2.plot(range(1, len(train)+1), train, marker='o', label='Train', color='#10b981')
        if val.size:
            ax2.plot(range(1, len(val)+1), val, marker='o', label='Val', color='#3b82f6')
        ax2.set_ylim(0, 1)
        ax2.set_xlabel('Fold')
        ax2.set_ylabel('Accuracy')
        ax2.set_title('Accuracy per Fold')
        ax2.legend()
        acc_path = os.path.join(out_dir, 'accuracy_per_fold.png')
        fig_acc.savefig(acc_path, bbox_inches='tight')
        plt.close(fig_acc)

        # Also save copies to project root folder for easy access
        root_dir = os.path.dirname(__file__)
        cm_root = os.path.join(root_dir, 'confusion_matrix.png')
        acc_root = os.path.join(root_dir, 'accuracy_per_fold.png')
        try:
            from shutil import copyfile
            copyfile(cm_path, cm_root)
            copyfile(acc_path, acc_root)
        except Exception:
            pass

        # Return relative paths for convenience
        rel_cm = os.path.join('static', 'evaluation', 'confusion_matrix.png')
        rel_acc = os.path.join('static', 'evaluation', 'accuracy_per_fold.png')
        return jsonify({'ok': True, 'metrics': metrics, 'files': {'confusion_matrix': rel_cm, 'accuracy': rel_acc}, 'root_files': {'confusion_matrix': 'confusion_matrix.png', 'accuracy': 'accuracy_per_fold.png'}}), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400

@app.route('/api/soil-predictions')
@login_required
def api_soil_predictions():
    """Return per-sample predictions (SFI, category, top recommendations) for all unique coordinates."""
    global model
    try:
        if model is None:
            # Ensure model is available
            load_or_train_model()
        df = pd.read_excel('soil_nutrients.xlsx')
        col_lat = find_column(df, ['Latitude', 'latitude', 'Lat', 'lat'])
        col_lon = find_column(df, ['Longitude', 'longitude', 'Lon', 'lon', 'Long'])
        if not col_lat or not col_lon:
            return jsonify({'points': []})
        col_series = find_column(df, ['Soil Series', 'Series', 'soil_series'])
        col_class = find_column(df, ['Soil Classification ', 'Soil Classification', 'Classification', 'soil_classification'])
        # Build unique samples
        df_clean = df.dropna(subset=[col_lat, col_lon]).copy()
        unique_samples = df_clean.groupby([col_lat, col_lon]).first().reset_index()

        # Prepare outputs
        results = []
        for _, r in unique_samples.iterrows():
            lat = to_float_safe(r[col_lat], None)
            lon = to_float_safe(r[col_lon], None)
            if lat is None or lon is None:
                continue
            # Compose features for prediction similar to location-info
            # Try to pull available columns; fallback defaults
            col_ph = find_column(df, ['Soil Properties.3', 'Soil Properties.4', 'pH', 'ph'])
            col_oc = find_column(df, ['Soil Properties.5', 'Organic Carbon', 'OC'])
            col_om = find_column(df, ['Soil Properties.6', 'Organic Matter', 'OM'])
            col_n = find_column(df, ['Soil Properties.7', 'Nitrogen', 'N'])
            col_p = find_column(df, ['Soil Properties.8', 'Phosphorus', 'P'])
            col_k = find_column(df, ['Soil Properties.9', 'Potassium', 'K'])
            col_ca = find_column(df, ['Soil Properties.10', 'Calcium', 'Ca'])
            col_mg = find_column(df, ['Soil Properties.11', 'Magnesium', 'Mg'])
            col_ecec = find_column(df, ['Soil Properties.12', 'ECEC', 'Cation Exchange Capacity', 'CEC'])
            col_sand = find_column(df, ['Soil Properties.1', 'Sand', 'Sand %', 'sand'])

            features = {
                'Soil Properties.1': to_float_safe(r.get(col_sand, 90.0), 90.0),
                'Soil Properties.4': to_float_safe(r.get(col_ph, 6.5), 6.5),
                'Soil Properties.5': to_float_safe(r.get(col_oc, 0.5), 0.5),
                'Soil Properties.6': to_float_safe(r.get(col_om, 1.0), 1.0),
                'Soil Properties.7': to_float_safe(r.get(col_n, 0.05), 0.05),
                'Soil Properties.8': to_float_safe(r.get(col_p, 5.0), 5.0),
                'Soil Properties.9': to_float_safe(r.get(col_k, 0.5), 0.5),
                'Soil Properties.10': to_float_safe(r.get(col_ca, 1.0), 1.0),
                'Soil Properties.11': to_float_safe(r.get(col_mg, 0.5), 0.5),
                'Soil Properties.12': to_float_safe(r.get(col_ecec, 2.0), 2.0)
            }
            pred = model.predict_fertility(features)
            recs = pred.get('recommendations', [])[:3]
            results.append({
                'lat': lat,
                'lng': lon,
                'series': str(r.get(col_series)) if col_series else '',
                'classification': str(r.get(col_class)) if col_class else '',
                'sfi': float(pred.get('sfi_actual', 0.0)),
                'category': pred.get('category'),
                'color': pred.get('color'),
                'recommendations': recs
            })
        return jsonify({'points': results})
    except Exception as e:
        return jsonify({'points': [], 'error': str(e)}), 200

@app.route('/')
@login_required
def index():
    """Main page with GIS interface"""
    return render_template('index.html')

# Removed manual prediction endpoint - now handled automatically in location-info

@app.route('/api/location-info', methods=['POST'])
@login_required
def get_location_info():
    """Get soil information for a specific location"""
    try:
        data = request.get_json()
        lat = float(data.get('latitude'))
        lon = float(data.get('longitude'))
        
        # Load the dataset to find nearest soil data
        df = pd.read_excel('soil_nutrients.xlsx')

        # Resolve column names robustly
        col_lat = find_column(df, ['Latitude', 'latitude', 'Lat', 'lat'])
        col_lon = find_column(df, ['Longitude', 'longitude', 'Lon', 'lon', 'Long'])
        col_series = find_column(df, ['Soil Series', 'Series', 'soil_series'])
        col_class = find_column(df, ['Soil Classification ', 'Soil Classification', 'Classification', 'soil_classification'])
        col_texture = find_column(df, ['Soil Properties.2', 'Texture', 'Soil Texture'])
        col_ph = find_column(df, ['Soil Properties.3', 'Soil Properties.4', 'pH', 'ph'])  # dataset inconsistency
        col_oc = find_column(df, ['Soil Properties.5', 'Organic Carbon', 'OC'])
        col_om = find_column(df, ['Soil Properties.6', 'Organic Matter', 'OM'])
        col_n = find_column(df, ['Soil Properties.7', 'Nitrogen', 'N'])
        col_p = find_column(df, ['Soil Properties.8', 'Phosphorus', 'P'])
        col_k = find_column(df, ['Soil Properties.9', 'Potassium', 'K'])
        col_ca = find_column(df, ['Soil Properties.10', 'Calcium', 'Ca'])
        col_mg = find_column(df, ['Soil Properties.11', 'Magnesium', 'Mg'])
        col_ecec = find_column(df, ['Soil Properties.12', 'ECEC', 'Cation Exchange Capacity', 'CEC'])
        
        # Filter out rows without coordinates and get unique soil samples
        if not col_lat or not col_lon:
            raise ValueError('Latitude/Longitude columns not found in dataset')
        df_clean = df.dropna(subset=[col_lat, col_lon]).copy()
        
        # Group by coordinates to get unique soil samples (avoid duplicate coordinates)
        unique_samples = df_clean.groupby([col_lat, col_lon]).first().reset_index()
        
        # Calculate distances and find nearest point
        distances = np.sqrt((unique_samples[col_lat].astype(float) - lat)**2 + (unique_samples[col_lon].astype(float) - lon)**2)
        nearest_idx = distances.idxmin()
        nearest_soil = unique_samples.loc[nearest_idx]
        
        # Get soil classification and properties
        soil_info = {
            'soil_series': (nearest_soil.get(col_series) if col_series else 'Unknown') or 'Unknown',
            'soil_classification': (nearest_soil.get(col_class) if col_class else 'Unknown') or 'Unknown',
            'texture': (nearest_soil.get(col_texture) if col_texture else 'Unknown') or 'Unknown',
            'ph': nearest_soil.get(col_ph, 'Unknown') if col_ph else 'Unknown',
            'organic_carbon': nearest_soil.get(col_oc, 'Unknown') if col_oc else 'Unknown',
            'organic_matter': nearest_soil.get(col_om, 'Unknown') if col_om else 'Unknown',
            'nitrogen': nearest_soil.get(col_n, 'Unknown') if col_n else 'Unknown',
            'phosphorus': nearest_soil.get(col_p, 'Unknown') if col_p else 'Unknown',
            'potassium': nearest_soil.get(col_k, 'Unknown') if col_k else 'Unknown',
            'distance_km': round(distances[nearest_idx] * 111, 2),  # Approximate km
            'calcium': nearest_soil.get(col_ca, 'Unknown') if col_ca else 'Unknown',
            'magnesium': nearest_soil.get(col_mg, 'Unknown') if col_mg else 'Unknown',
            'ecec': nearest_soil.get(col_ecec, 'Unknown') if col_ecec else 'Unknown'
        }
        
        # If location is within reasonable range (within 100km), provide detailed analysis
        if distances[nearest_idx] * 111 <= 100:  # 100km threshold
            # Prepare soil properties for fertility analysis using actual dataset values
            soil_properties = {
                'Soil Properties.1': to_float_safe(nearest_soil.get(find_column(df, ['Soil Properties.1', 'Sand', 'Sand %', 'sand']), 90.0), 90.0),
                # Model expects pH at key .4; feed numeric from detected pH
                'Soil Properties.4': to_float_safe(nearest_soil.get(col_ph, 6.5), 6.5),
                'Soil Properties.5': to_float_safe(nearest_soil.get(col_oc, 0.5), 0.5),
                'Soil Properties.6': to_float_safe(nearest_soil.get(col_om, 1.0), 1.0),
                'Soil Properties.7': to_float_safe(nearest_soil.get(col_n, 0.05), 0.05),
                'Soil Properties.8': to_float_safe(nearest_soil.get(col_p, 5.0), 5.0),
                'Soil Properties.9': to_float_safe(nearest_soil.get(col_k, 0.5), 0.5),
                'Soil Properties.10': to_float_safe(nearest_soil.get(col_ca, 1.0), 1.0),
                'Soil Properties.11': to_float_safe(nearest_soil.get(col_mg, 0.5), 0.5),
                'Soil Properties.12': to_float_safe(nearest_soil.get(col_ecec, 2.0), 2.0)
            }
            
            # Get fertility analysis
            fertility_result = model.predict_fertility(soil_properties)
            
            # Add fertility analysis to soil info
            soil_info.update({
                'fertility_analysis': {
                    'sfi_score': fertility_result['sfi_actual'],
                    'category': fertility_result['category'],
                    'color': fertility_result['color'],
                    'recommendations': fertility_result['recommendations']
                },
                'analysis_available': True
            })
        else:
            soil_info['analysis_available'] = False
            soil_info['fertility_analysis'] = None
        
        return jsonify(soil_info)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/sample-data')
@login_required
def get_sample_data():
    """Get sample soil data for demonstration"""
    sample_data = {
        'sand_percent': 90.0,
        'ph': 6.0,
        'organic_carbon': 0.5,
        'organic_matter': 0.9,
        'nitrogen': 0.04,
        'phosphorus': 5.0,
        'potassium': 0.1,
        'calcium': 1.5,
        'magnesium': 0.8,
        'ecec': 3.0
    }
    return jsonify(sample_data)

# --- Auth Routes ---

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        if not email or not password:
            flash('Email and password are required.', 'error')
            return redirect(url_for('signup'))
        if password != confirm:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('signup'))
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return redirect(url_for('signup'))

        created = create_user(email, password)
        if not created:
            flash('An account with this email already exists.', 'error')
            return redirect(url_for('signup'))

        user = find_user_by_email(email)
        session['user_id'] = user['id']
        session['user_email'] = user['email']
        flash('Welcome! Your account has been created.', 'success')
        return redirect(url_for('index'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        user = find_user_by_email(email)
        if not user or not check_password_hash(user['password_hash'], password):
            flash('Invalid email or password.', 'error')
            return redirect(url_for('login'))

        session['user_id'] = user['id']
        session['user_email'] = user['email']
        next_url = request.args.get('next') or url_for('index')
        return redirect(next_url)

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# Optional: keep logged-out page in case you want to link to it manually later
@app.route('/logged-out')
def logged_out():
    return render_template('logged_out.html')

# --- Data-derived NDVI/DEM endpoints (from Excel points) ---

@app.route('/api/ndvi-points')
@login_required
def ndvi_points():
    df = pd.read_excel('soil_nutrients.xlsx')
    col_lat = find_column(df, ['Latitude', 'latitude', 'Lat', 'lat'])
    col_lon = find_column(df, ['Longitude', 'longitude', 'Lon', 'lon', 'Long'])
    if not col_lat or not col_lon:
        return jsonify({'error': 'Latitude/Longitude columns not found'}), 400

    # Prefer a real NDVI column if present; else derive proxy from organic content
    col_ndvi = find_column(df, ['NDVI', 'ndvi'])
    if col_ndvi:
        values = pd.to_numeric(df[col_ndvi], errors='coerce')
        norm_vals = minmax_scale(values, default=0.0)
    else:
        # Proxy NDVI: blend of Organic Matter and Organic Carbon if available
        col_oc = find_column(df, ['Soil Properties.5', 'Organic Carbon', 'OC'])
        col_om = find_column(df, ['Soil Properties.6', 'Organic Matter', 'OM'])
        base = pd.Series([0.0] * len(df))
        if col_oc:
            base = base.add(pd.to_numeric(df[col_oc], errors='coerce').fillna(0), fill_value=0)
        if col_om:
            base = base.add(pd.to_numeric(df[col_om], errors='coerce').fillna(0), fill_value=0)
        norm_vals = minmax_scale(base, default=0.0)

    points = []
    for lat, lon, v in zip(df[col_lat], df[col_lon], norm_vals):
        if pd.notna(lat) and pd.notna(lon):
            points.append({'lat': float(lat), 'lon': float(lon), 'value': float(v)})
    return jsonify({'points': points})

@app.route('/api/dem-points')
@login_required
def dem_points():
    df = pd.read_excel('soil_nutrients.xlsx')
    col_lat = find_column(df, ['Latitude', 'latitude', 'Lat', 'lat'])
    col_lon = find_column(df, ['Longitude', 'longitude', 'Lon', 'lon', 'Long'])
    if not col_lat or not col_lon:
        return jsonify({'error': 'Latitude/Longitude columns not found'}), 400

    col_dem = find_column(df, ['Elevation', 'elevation', 'Altitude', 'altitude', 'DEM', 'dem', 'Elevation (m)'])
    if not col_dem:
        return jsonify({'error': 'Elevation/DEM column not found'}), 400

    values = pd.to_numeric(df[col_dem], errors='coerce')
    norm_vals = minmax_scale(values, default=0.0)
    points = []
    for lat, lon, v, raw in zip(df[col_lat], df[col_lon], norm_vals, values):
        if pd.notna(lat) and pd.notna(lon):
            points.append({'lat': float(lat), 'lon': float(lon), 'value': float(v), 'elev': to_float_safe(raw, None)})
    return jsonify({'points': points})

if __name__ == '__main__':
    init_user_table()
    load_or_train_model()
    app.run(debug=True, host='0.0.0.0', port=5000)
