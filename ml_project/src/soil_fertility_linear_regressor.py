"""
Soil Fertility Linear Regressor
==============================

This script mirrors the Random Forest regressor workflow but uses a Linear
Regression model. It loads and preprocesses the same dataset, trains the
model, prints metrics, and generates training/testing/evaluation/validation
graphs and a performance summary. Artifacts are saved under the results/ dir.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, learning_curve, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score,
    explained_variance_score, max_error, median_absolute_error
)
import joblib
import os
import warnings
warnings.filterwarnings('ignore')


class SoilFertilityLinearRegressor:
    def __init__(self):
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
        print("Loading soil nutrients dataset for linear regression...")

        df = pd.read_excel(file_path)
        print(f"Original dataset shape: {df.shape}")

        df = df.iloc[1:].reset_index(drop=True)
        print(f"After removing header: {df.shape}")

        processed_data = []
        for _, row in df.iterrows():
            try:
                soil_series = row['Soil Series']
                soil_classification = row['Soil Classification ']
                horizon = row['Soil Properties']

                properties_1 = str(row['Soil Properties.1']).split()
                if len(properties_1) < 3:
                    continue
                sand = float(properties_1[0])
                silt = float(properties_1[1])
                clay = float(properties_1[2])

                ph = float(row['Soil Properties.3']) if pd.notna(row['Soil Properties.3']) else None
                organic_carbon = float(row['Soil Properties.4']) if pd.notna(row['Soil Properties.4']) else None
                total_nitrogen = float(row['Soil Properties.5']) if pd.notna(row['Soil Properties.5']) else None
                available_phosphorus = float(row['Soil Properties.6']) if pd.notna(row['Soil Properties.6']) else None
                exchangeable_potassium = float(row['Soil Properties.7']) if pd.notna(row['Soil Properties.7']) else None
                cec = float(row['Soil Properties.8']) if pd.notna(row['Soil Properties.8']) else None
                base_saturation = float(row['Soil Properties.12']) if pd.notna(row['Soil Properties.12']) else None

                latitude = row['Latitude'] if pd.notna(row['Latitude']) else None
                longitude = row['Longitude'] if pd.notna(row['Longitude']) else None

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
            except (ValueError, TypeError):
                continue

        self.data = pd.DataFrame(processed_data)
        print(f"Processed dataset shape: {self.data.shape}")
        if len(self.data) == 0:
            raise ValueError("No valid data rows found after processing")

        self._create_fertility_score()

        categorical_columns = ['Soil_Series', 'Soil_Classification', 'Horizon']
        for col in categorical_columns:
            if col in self.data.columns:
                le = LabelEncoder()
                self.data[col] = le.fit_transform(self.data[col].astype(str))
                self.label_encoders[col] = le

        print(f"Final dataset shape: {self.data.shape}")
        print("Fertility score statistics:")
        print(f"  Mean: {self.data['Fertility_Score'].mean():.2f}")
        print(f"  Std: {self.data['Fertility_Score'].std():.2f}")
        print(f"  Min: {self.data['Fertility_Score'].min():.2f}")
        print(f"  Max: {self.data['Fertility_Score'].max():.2f}")
        return self.data

    def _create_fertility_score(self):
        def normalize_feature(series, reverse=False):
            min_val, max_val = series.min(), series.max()
            if reverse:
                normalized = 100 - abs(series - 7) * 20
                normalized = np.clip(normalized, 0, 100)
            else:
                normalized = ((series - min_val) / (max_val - min_val)) * 100
            return normalized

        fertility_score = (
            normalize_feature(self.data['Organic_Carbon']) * 0.25 +
            normalize_feature(self.data['Total_Nitrogen']) * 0.20 +
            normalize_feature(self.data['Available_Phosphorus']) * 0.20 +
            normalize_feature(self.data['Exchangeable_Potassium']) * 0.15 +
            normalize_feature(self.data['pH'], reverse=True) * 0.10 +
            normalize_feature(self.data['CEC']) * 0.10
        )

        self.data['Fertility_Score'] = fertility_score

        high_threshold = fertility_score.quantile(0.67)
        low_threshold = fertility_score.quantile(0.33)

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
        self.target_column = target_column

        feature_columns = [
            'Sand', 'Silt', 'Clay', 'pH', 'Organic_Carbon',
            'Total_Nitrogen', 'Available_Phosphorus', 'Exchangeable_Potassium',
            'CEC', 'Base_Saturation'
        ]
        if 'Soil_Series' in self.data.columns:
            feature_columns.append('Soil_Series')
        if 'Soil_Classification' in self.data.columns:
            feature_columns.append('Soil_Classification')

        self.feature_columns = feature_columns

        X = self.data[feature_columns].copy()
        y = self.data[target_column].copy()

        X = X.fillna(X.median())

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)

        print(f"Training set shape: {self.X_train.shape}")
        print(f"Test set shape: {self.X_test.shape}")
        print(f"Features: {self.feature_columns}")

    def train_model(self):
        self.model = LinearRegression(n_jobs=None)
        print("Training Linear Regression model...")
        self.model.fit(self.X_train_scaled, self.y_train)

        y_train_pred = self.model.predict(self.X_train_scaled)
        y_test_pred = self.model.predict(self.X_test_scaled)

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

    def evaluate_model(self):
        if self.model is None:
            raise ValueError("Model must be trained first")

        y_train_pred = self.model.predict(self.X_train_scaled)
        y_test_pred = self.model.predict(self.X_test_scaled)

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

        print("\n=== Linear Regression Evaluation Results ===")
        for k in metrics:
            if k.startswith('train_') or k.startswith('test_'):
                print(f"{k}: {metrics[k]:.4f}")

        return metrics, y_test_pred

    def plot_train_predictions(self, save_path='results/linear_regression_train_predictions.png'):
        if self.model is None:
            raise ValueError("Model must be trained first")
        y_train_pred = self.model.predict(self.X_train_scaled)

        plt.figure(figsize=(12, 8))
        plt.scatter(self.y_train, y_train_pred, alpha=0.7, s=80, color='teal', edgecolors='black')
        min_val = min(self.y_train.min(), y_train_pred.min())
        max_val = max(self.y_train.max(), y_train_pred.max())
        plt.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Prediction')

        r2 = r2_score(self.y_train, y_train_pred)
        mse = mean_squared_error(self.y_train, y_train_pred)
        mae = mean_absolute_error(self.y_train, y_train_pred)
        plt.text(0.05, 0.95, f'R² = {r2:.4f}\nMSE = {mse:.4f}\nMAE = {mae:.4f}',
                 transform=plt.gca().transAxes,
                 bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
                 verticalalignment='top')
        plt.xlabel('Actual Fertility Score (Train)')
        plt.ylabel('Predicted Fertility Score (Train)')
        plt.title('Training Set: Actual vs Predicted - Linear Regression')
        plt.legend()
        plt.grid(True, alpha=0.3)
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()

    def plot_test_predictions(self, save_path='results/linear_regression_test_predictions.png'):
        if self.model is None:
            raise ValueError("Model must be trained first")
        y_test_pred = self.model.predict(self.X_test_scaled)

        plt.figure(figsize=(12, 8))
        plt.scatter(self.y_test, y_test_pred, alpha=0.7, s=100, color='navy', edgecolors='black')
        min_val = min(self.y_test.min(), y_test_pred.min())
        max_val = max(self.y_test.max(), y_test_pred.max())
        plt.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Prediction')

        r2 = r2_score(self.y_test, y_test_pred)
        mse = mean_squared_error(self.y_test, y_test_pred)
        mae = mean_absolute_error(self.y_test, y_test_pred)
        plt.text(0.05, 0.95, f'R² = {r2:.4f}\nMSE = {mse:.4f}\nMAE = {mae:.4f}',
                 transform=plt.gca().transAxes,
                 bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
                 verticalalignment='top')
        plt.xlabel('Actual Fertility Score (Test)')
        plt.ylabel('Predicted Fertility Score (Test)')
        plt.title('Testing Set: Actual vs Predicted - Linear Regression')
        plt.legend()
        plt.grid(True, alpha=0.3)
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        return r2, mse, mae

    def plot_residuals(self, save_path='results/linear_regression_residuals.png'):
        if self.model is None:
            raise ValueError("Model must be trained first")
        y_test_pred = self.model.predict(self.X_test_scaled)
        residuals = self.y_test - y_test_pred

        fig, axes = plt.subplots(2, 2, figsize=(15, 12))

        axes[0, 0].scatter(y_test_pred, residuals, alpha=0.7, color='blue')
        axes[0, 0].axhline(y=0, color='r', linestyle='--')
        axes[0, 0].set_xlabel('Predicted Values')
        axes[0, 0].set_ylabel('Residuals')
        axes[0, 0].set_title('Residuals vs Predicted')
        axes[0, 0].grid(True, alpha=0.3)

        axes[0, 1].hist(residuals, bins=10, alpha=0.7, edgecolor='black', color='green')
        axes[0, 1].set_xlabel('Residuals')
        axes[0, 1].set_ylabel('Frequency')
        axes[0, 1].set_title('Residuals Distribution')
        axes[0, 1].grid(True, alpha=0.3)

        from scipy import stats
        stats.probplot(residuals, dist="norm", plot=axes[1, 0])
        axes[1, 0].set_title('Q-Q Plot of Residuals')
        axes[1, 0].grid(True, alpha=0.3)

        axes[1, 1].plot(residuals, 'o-', alpha=0.7, color='red')
        axes[1, 1].axhline(y=0, color='r', linestyle='--')
        axes[1, 1].set_xlabel('Sample Index')
        axes[1, 1].set_ylabel('Residuals')
        axes[1, 1].set_title('Residuals vs Sample Index')
        axes[1, 1].grid(True, alpha=0.3)

        plt.suptitle('Residuals Analysis - Linear Regression', fontsize=16)
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()

    def plot_learning_curve(self, save_path='results/linear_regression_learning_curve.png'):
        if self.model is None:
            raise ValueError("Model must be trained first")
        train_sizes = np.linspace(0.1, 1.0, 10)
        train_sizes_abs, train_scores, val_scores = learning_curve(
            self.model, self.X_train_scaled, self.y_train,
            train_sizes=train_sizes, cv=3, scoring='neg_mean_squared_error',
            n_jobs=-1
        )
        train_scores_mean = -train_scores.mean(axis=1)
        train_scores_std = train_scores.std(axis=1)
        val_scores_mean = -val_scores.mean(axis=1)
        val_scores_std = val_scores.std(axis=1)

        plt.figure(figsize=(12, 8))
        plt.plot(train_sizes_abs, train_scores_mean, 'o-', color='blue', label='Training Score')
        plt.fill_between(train_sizes_abs, train_scores_mean - train_scores_std,
                         train_scores_mean + train_scores_std, alpha=0.1, color='blue')
        plt.plot(train_sizes_abs, val_scores_mean, 'o-', color='red', label='Validation Score')
        plt.fill_between(train_sizes_abs, val_scores_mean - val_scores_std,
                         val_scores_mean + val_scores_std, alpha=0.1, color='red')
        plt.xlabel('Training Set Size')
        plt.ylabel('Mean Squared Error')
        plt.title('Learning Curve - Linear Regression')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()

    def cross_validate(self, cv=3):
        if self.model is None:
            raise ValueError("Model must be trained first")
        cv_scores = cross_val_score(
            self.model,
            self.X_train_scaled,
            self.y_train,
            cv=cv,
            scoring='neg_mean_squared_error'
        )
        print(f"\nCross-validation MSE scores: {-cv_scores}")
        print(f"Mean CV MSE: {-cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        return cv_scores

    def plot_performance_bars(self, save_path='results/linear_regression_performance.png'):
        if self.model is None:
            raise ValueError("Model must be trained first")
        from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
        y_pred = self.model.predict(self.X_test_scaled)
        metrics = {
            'R²': r2_score(self.y_test, y_pred),
            'RMSE': np.sqrt(mean_squared_error(self.y_test, y_pred)),
            'MAE': mean_absolute_error(self.y_test, y_pred)
        }
        categories = list(metrics.keys())
        values = list(metrics.values())
        plt.figure(figsize=(10, 7))
        bars = plt.bar(categories, values, color=['royalblue', 'seagreen', 'darkorange'])
        plt.title('Linear Regression Performance (Test)')
        plt.grid(True, alpha=0.3, axis='y')
        for bar, value in zip(bars, values):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + (0.01 if height >= 1 else 0.001),
                     f'{value:.3f}', ha='center', va='bottom')
        os.makedirs('results', exist_ok=True)
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()

    def save_model(self, model_path='models/soil_fertility_linear_regressor.pkl'):
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
    print("🌱 Starting Soil Fertility Linear Regression Analysis")
    print("=" * 50)

    reg = SoilFertilityLinearRegressor()
    reg.load_and_preprocess_data('soil_nutrients.xlsx')
    reg.prepare_features()
    print("\n🤖 Training Linear Regression...")
    reg.train_model()

    print("\n📊 Model Evaluation...")
    metrics, _ = reg.evaluate_model()

    print("\n🔄 Cross-Validation...")
    _ = reg.cross_validate(cv=3)

    print("\n📈 Generating Linear Regression Visualizations...")
    os.makedirs('results', exist_ok=True)
    reg.plot_train_predictions()
    reg.plot_test_predictions()
    reg.plot_residuals()
    reg.plot_learning_curve()
    reg.plot_performance_bars()

    print("\n💾 Saving Model...")
    reg.save_model()

    print("\n✅ Linear Regression Analysis Completed!")
    print(f"Test R²: {metrics['test_r2']:.4f}")
    print(f"Test RMSE: {metrics['test_rmse']:.4f}")
    print(f"Test MAE: {metrics['test_mae']:.4f}")
    print("Check the 'results/' folder for all linear regression visualizations.")
    print("Model saved to 'models/soil_fertility_linear_regressor.pkl'")

    return reg, metrics


if __name__ == "__main__":
    reg, metrics = main()


