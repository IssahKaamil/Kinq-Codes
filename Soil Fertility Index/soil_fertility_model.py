import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, KFold, RandomizedSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, confusion_matrix, accuracy_score, precision_recall_fscore_support
import joblib
import warnings
warnings.filterwarnings('ignore')

class SoilFertilityModel:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = []
        
    def preprocess_data(self, df):
        """Preprocess the soil nutrients dataset"""
        # Remove the first row (header row) and rows with missing coordinates
        df_clean = df.dropna(subset=['Latitude', 'Longitude']).copy()
        
        # Convert soil properties to numeric where possible
        numeric_columns = ['Soil Properties.1', 'Soil Properties.2', 'Soil Properties.3', 
                          'Soil Properties.4', 'Soil Properties.5', 'Soil Properties.6',
                          'Soil Properties.7', 'Soil Properties.8', 'Soil Properties.9',
                          'Soil Properties.10', 'Soil Properties.11', 'Soil Properties.12']
        
        for col in numeric_columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
        
        # Handle categorical variables
        categorical_columns = ['Soil Classification', 'Soil Properties.2', 'Soil Properties.3']
        
        for col in categorical_columns:
            if col in df_clean.columns:
                le = LabelEncoder()
                df_clean[f'{col}_encoded'] = le.fit_transform(df_clean[col].astype(str))
                self.label_encoders[col] = le
        
        # Create feature columns - only include numeric columns that exist
        potential_features = []
        for col in df_clean.columns:
            if col not in ['Soil Series', 'Soil Classification', 'Soil Properties', 
                          'Soil Properties.2', 'Soil Properties.3', 'Latitude', 'Longitude']:
                if df_clean[col].dtype in ['int64', 'float64']:
                    potential_features.append(col)
        
        self.feature_columns = potential_features
        
        # Fill missing values with 0 for numeric features
        for col in self.feature_columns:
            df_clean[col] = df_clean[col].fillna(0)
        
        print(f"Preprocessed data shape: {df_clean.shape}")
        print(f"Feature columns: {self.feature_columns}")
        
        return df_clean
    
    def calculate_soil_fertility_index(self, features):
        """Calculate Soil Fertility Index based on key parameters"""
        # Extract key fertility parameters
        ph = features.get('Soil Properties.4', 7.0)  # pH
        oc = features.get('Soil Properties.5', 0.5)  # Organic Carbon
        om = features.get('Soil Properties.6', 1.0)  # Organic Matter
        n = features.get('Soil Properties.7', 0.05)  # Nitrogen
        p = features.get('Soil Properties.8', 5.0)   # Phosphorus
        k = features.get('Soil Properties.9', 0.5)   # Potassium
        ca = features.get('Soil Properties.10', 1.0) # Calcium
        mg = features.get('Soil Properties.11', 0.5) # Magnesium
        ecec = features.get('Soil Properties.12', 2.0) # ECEC
        
        # Normalize values to 0-100 scale
        ph_score = max(0, 100 - abs(ph - 6.5) * 20)  # Optimal pH around 6.5
        oc_score = min(100, oc * 100)  # Higher OC is better
        om_score = min(100, om * 50)   # Higher OM is better
        n_score = min(100, n * 1000)   # Higher N is better
        p_score = min(100, p * 10)     # Higher P is better
        k_score = min(100, k * 100)    # Higher K is better
        ca_score = min(100, ca * 50)   # Higher Ca is better
        mg_score = min(100, mg * 100)  # Higher Mg is better
        ecec_score = min(100, ecec * 25)  # Higher ECEC is better
        
        # Calculate weighted average
        weights = [0.15, 0.15, 0.15, 0.15, 0.10, 0.10, 0.05, 0.05, 0.10]
        scores = [ph_score, oc_score, om_score, n_score, p_score, k_score, ca_score, mg_score, ecec_score]
        
        sfi = sum(w * s for w, s in zip(weights, scores))
        
        return sfi
    
    def get_fertility_category(self, sfi):
        """Categorize soil fertility based on SFI score"""
        if sfi >= 80:
            return "Excellent", "green"
        elif sfi >= 60:
            return "Good", "blue"
        elif sfi >= 40:
            return "Average", "orange"
        else:
            return "Below Average", "red"
    
    def get_recommendations(self, features, sfi, category):
        """Generate comprehensive soil management recommendations based on fertility parameters"""
        recommendations = []
        
        ph = features.get('Soil Properties.4', 7.0)
        oc = features.get('Soil Properties.5', 0.5)
        om = features.get('Soil Properties.6', 1.0)
        n = features.get('Soil Properties.7', 0.05)
        p = features.get('Soil Properties.8', 5.0)
        k = features.get('Soil Properties.9', 0.5)
        ca = features.get('Soil Properties.10', 1.0)
        mg = features.get('Soil Properties.11', 0.5)
        ecec = features.get('Soil Properties.12', 2.0)
        
        # pH recommendations
        if ph < 5.5:
            recommendations.append("Apply agricultural lime (2-4 tons/acre) to raise soil pH to optimal range (6.0-7.0)")
            recommendations.append("Consider dolomitic lime if magnesium levels are also low")
        elif ph > 7.5:
            recommendations.append("Apply elemental sulfur (1-2 tons/acre) to lower soil pH gradually")
            recommendations.append("Use acidifying fertilizers like ammonium sulfate")
        
        # Organic matter recommendations
        if oc < 1.0 or om < 2.0:
            recommendations.append("Increase organic matter through composting (5-10 tons/acre annually)")
            recommendations.append("Implement green manure crops (clover, vetch, rye)")
            recommendations.append("Use cover crops during fallow periods")
        
        # Nitrogen recommendations
        if n < 0.1:
            recommendations.append("Apply nitrogen fertilizers (80-120 lbs N/acre) or legume cover crops")
            recommendations.append("Consider split applications for better efficiency")
            recommendations.append("Use slow-release nitrogen sources")
        
        # Phosphorus recommendations
        if p < 10:
            recommendations.append("Apply phosphorus fertilizers (40-80 lbs P2O5/acre) or bone meal")
            recommendations.append("Consider band placement for better root access")
            recommendations.append("Test soil annually to monitor phosphorus levels")
        
        # Potassium recommendations
        if k < 0.5:
            recommendations.append("Apply potassium fertilizers (60-120 lbs K2O/acre) or wood ash")
            recommendations.append("Consider potassium sulfate for sulfur-deficient soils")
            recommendations.append("Monitor potassium levels in high-yielding crops")
        
        # Calcium and Magnesium recommendations
        if ca < 1.0:
            recommendations.append("Apply gypsum (1-2 tons/acre) for calcium without affecting pH")
            recommendations.append("Consider calcium nitrate for immediate availability")
        
        if mg < 0.5:
            recommendations.append("Apply dolomitic lime or Epsom salts (magnesium sulfate)")
            recommendations.append("Ensure proper calcium-magnesium balance (ideal ratio 6:1)")
        
        # ECEC recommendations
        if ecec < 2.0:
            recommendations.append("Focus on increasing organic matter to improve cation exchange capacity")
            recommendations.append("Consider clay amendments for sandy soils")
            recommendations.append("Implement conservation tillage practices")
        
        # Category-specific recommendations
        if category == "Below Average":
            recommendations.append("Implement comprehensive soil improvement program over 3-5 years")
            recommendations.append("Consider crop rotation with legumes (soybeans, alfalfa, clover)")
            recommendations.append("Implement no-till or reduced-till practices")
            recommendations.append("Establish permanent vegetative cover where possible")
        elif category == "Average":
            recommendations.append("Maintain current practices and gradually improve soil health")
            recommendations.append("Increase organic matter by 0.5-1% over 3 years")
            recommendations.append("Implement crop rotation with at least 25% legumes")
        elif category == "Good":
            recommendations.append("Maintain soil health through sustainable practices")
            recommendations.append("Continue organic matter additions (2-3 tons/acre annually)")
            recommendations.append("Monitor soil health indicators regularly")
        elif category == "Excellent":
            recommendations.append("Maintain current excellent soil conditions")
            recommendations.append("Continue sustainable farming practices")
            recommendations.append("Document successful practices for knowledge sharing")
        
        # General best practices
        recommendations.append("Implement soil conservation practices (contour farming, terracing)")
        recommendations.append("Use integrated pest management to reduce chemical inputs")
        recommendations.append("Monitor soil health indicators annually")
        recommendations.append("Consider precision agriculture technologies for optimal input management")
        
        return recommendations
    
    def train_model(self, df):
        """Train the Random Forest model"""
        # Preprocess data
        df_processed = self.preprocess_data(df)
        
        # Prepare features and target
        X = df_processed[self.feature_columns].values
        y = df_processed.apply(lambda row: self.calculate_soil_fertility_index(
            {col: row[col] for col in self.feature_columns}), axis=1).values
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test_scaled)
        mse = mean_squared_error(y_test, y_pred)
        rmse = mse ** 0.5
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # Derive categories for confusion-matrix style evaluation
        def to_cat(sfi):
            return self.get_fertility_category(sfi)[0]
        y_true_cat = [to_cat(v) for v in y_test]
        y_pred_cat = [to_cat(v) for v in y_pred]
        labels = ["Below Average", "Average", "Good", "Excellent"]
        cm = confusion_matrix(y_true_cat, y_pred_cat, labels=labels)
        acc = accuracy_score(y_true_cat, y_pred_cat)
        precision, recall, f1, _ = precision_recall_fscore_support(y_true_cat, y_pred_cat, labels=labels, zero_division=0, average=None)
        precision_macro, recall_macro, f1_macro, _ = precision_recall_fscore_support(y_true_cat, y_pred_cat, zero_division=0, average='macro')
        
        print(f"Model Performance:")
        print(f"Mean Squared Error: {mse:.2f}")
        print(f"Root MSE: {rmse:.2f}")
        print(f"Mean Absolute Error: {mae:.2f}")
        print(f"R² Score: {r2:.2f}")
        print(f"Classification Accuracy (by category): {acc:.2f}")
        
        self.last_metrics = {
            'mse': float(mse),
            'rmse': float(rmse),
            'mae': float(mae),
            'r2': float(r2),
            'classification': {
                'labels': labels,
                'confusion_matrix': cm.tolist(),
                'accuracy': float(acc),
                'precision_per_class': [float(x) for x in precision],
                'recall_per_class': [float(x) for x in recall],
                'f1_per_class': [float(x) for x in f1],
                'precision_macro': float(precision_macro),
                'recall_macro': float(recall_macro),
                'f1_macro': float(f1_macro)
            }
        }
        
        return df_processed

    def evaluate_full(self, df, n_splits: int = 5):
        """Use all data for training/evaluation via K-Fold CV; fit final model on full data.
        Returns metrics including confusion matrix based on category bins.
        """
        df_processed = self.preprocess_data(df)
        X = df_processed[self.feature_columns].values
        y = df_processed.apply(lambda row: self.calculate_soil_fertility_index(
            {col: row[col] for col in self.feature_columns}), axis=1).values

        kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
        y_pred_all = np.zeros_like(y, dtype=float)

        train_acc_per_fold = []
        val_acc_per_fold = []
        for train_idx, val_idx in kf.split(X):
            X_train, X_val = X[train_idx], X[val_idx]
            y_train = y[train_idx]
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_val_scaled = self.scaler.transform(X_val)
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train_scaled, y_train)
            y_pred_all[val_idx] = model.predict(X_val_scaled)

            # per-fold train/val accuracy over categories
            def to_cat(sfi):
                return self.get_fertility_category(sfi)[0]
            y_train_pred = model.predict(X_train_scaled)
            y_train_true_cat = [to_cat(v) for v in y_train]
            y_train_pred_cat = [to_cat(v) for v in y_train_pred]
            y_val_true_cat = [to_cat(v) for v in y[val_idx]]
            y_val_pred_cat = [to_cat(v) for v in y_pred_all[val_idx]]
            train_acc_per_fold.append(float(accuracy_score(y_train_true_cat, y_train_pred_cat)))
            val_acc_per_fold.append(float(accuracy_score(y_val_true_cat, y_val_pred_cat)))

        # Regression metrics (cross-validated predictions vs ground truth)
        mse = mean_squared_error(y, y_pred_all)
        rmse = mse ** 0.5
        mae = mean_absolute_error(y, y_pred_all)
        r2 = r2_score(y, y_pred_all)

        # Classification metrics based on categories
        def to_cat(sfi):
            return self.get_fertility_category(sfi)[0]
        y_true_cat = [to_cat(v) for v in y]
        y_pred_cat = [to_cat(v) for v in y_pred_all]
        labels = ["Below Average", "Average", "Good", "Excellent"]
        cm = confusion_matrix(y_true_cat, y_pred_cat, labels=labels)
        acc = accuracy_score(y_true_cat, y_pred_cat)
        precision, recall, f1, _ = precision_recall_fscore_support(y_true_cat, y_pred_cat, labels=labels, zero_division=0, average=None)
        precision_macro, recall_macro, f1_macro, _ = precision_recall_fscore_support(y_true_cat, y_pred_cat, zero_division=0, average='macro')

        # Hyperparameter fine-tuning on full data (inner CV)
        X_scaled_full = self.scaler.fit_transform(X)
        base_model = RandomForestRegressor(random_state=42)
        param_distributions = {
            'n_estimators': [100, 200, 300, 400],
            'max_depth': [None, 5, 10, 20, 30],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'max_features': ['sqrt', 'log2', None]
        }
        inner_cv = KFold(n_splits=3, shuffle=True, random_state=42)
        search = RandomizedSearchCV(
            estimator=base_model,
            param_distributions=param_distributions,
            n_iter=20,
            cv=inner_cv,
            random_state=42,
            n_jobs=-1,
            scoring='r2',
            verbose=0
        )
        search.fit(X_scaled_full, y)
        best_params = search.best_params_
        best_score = float(search.best_score_)

        # Fit final model with best hyperparameters
        self.model = RandomForestRegressor(random_state=42, **best_params)
        self.model.fit(X_scaled_full, y)

        metrics = {
            'cv_splits': int(n_splits),
            'mse': float(mse),
            'rmse': float(rmse),
            'mae': float(mae),
            'r2': float(r2),
            'accuracy_per_fold': {
                'train': train_acc_per_fold,
                'val': val_acc_per_fold
            },
            'tuning': {
                'best_params': best_params,
                'inner_cv_r2': best_score
            },
            'classification': {
                'labels': labels,
                'confusion_matrix': cm.tolist(),
                'accuracy': float(acc),
                'precision_per_class': [float(x) for x in precision],
                'recall_per_class': [float(x) for x in recall],
                'f1_per_class': [float(x) for x in f1],
                'precision_macro': float(precision_macro),
                'recall_macro': float(recall_macro),
                'f1_macro': float(f1_macro)
            }
        }
        self.last_metrics = metrics
        return metrics
    
    def predict_fertility(self, features_dict):
        """Predict soil fertility for new data"""
        if self.model is None:
            raise ValueError("Model not trained. Call train_model() first.")
        
        # Prepare features
        features = []
        for col in self.feature_columns:
            if col in features_dict:
                features.append(features_dict[col])
            else:
                features.append(0)  # Default value
        
        # Scale features
        features_scaled = self.scaler.transform([features])
        
        # Predict
        sfi_predicted = self.model.predict(features_scaled)[0]
        
        # Calculate actual SFI
        sfi_actual = self.calculate_soil_fertility_index(features_dict)
        
        # Get category and recommendations
        category, color = self.get_fertility_category(sfi_actual)
        recommendations = self.get_recommendations(features_dict, sfi_actual, category)
        
        return {
            'sfi_predicted': sfi_predicted,
            'sfi_actual': sfi_actual,
            'category': category,
            'color': color,
            'recommendations': recommendations
        }
    
    def save_model(self, filepath):
        """Save the trained model"""
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'feature_columns': self.feature_columns
        }
        joblib.dump(model_data, filepath)
    
    def load_model(self, filepath):
        """Load a trained model"""
        model_data = joblib.load(filepath)
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.label_encoders = model_data['label_encoders']
        self.feature_columns = model_data['feature_columns']

