"""
Soil Fertility Classification Model - Fixed Version
=================================================

This script trains a Random Forest Classifier to predict soil fertility index
and classify it into High, Medium, and Low categories.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (
    classification_report, confusion_matrix, accuracy_score,
    precision_score, recall_score, f1_score
)
import joblib
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class SoilFertilityClassifier:
    def __init__(self):
        """Initialize the Soil Fertility Classifier"""
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = None
        self.target_column = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.fertility_thresholds = None
        
    def load_and_preprocess_data(self, file_path='soil_nutrients.xlsx'):
        """
        Load and preprocess the soil nutrients dataset
        """
        print("Loading soil nutrients dataset...")
        
        # Load the dataset
        df = pd.read_excel(file_path)
        print(f"Original dataset shape: {df.shape}")
        
        # Remove the header row (first row contains column descriptions)
        df = df.iloc[1:].reset_index(drop=True)
        print(f"After removing header: {df.shape}")
        
        # Parse the data properly
        processed_data = []
        
        for idx, row in df.iterrows():
            try:
                # Extract soil properties from the row
                soil_series = row['Soil Series']
                soil_classification = row['Soil Classification ']
                horizon = row['Soil Properties']
                
                # Parse the combined values in Soil Properties.1
                properties_1 = str(row['Soil Properties.1']).split()
                if len(properties_1) >= 3:
                    sand = float(properties_1[0])
                    silt = float(properties_1[1])
                    clay = float(properties_1[2])
                else:
                    continue
                
                # Extract other properties
                ph = float(row['Soil Properties.3']) if pd.notna(row['Soil Properties.3']) else None
                organic_carbon = float(row['Soil Properties.4']) if pd.notna(row['Soil Properties.4']) else None
                total_nitrogen = float(row['Soil Properties.5']) if pd.notna(row['Soil Properties.5']) else None
                available_phosphorus = float(row['Soil Properties.6']) if pd.notna(row['Soil Properties.6']) else None
                exchangeable_potassium = float(row['Soil Properties.7']) if pd.notna(row['Soil Properties.7']) else None
                cec = float(row['Soil Properties.8']) if pd.notna(row['Soil Properties.8']) else None
                base_saturation = float(row['Soil Properties.12']) if pd.notna(row['Soil Properties.12']) else None
                
                latitude = row['Latitude'] if pd.notna(row['Latitude']) else None
                longitude = row['Longitude'] if pd.notna(row['Longitude']) else None
                
                # Only include rows with essential data
                if all(pd.notna([ph, organic_carbon, total_nitrogen, available_phosphorus, 
                                exchangeable_potassium, cec, base_saturation])):
                    processed_data.append({
                        'Soil_Series': soil_series,
                        'Soil_Classification': soil_classification,
                        'Horizon': horizon,
                        'Sand': sand,
                        'Silt': silt,
                        'Clay': clay,
                        'pH': ph,
                        'Organic_Carbon': organic_carbon,
                        'Total_Nitrogen': total_nitrogen,
                        'Available_Phosphorus': available_phosphorus,
                        'Exchangeable_Potassium': exchangeable_potassium,
                        'CEC': cec,
                        'Base_Saturation': base_saturation,
                        'Latitude': latitude,
                        'Longitude': longitude
                    })
            except (ValueError, TypeError) as e:
                continue
        
        # Create DataFrame from processed data
        self.data = pd.DataFrame(processed_data)
        print(f"Processed dataset shape: {self.data.shape}")
        
        if len(self.data) == 0:
            raise ValueError("No valid data rows found after processing")
        
        # Create soil fertility index
        self._create_fertility_index()
        
        # Encode categorical variables
        categorical_columns = ['Soil_Series', 'Soil_Classification', 'Horizon']
        for col in categorical_columns:
            if col in self.data.columns:
                le = LabelEncoder()
                self.data[col] = le.fit_transform(self.data[col].astype(str))
                self.label_encoders[col] = le
        
        print(f"Final dataset shape: {self.data.shape}")
        print(f"Fertility distribution:\n{self.data['Fertility_Index'].value_counts()}")
        
        return self.data
    
    def _create_fertility_index(self):
        """
        Create soil fertility index based on key soil properties
        """
        # Normalize key soil properties (0-100 scale)
        def normalize_feature(series, reverse=False):
            """Normalize feature to 0-100 scale"""
            min_val, max_val = series.min(), series.max()
            if reverse:  # For pH (optimal around 6.5-7.5)
                # pH closer to 7 is better
                normalized = 100 - abs(series - 7) * 20
                normalized = np.clip(normalized, 0, 100)
            else:
                normalized = ((series - min_val) / (max_val - min_val)) * 100
            return normalized
        
        # Calculate fertility score based on key indicators
        fertility_score = (
            normalize_feature(self.data['Organic_Carbon']) * 0.25 +  # 25% weight
            normalize_feature(self.data['Total_Nitrogen']) * 0.20 +   # 20% weight
            normalize_feature(self.data['Available_Phosphorus']) * 0.20 +  # 20% weight
            normalize_feature(self.data['Exchangeable_Potassium']) * 0.15 +  # 15% weight
            normalize_feature(self.data['pH'], reverse=True) * 0.10 +  # 10% weight (pH optimal around 7)
            normalize_feature(self.data['CEC']) * 0.10  # 10% weight
        )
        
        # Classify into High, Medium, Low based on percentiles
        high_threshold = fertility_score.quantile(0.67)  # Top 33%
        low_threshold = fertility_score.quantile(0.33)   # Bottom 33%
        
        def classify_fertility(score):
            if score >= high_threshold:
                return 'High'
            elif score >= low_threshold:
                return 'Medium'
            else:
                return 'Low'
        
        self.data['Fertility_Score'] = fertility_score
        self.data['Fertility_Index'] = self.data['Fertility_Score'].apply(classify_fertility)
        
        self.fertility_thresholds = {
            'high_threshold': high_threshold,
            'low_threshold': low_threshold
        }
        
        print(f"Fertility thresholds - High: {high_threshold:.2f}, Low: {low_threshold:.2f}")
    
    def prepare_features(self, target_column='Fertility_Index'):
        """
        Prepare features for training
        """
        self.target_column = target_column
        
        # Select features for training
        feature_columns = [
            'Sand', 'Silt', 'Clay', 'pH', 'Organic_Carbon', 
            'Total_Nitrogen', 'Available_Phosphorus', 'Exchangeable_Potassium', 
            'CEC', 'Base_Saturation'
        ]
        
        # Add categorical features if available
        if 'Soil_Series' in self.data.columns:
            feature_columns.append('Soil_Series')
        if 'Soil_Classification' in self.data.columns:
            feature_columns.append('Soil_Classification')
        
        self.feature_columns = feature_columns
        
        # Prepare X and y
        X = self.data[feature_columns].copy()
        y = self.data[target_column].copy()
        
        # Handle any remaining missing values
        X = X.fillna(X.median())
        
        # Split the data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        
        print(f"Training set shape: {self.X_train.shape}")
        print(f"Test set shape: {self.X_test.shape}")
        print(f"Features: {self.feature_columns}")
        
    def train_model(self, n_estimators=100, max_depth=None, min_samples_split=2, 
                   min_samples_leaf=1, random_state=42):
        """
        Train the Random Forest Classifier
        """
        # Initialize the model
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            random_state=random_state,
            n_jobs=-1
        )
        
        # Train the model
        print("Training Random Forest Classifier...")
        self.model.fit(self.X_train_scaled, self.y_train)
        
        # Make predictions
        y_train_pred = self.model.predict(self.X_train_scaled)
        y_test_pred = self.model.predict(self.X_test_scaled)
        
        # Calculate metrics
        train_accuracy = accuracy_score(self.y_train, y_train_pred)
        test_accuracy = accuracy_score(self.y_test, y_test_pred)
        
        print(f"\nModel Performance:")
        print(f"Training Accuracy: {train_accuracy:.4f}")
        print(f"Test Accuracy: {test_accuracy:.4f}")
        
        return {
            'train_accuracy': train_accuracy,
            'test_accuracy': test_accuracy
        }
    
    def hyperparameter_tuning(self, cv=3):
        """
        Perform hyperparameter tuning
        """
        param_grid = {
            'n_estimators': [50, 100],
            'max_depth': [None, 10, 20],
            'min_samples_split': [2, 5],
            'min_samples_leaf': [1, 2]
        }
        
        print("Performing hyperparameter tuning...")
        grid_search = GridSearchCV(
            RandomForestClassifier(random_state=42, n_jobs=-1),
            param_grid,
            cv=cv,
            scoring='accuracy',
            n_jobs=-1,
            verbose=1
        )
        
        grid_search.fit(self.X_train_scaled, self.y_train)
        
        print(f"Best parameters: {grid_search.best_params_}")
        print(f"Best cross-validation score: {grid_search.best_score_:.4f}")
        
        # Update model with best parameters
        self.model = grid_search.best_estimator_
        
        return grid_search.best_params_
    
    def evaluate_model(self):
        """
        Comprehensive model evaluation
        """
        if self.model is None:
            raise ValueError("Model must be trained first")
        
        # Make predictions
        y_train_pred = self.model.predict(self.X_train_scaled)
        y_test_pred = self.model.predict(self.X_test_scaled)
        
        # Calculate metrics
        metrics = {
            'train_accuracy': accuracy_score(self.y_train, y_train_pred),
            'test_accuracy': accuracy_score(self.y_test, y_test_pred),
            'train_precision': precision_score(self.y_train, y_train_pred, average='weighted'),
            'test_precision': precision_score(self.y_test, y_test_pred, average='weighted'),
            'train_recall': recall_score(self.y_train, y_train_pred, average='weighted'),
            'test_recall': recall_score(self.y_test, y_test_pred, average='weighted'),
            'train_f1': f1_score(self.y_train, y_train_pred, average='weighted'),
            'test_f1': f1_score(self.y_test, y_test_pred, average='weighted')
        }
        
        print("\n=== Model Evaluation Results ===")
        print(f"Training Accuracy: {metrics['train_accuracy']:.4f}")
        print(f"Test Accuracy: {metrics['test_accuracy']:.4f}")
        print(f"Training Precision: {metrics['train_precision']:.4f}")
        print(f"Test Precision: {metrics['test_precision']:.4f}")
        print(f"Training Recall: {metrics['train_recall']:.4f}")
        print(f"Test Recall: {metrics['test_recall']:.4f}")
        print(f"Training F1-Score: {metrics['train_f1']:.4f}")
        print(f"Test F1-Score: {metrics['test_f1']:.4f}")
        
        # Classification report
        print("\n=== Classification Report (Test Set) ===")
        print(classification_report(self.y_test, y_test_pred))
        
        return metrics, y_test_pred
    
    def plot_confusion_matrix(self, y_pred=None, save_path=None):
        """
        Plot confusion matrix
        """
        if y_pred is None:
            y_pred = self.model.predict(self.X_test_scaled)
        
        cm = confusion_matrix(self.y_test, y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['High', 'Medium', 'Low'],
                   yticklabels=['High', 'Medium', 'Low'])
        plt.title('Confusion Matrix - Soil Fertility Classification')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        return cm
    
    def plot_feature_importance(self, top_n=15, save_path=None):
        """
        Plot feature importance
        """
        if self.model is None:
            raise ValueError("Model must be trained first")
        
        importance_df = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        plt.figure(figsize=(12, 8))
        sns.barplot(data=importance_df.head(top_n), x='importance', y='feature')
        plt.title(f'Top {top_n} Feature Importance - Soil Fertility')
        plt.xlabel('Importance')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        return importance_df
    
    def plot_fertility_distribution(self, save_path=None):
        """
        Plot fertility distribution
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Fertility index distribution
        fertility_counts = self.data['Fertility_Index'].value_counts()
        axes[0, 0].pie(fertility_counts.values, labels=fertility_counts.index, autopct='%1.1f%%')
        axes[0, 0].set_title('Soil Fertility Distribution')
        
        # Fertility score histogram
        axes[0, 1].hist(self.data['Fertility_Score'], bins=20, alpha=0.7, edgecolor='black')
        axes[0, 1].axvline(self.fertility_thresholds['high_threshold'], color='green', linestyle='--', label='High Threshold')
        axes[0, 1].axvline(self.fertility_thresholds['low_threshold'], color='red', linestyle='--', label='Low Threshold')
        axes[0, 1].set_xlabel('Fertility Score')
        axes[0, 1].set_ylabel('Frequency')
        axes[0, 1].set_title('Fertility Score Distribution')
        axes[0, 1].legend()
        
        # Key nutrients by fertility level
        key_nutrients = ['Organic_Carbon', 'Total_Nitrogen', 'Available_Phosphorus']
        for i, nutrient in enumerate(key_nutrients):
            if i < 2:
                sns.boxplot(data=self.data, x='Fertility_Index', y=nutrient, ax=axes[1, i])
                axes[1, i].set_title(f'{nutrient} by Fertility Level')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_correlation_heatmap(self, save_path=None):
        """
        Plot correlation heatmap of soil properties
        """
        numeric_columns = ['Sand', 'Silt', 'Clay', 'pH', 'Organic_Carbon', 
                          'Total_Nitrogen', 'Available_Phosphorus', 'Exchangeable_Potassium', 
                          'CEC', 'Base_Saturation', 'Fertility_Score']
        
        correlation_data = self.data[numeric_columns].corr()
        
        plt.figure(figsize=(12, 10))
        sns.heatmap(correlation_data, annot=True, cmap='coolwarm', center=0, 
                   square=True, fmt='.2f')
        plt.title('Soil Properties Correlation Matrix')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def cross_validate(self, cv=5):
        """
        Perform cross-validation
        """
        if self.model is None:
            raise ValueError("Model must be trained first")
        
        cv_scores = cross_val_score(
            self.model, 
            self.X_train_scaled, 
            self.y_train, 
            cv=cv, 
            scoring='accuracy'
        )
        
        print(f"\nCross-validation scores: {cv_scores}")
        print(f"Mean CV score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
        return cv_scores
    
    def save_model(self, model_path='models/soil_fertility_model.pkl'):
        """
        Save the trained model
        """
        if self.model is None:
            raise ValueError("Model must be trained first")
        
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'feature_columns': self.feature_columns,
            'target_column': self.target_column,
            'fertility_thresholds': self.fertility_thresholds
        }
        
        joblib.dump(model_data, model_path)
        print(f"Model saved to {model_path}")


