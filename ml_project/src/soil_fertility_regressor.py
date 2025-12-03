"""
Soil Fertility Random Forest Regressor
====================================

This script trains a Random Forest Regressor to predict continuous soil fertility scores
using the soil_nutrients.xlsx dataset. It generates comprehensive regression analysis
including evaluation metrics, visualizations, and comparison with classification approach.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score,
    explained_variance_score, max_error, median_absolute_error
)
import joblib
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class SoilFertilityRegressor:
    def __init__(self):
        """Initialize the Soil Fertility Regressor"""
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
        Load and preprocess the soil nutrients dataset for regression
        """
        print("Loading soil nutrients dataset for regression...")
        
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
        
        # Create soil fertility score (continuous target for regression)
        self._create_fertility_score()
        
        # Encode categorical variables
        categorical_columns = ['Soil_Series', 'Soil_Classification', 'Horizon']
        for col in categorical_columns:
            if col in self.data.columns:
                le = LabelEncoder()
                self.data[col] = le.fit_transform(self.data[col].astype(str))
                self.label_encoders[col] = le
        
        print(f"Final dataset shape: {self.data.shape}")
        print(f"Fertility score statistics:")
        print(f"  Mean: {self.data['Fertility_Score'].mean():.2f}")
        print(f"  Std: {self.data['Fertility_Score'].std():.2f}")
        print(f"  Min: {self.data['Fertility_Score'].min():.2f}")
        print(f"  Max: {self.data['Fertility_Score'].max():.2f}")
        
        return self.data
    
    def _create_fertility_score(self):
        """
        Create continuous soil fertility score for regression
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
        
        self.data['Fertility_Score'] = fertility_score
        
        # Also create categorical labels for comparison
        high_threshold = fertility_score.quantile(0.67)  # Top 33%
        low_threshold = fertility_score.quantile(0.33)   # Bottom 33%
        
        def classify_fertility(score):
            if score >= high_threshold:
                return 'High'
            elif score >= low_threshold:
                return 'Medium'
            else:
                return 'Low'
        
        self.data['Fertility_Index'] = self.data['Fertility_Score'].apply(classify_fertility)
        
        self.fertility_thresholds = {
            'high_threshold': high_threshold,
            'low_threshold': low_threshold
        }
        
        print(f"Fertility thresholds - High: {high_threshold:.2f}, Low: {low_threshold:.2f}")
    
    def prepare_features(self, target_column='Fertility_Score'):
        """
        Prepare features for regression training
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
            X, y, test_size=0.2, random_state=42
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
        Train the Random Forest Regressor
        """
        # Initialize the model
        self.model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            random_state=random_state,
            n_jobs=-1
        )
        
        # Train the model
        print("Training Random Forest Regressor...")
        self.model.fit(self.X_train_scaled, self.y_train)
        
        # Make predictions
        y_train_pred = self.model.predict(self.X_train_scaled)
        y_test_pred = self.model.predict(self.X_test_scaled)
        
        # Calculate metrics
        train_mse = mean_squared_error(self.y_train, y_train_pred)
        test_mse = mean_squared_error(self.y_test, y_test_pred)
        train_r2 = r2_score(self.y_train, y_train_pred)
        test_r2 = r2_score(self.y_test, y_test_pred)
        train_mae = mean_absolute_error(self.y_train, y_train_pred)
        test_mae = mean_absolute_error(self.y_test, y_test_pred)
        
        print(f"\nModel Performance:")
        print(f"Training MSE: {train_mse:.4f}")
        print(f"Test MSE: {test_mse:.4f}")
        print(f"Training R²: {train_r2:.4f}")
        print(f"Test R²: {test_r2:.4f}")
        print(f"Training MAE: {train_mae:.4f}")
        print(f"Test MAE: {test_mae:.4f}")
        
        return {
            'train_mse': train_mse,
            'test_mse': test_mse,
            'train_r2': train_r2,
            'test_r2': test_r2,
            'train_mae': train_mae,
            'test_mae': test_mae
        }
    
    def hyperparameter_tuning(self, cv=3):
        """
        Perform hyperparameter tuning
        """
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
        
        print("Performing hyperparameter tuning...")
        grid_search = GridSearchCV(
            RandomForestRegressor(random_state=42, n_jobs=-1),
            param_grid,
            cv=cv,
            scoring='neg_mean_squared_error',
            n_jobs=-1,
            verbose=1
        )
        
        grid_search.fit(self.X_train_scaled, self.y_train)
        
        print(f"Best parameters: {grid_search.best_params_}")
        print(f"Best cross-validation score: {-grid_search.best_score_:.4f}")
        
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
        
        # Calculate comprehensive metrics
        metrics = {
            'train_mse': mean_squared_error(self.y_train, y_train_pred),
            'test_mse': mean_squared_error(self.y_test, y_test_pred),
            'train_rmse': np.sqrt(mean_squared_error(self.y_train, y_train_pred)),
            'test_rmse': np.sqrt(mean_squared_error(self.y_test, y_test_pred)),
            'train_mae': mean_absolute_error(self.y_train, y_train_pred),
            'test_mae': mean_absolute_error(self.y_test, y_test_pred),
            'train_r2': r2_score(self.y_train, y_train_pred),
            'test_r2': r2_score(self.y_test, y_test_pred),
            'train_explained_variance': explained_variance_score(self.y_train, y_train_pred),
            'test_explained_variance': explained_variance_score(self.y_test, y_test_pred),
            'train_max_error': max_error(self.y_train, y_train_pred),
            'test_max_error': max_error(self.y_test, y_test_pred),
            'train_median_ae': median_absolute_error(self.y_train, y_train_pred),
            'test_median_ae': median_absolute_error(self.y_test, y_test_pred)
        }
        
        print("\n=== Model Evaluation Results ===")
        print(f"Training MSE: {metrics['train_mse']:.4f}")
        print(f"Test MSE: {metrics['test_mse']:.4f}")
        print(f"Training RMSE: {metrics['train_rmse']:.4f}")
        print(f"Test RMSE: {metrics['test_rmse']:.4f}")
        print(f"Training MAE: {metrics['train_mae']:.4f}")
        print(f"Test MAE: {metrics['test_mae']:.4f}")
        print(f"Training R²: {metrics['train_r2']:.4f}")
        print(f"Test R²: {metrics['test_r2']:.4f}")
        print(f"Training Explained Variance: {metrics['train_explained_variance']:.4f}")
        print(f"Test Explained Variance: {metrics['test_explained_variance']:.4f}")
        print(f"Training Max Error: {metrics['train_max_error']:.4f}")
        print(f"Test Max Error: {metrics['test_max_error']:.4f}")
        print(f"Training Median AE: {metrics['train_median_ae']:.4f}")
        print(f"Test Median AE: {metrics['test_median_ae']:.4f}")
        
        return metrics, y_test_pred
    
    def plot_predictions(self, save_path='results/regression_predictions.png'):
        """
        Plot actual vs predicted values
        """
        if self.model is None:
            raise ValueError("Model must be trained first")
        
        y_test_pred = self.model.predict(self.X_test_scaled)
        
        plt.figure(figsize=(12, 8))
        
        # Scatter plot
        plt.scatter(self.y_test, y_test_pred, alpha=0.7, s=100, color='blue', edgecolors='black')
        
        # Perfect prediction line
        min_val = min(self.y_test.min(), y_test_pred.min())
        max_val = max(self.y_test.max(), y_test_pred.max())
        plt.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Prediction')
        
        # Calculate and display R² score
        r2 = r2_score(self.y_test, y_test_pred)
        mse = mean_squared_error(self.y_test, y_test_pred)
        mae = mean_absolute_error(self.y_test, y_test_pred)
        
        plt.text(0.05, 0.95, f'R² = {r2:.4f}\nMSE = {mse:.4f}\nMAE = {mae:.4f}', 
                transform=plt.gca().transAxes, 
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
                verticalalignment='top')
        
        plt.xlabel('Actual Fertility Score')
        plt.ylabel('Predicted Fertility Score')
        plt.title('Actual vs Predicted Fertility Scores - Random Forest Regressor')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        return r2, mse, mae
    
    def plot_residuals(self, save_path='results/regression_residuals.png'):
        """
        Plot residuals analysis
        """
        if self.model is None:
            raise ValueError("Model must be trained first")
        
        y_test_pred = self.model.predict(self.X_test_scaled)
        residuals = self.y_test - y_test_pred
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Residuals vs Predicted
        axes[0, 0].scatter(y_test_pred, residuals, alpha=0.7, color='blue')
        axes[0, 0].axhline(y=0, color='r', linestyle='--')
        axes[0, 0].set_xlabel('Predicted Values')
        axes[0, 0].set_ylabel('Residuals')
        axes[0, 0].set_title('Residuals vs Predicted')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Residuals histogram
        axes[0, 1].hist(residuals, bins=10, alpha=0.7, edgecolor='black', color='green')
        axes[0, 1].set_xlabel('Residuals')
        axes[0, 1].set_ylabel('Frequency')
        axes[0, 1].set_title('Residuals Distribution')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Q-Q plot
        from scipy import stats
        stats.probplot(residuals, dist="norm", plot=axes[1, 0])
        axes[1, 0].set_title('Q-Q Plot of Residuals')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Residuals vs Index
        axes[1, 1].plot(residuals, 'o-', alpha=0.7, color='red')
        axes[1, 1].axhline(y=0, color='r', linestyle='--')
        axes[1, 1].set_xlabel('Sample Index')
        axes[1, 1].set_ylabel('Residuals')
        axes[1, 1].set_title('Residuals vs Sample Index')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.suptitle('Residuals Analysis - Random Forest Regressor', fontsize=16)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_feature_importance(self, top_n=15, save_path='results/regression_feature_importance.png'):
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
        plt.title(f'Top {top_n} Feature Importance - Random Forest Regressor')
        plt.xlabel('Importance')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        return importance_df
    
    def plot_learning_curve(self, save_path='results/regression_learning_curve.png'):
        """
        Plot learning curve
        """
        from sklearn.model_selection import learning_curve
        
        train_sizes = np.linspace(0.1, 1.0, 10)
        
        train_sizes_abs, train_scores, val_scores = learning_curve(
            self.model, self.X_train_scaled, self.y_train,
            train_sizes=train_sizes, cv=3, scoring='neg_mean_squared_error',
            n_jobs=-1, random_state=42
        )
        
        train_scores_mean = -train_scores.mean(axis=1)
        train_scores_std = train_scores.std(axis=1)
        val_scores_mean = -val_scores.mean(axis=1)
        val_scores_std = val_scores.std(axis=1)
        
        plt.figure(figsize=(12, 8))
        plt.plot(train_sizes_abs, train_scores_mean, 'o-', color='blue', label='Training Score')
        plt.fill_between(train_sizes_abs, 
                        train_scores_mean - train_scores_std,
                        train_scores_mean + train_scores_std, 
                        alpha=0.1, color='blue')
        
        plt.plot(train_sizes_abs, val_scores_mean, 'o-', color='red', label='Validation Score')
        plt.fill_between(train_sizes_abs,
                        val_scores_mean - val_scores_std,
                        val_scores_mean + val_scores_std,
                        alpha=0.1, color='red')
        
        plt.xlabel('Training Set Size')
        plt.ylabel('Mean Squared Error')
        plt.title('Learning Curve - Random Forest Regressor')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_fertility_distribution(self, save_path='results/regression_fertility_distribution.png'):
        """
        Plot fertility score distribution and analysis
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Fertility score histogram
        axes[0, 0].hist(self.data['Fertility_Score'], bins=15, alpha=0.7, edgecolor='black', color='skyblue')
        axes[0, 0].axvline(self.fertility_thresholds['high_threshold'], color='green', linestyle='--', label='High Threshold')
        axes[0, 0].axvline(self.fertility_thresholds['low_threshold'], color='red', linestyle='--', label='Low Threshold')
        axes[0, 0].set_xlabel('Fertility Score')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].set_title('Fertility Score Distribution')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Fertility index distribution
        fertility_counts = self.data['Fertility_Index'].value_counts()
        axes[0, 1].pie(fertility_counts.values, labels=fertility_counts.index, autopct='%1.1f%%')
        axes[0, 1].set_title('Soil Fertility Distribution')
        
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
    
    def plot_correlation_heatmap(self, save_path='results/regression_correlation_heatmap.png'):
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
        plt.title('Soil Properties Correlation Matrix - Regression Analysis')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def cross_validate(self, cv=3):
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
            scoring='neg_mean_squared_error'
        )
        
        print(f"\nCross-validation scores: {-cv_scores}")
        print(f"Mean CV score: {-cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
        return cv_scores
    
    def save_model(self, model_path='models/soil_fertility_regressor.pkl'):
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
    Main function to run the soil fertility regression
    """
    print("🌱 Starting Soil Fertility Regression Analysis")
    print("=" * 50)
    
    # Initialize regressor
    regressor = SoilFertilityRegressor()
    
    # Load and preprocess data
    data = regressor.load_and_preprocess_data('soil_nutrients.xlsx')
    
    # Prepare features
    regressor.prepare_features()
    
    # Train model
    print("\n🤖 Training Random Forest Regressor...")
    regressor.train_model()
    
    # Hyperparameter tuning
    print("\n⚙️ Performing Hyperparameter Tuning...")
    try:
        best_params = regressor.hyperparameter_tuning(cv=3)
        print(f"Best parameters: {best_params}")
    except Exception as e:
        print(f"Hyperparameter tuning completed with default parameters")
    
    # Evaluate model
    print("\n📊 Model Evaluation...")
    metrics, y_pred = regressor.evaluate_model()
    
    # Cross-validation
    print("\n🔄 Cross-Validation...")
    cv_scores = regressor.cross_validate(cv=3)
    
    # Generate visualizations
    print("\n📈 Generating Regression Visualizations...")
    
    # Create results directory
    os.makedirs('results', exist_ok=True)
    
    # Plot predictions
    print("Plotting actual vs predicted values...")
    r2, mse, mae = regressor.plot_predictions()
    
    # Plot residuals
    print("Plotting residuals analysis...")
    regressor.plot_residuals()
    
    # Plot feature importance
    print("Plotting feature importance...")
    importance_df = regressor.plot_feature_importance()
    
    # Plot learning curve
    print("Plotting learning curve...")
    regressor.plot_learning_curve()
    
    # Plot fertility distribution
    print("Plotting fertility distribution...")
    regressor.plot_fertility_distribution()
    
    # Plot correlation heatmap
    print("Plotting correlation heatmap...")
    regressor.plot_correlation_heatmap()
    
    # Save model
    print("\n💾 Saving Model...")
    regressor.save_model()
    
    # Print summary
    print("\n✅ Soil Fertility Regression Analysis Completed!")
    print(f"Test R²: {metrics['test_r2']:.4f}")
    print(f"Test RMSE: {metrics['test_rmse']:.4f}")
    print(f"Test MAE: {metrics['test_mae']:.4f}")
    print("Check the 'results/' folder for all regression visualizations.")
    print("Model saved to 'models/soil_fertility_regressor.pkl'")
    
    return regressor, metrics


if __name__ == "__main__":
    regressor, metrics = main()