def main():
    """Main function to train and test the model"""
    # Load data
    print("Loading soil nutrients data...")
    df = pd.read_excel('soil_nutrients.xlsx')
    
    # Initialize and train model
    print("Training soil fertility model...")
    model = SoilFertilityModel()
    df_processed = model.train_model(df)
    
    # Save model
    print("Saving trained model...")
    model.save_model('soil_fertility_model.pkl')
    
    # Test prediction
    print("\nTesting model with sample data...")
    sample_features = {
        'Soil Properties.1': 90.0,
        'Soil Properties.4': 6.0,
        'Soil Properties.5': 0.5,
        'Soil Properties.6': 0.9,
        'Soil Properties.7': 0.04,
        'Soil Properties.8': 5.0,
        'Soil Properties.9': 0.1,
        'Soil Properties.10': 1.5,
        'Soil Properties.11': 0.8,
        'Soil Properties.12': 3.0
    }
    
    result = model.predict_fertility(sample_features)
    print(f"Sample Prediction Results:")
    print(f"SFI Score: {result['sfi_actual']:.2f}")
    print(f"Category: {result['category']}")
    print(f"Recommendations:")
    for rec in result['recommendations']:
        print(f"  - {rec}")
    
    print("\nModel training completed successfully!")

if __name__ == "__main__":
    main()