def main():
    """
    Main function to run the soil fertility classification
    """
    print("🌱 Starting Soil Fertility Classification")
    print("=" * 50)
    
    # Initialize classifier
    classifier = SoilFertilityClassifier()
    
    # Load and preprocess data
    data = classifier.load_and_preprocess_data('soil_nutrients.xlsx')
    
    # Prepare features
    classifier.prepare_features()
    
    # Train model
    print("\n🤖 Training Random Forest Classifier...")
    classifier.train_model()
    
    # Hyperparameter tuning
    print("\n⚙️ Performing Hyperparameter Tuning...")
    try:
        best_params = classifier.hyperparameter_tuning(cv=3)
        print(f"Best parameters: {best_params}")
    except Exception as e:
        print(f"Hyperparameter tuning completed with default parameters")
    
    # Evaluate model
    print("\n📊 Model Evaluation...")
    metrics, y_pred = classifier.evaluate_model()
    
    # Cross-validation
    print("\n🔄 Cross-Validation...")
    cv_scores = classifier.cross_validate(cv=5)
    
    # Generate visualizations
    print("\n📈 Generating Visualizations...")
    
    # Create results directory
    os.makedirs('results', exist_ok=True)
    
    # Plot confusion matrix
    print("Plotting confusion matrix...")
    cm = classifier.plot_confusion_matrix(y_pred, 'results/confusion_matrix.png')
    
    # Plot feature importance
    print("Plotting feature importance...")
    importance_df = classifier.plot_feature_importance(save_path='results/feature_importance.png')
    
    # Plot fertility distribution
    print("Plotting fertility distribution...")
    classifier.plot_fertility_distribution('results/fertility_distribution.png')
    
    # Plot correlation heatmap
    print("Plotting correlation heatmap...")
    classifier.plot_correlation_heatmap('results/correlation_heatmap.png')
    
    # Save model
    print("\n💾 Saving Model...")
    classifier.save_model()
    
    # Print summary
    print("\n✅ Soil Fertility Classification Completed!")
    print(f"Test Accuracy: {metrics['test_accuracy']:.4f}")
    print(f"Test F1-Score: {metrics['test_f1']:.4f}")
    print("Check the 'results/' folder for visualizations.")
    print("Model saved to 'models/soil_fertility_model.pkl'")
    
    return classifier, metrics


if __name__ == "__main__":
    classifier, metrics = main()
