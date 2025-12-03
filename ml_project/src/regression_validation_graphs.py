"""
Regression-Specific Validation and Testing Graphs
===============================================

This script generates comprehensive validation and testing graphs specifically for
the Random Forest Regressor, including regression confusion matrix, testing graphs,
and validation analysis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import learning_curve, validation_curve, cross_val_score
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score,
    explained_variance_score, max_error, median_absolute_error
)
import joblib
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class RegressionValidationGraphs:
    def __init__(self, model_path='models/soil_fertility_regressor.pkl'):
        """
        Initialize with trained regressor model
        """
        self.model_path = model_path
        self.model = None
        self.scaler = None
        self.label_encoders = None
        self.feature_columns = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        
    def load_model_and_data(self):
        """
        Load the trained regressor model and prepare data
        """
        # Load model
        model_data = joblib.load(self.model_path)
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.label_encoders = model_data['label_encoders']
        self.feature_columns = model_data['feature_columns']
        
        # Load and preprocess data (same as training)
        from soil_fertility_regressor import SoilFertilityRegressor
        regressor_obj = SoilFertilityRegressor()
        data = regressor_obj.load_and_preprocess_data('soil_nutrients.xlsx')
        regressor_obj.prepare_features()
        
        self.X_train = regressor_obj.X_train
        self.X_test = regressor_obj.X_test
        self.y_train = regressor_obj.y_train
        self.y_test = regressor_obj.y_test
        self.X_train_scaled = regressor_obj.X_train_scaled
        self.X_test_scaled = regressor_obj.X_test_scaled
        
        print(f"Regressor model and data loaded successfully!")
        print(f"Training set: {self.X_train.shape}")
        print(f"Test set: {self.X_test.shape}")
        
    def create_regression_confusion_matrix(self, save_path='results/regression_confusion_matrix.png'):
        """
        Create a regression-specific confusion matrix showing prediction accuracy ranges
        """
        # Make predictions
        y_pred = self.model.predict(self.X_test_scaled)
        
        # Define accuracy ranges (in fertility score points)
        ranges = [0, 5, 10, 15, 20, float('inf')]
        range_labels = ['0-5', '5-10', '10-15', '15-20', '20+']
        
        # Calculate absolute errors
        errors = np.abs(self.y_test - y_pred)
        
        # Create confusion matrix-like structure
        confusion_data = []
        for i, (actual, pred) in enumerate(zip(self.y_test, y_pred)):
            error = abs(actual - pred)
            range_idx = np.digitize(error, ranges) - 1
            range_idx = min(range_idx, len(range_labels) - 1)
            
            confusion_data.append({
                'Sample': i,
                'Actual': actual,
                'Predicted': pred,
                'Error': error,
                'Range': range_labels[range_idx]
            })
        
        confusion_df = pd.DataFrame(confusion_data)
        
        # Create the confusion matrix visualization
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Error range distribution
        range_counts = confusion_df['Range'].value_counts().reindex(range_labels, fill_value=0)
        bars = axes[0, 0].bar(range_labels, range_counts.values, color=['green', 'yellow', 'orange', 'red', 'darkred'])
        axes[0, 0].set_title('Prediction Error Distribution')
        axes[0, 0].set_xlabel('Error Range (Fertility Score Points)')
        axes[0, 0].set_ylabel('Number of Samples')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, count in zip(bars, range_counts.values):
            if count > 0:
                height = bar.get_height()
                axes[0, 0].text(bar.get_x() + bar.get_width()/2., height + 0.05,
                               f'{count}', ha='center', va='bottom')
        
        # 2. Actual vs Predicted with error zones
        axes[0, 1].scatter(self.y_test, y_pred, alpha=0.7, s=100, c=errors, cmap='RdYlGn_r')
        
        # Add error zones
        min_val = min(self.y_test.min(), y_pred.min())
        max_val = max(self.y_test.max(), y_pred.max())
        
        # Perfect prediction line
        axes[0, 1].plot([min_val, max_val], [min_val, max_val], 'k--', lw=2, label='Perfect Prediction')
        
        # Error zones
        axes[0, 1].fill_between([min_val, max_val], [min_val-5, max_val-5], [min_val+5, max_val+5], 
                               alpha=0.2, color='green', label='±5 points')
        axes[0, 1].fill_between([min_val, max_val], [min_val-10, max_val-10], [min_val+10, max_val+10], 
                               alpha=0.2, color='yellow', label='±10 points')
        axes[0, 1].fill_between([min_val, max_val], [min_val-15, max_val-15], [min_val+15, max_val+15], 
                               alpha=0.2, color='orange', label='±15 points')
        
        axes[0, 1].set_xlabel('Actual Fertility Score')
        axes[0, 1].set_ylabel('Predicted Fertility Score')
        axes[0, 1].set_title('Prediction Accuracy Zones')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # Add colorbar
        cbar = plt.colorbar(axes[0, 1].collections[0], ax=axes[0, 1])
        cbar.set_label('Absolute Error')
        
        # 3. Error by actual fertility level
        # Create fertility level bins
        low_mask = self.y_test < 25
        medium_mask = (self.y_test >= 25) & (self.y_test < 35)
        high_mask = self.y_test >= 35
        
        levels = ['Low', 'Medium', 'High']
        masks = [low_mask, medium_mask, high_mask]
        
        errors_by_level = [errors[mask] if np.any(mask) else [] for mask in masks]
        
        # Box plot of errors by fertility level
        box_data = [errors_by_level[i] for i in range(len(levels)) if len(errors_by_level[i]) > 0]
        box_labels = [levels[i] for i in range(len(levels)) if len(errors_by_level[i]) > 0]
        
        if box_data:
            bp = axes[1, 0].boxplot(box_data, labels=box_labels, patch_artist=True)
            colors = ['lightblue', 'lightgreen', 'lightcoral']
            for patch, color in zip(bp['boxes'], colors[:len(bp['boxes'])]):
                patch.set_facecolor(color)
        
        axes[1, 0].set_xlabel('Actual Fertility Level')
        axes[1, 0].set_ylabel('Prediction Error')
        axes[1, 0].set_title('Error Distribution by Fertility Level')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Summary statistics
        stats_text = f"""
        Regression Confusion Matrix Summary:
        
        Total Samples: {len(self.y_test)}
        Mean Error: {errors.mean():.2f} points
        Median Error: {np.median(errors):.2f} points
        Max Error: {errors.max():.2f} points
        Std Error: {errors.std():.2f} points
        
        Accuracy Ranges:
        ±5 points: {np.sum(errors <= 5)} samples ({np.sum(errors <= 5)/len(errors)*100:.1f}%)
        ±10 points: {np.sum(errors <= 10)} samples ({np.sum(errors <= 10)/len(errors)*100:.1f}%)
        ±15 points: {np.sum(errors <= 15)} samples ({np.sum(errors <= 15)/len(errors)*100:.1f}%)
        
        R² Score: {r2_score(self.y_test, y_pred):.3f}
        RMSE: {np.sqrt(mean_squared_error(self.y_test, y_pred)):.2f}
        MAE: {mean_absolute_error(self.y_test, y_pred):.2f}
        """
        
        axes[1, 1].text(0.05, 0.95, stats_text, transform=axes[1, 1].transAxes, fontsize=10,
                        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
        axes[1, 1].set_title('Regression Performance Summary')
        axes[1, 1].axis('off')
        
        plt.suptitle('Regression Confusion Matrix - Prediction Accuracy Analysis', fontsize=16)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        return confusion_df
    
    def plot_comprehensive_testing_graphs(self, save_path='results/regression_testing_graphs.png'):
        """
        Create comprehensive testing and evaluation graphs for regression
        """
        # Make predictions
        y_pred = self.model.predict(self.X_test_scaled)
        residuals = self.y_test - y_pred
        
        fig, axes = plt.subplots(3, 2, figsize=(15, 18))
        
        # 1. Actual vs Predicted with confidence intervals
        axes[0, 0].scatter(self.y_test, y_pred, alpha=0.7, s=100, color='blue', edgecolors='black')
        
        # Perfect prediction line
        min_val = min(self.y_test.min(), y_pred.min())
        max_val = max(self.y_test.max(), y_pred.max())
        axes[0, 0].plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Prediction')
        
        # Confidence intervals
        mse = mean_squared_error(self.y_test, y_pred)
        std_error = np.sqrt(mse)
        
        # 95% confidence interval
        axes[0, 0].fill_between([min_val, max_val], 
                               [min_val - 1.96*std_error, max_val - 1.96*std_error],
                               [min_val + 1.96*std_error, max_val + 1.96*std_error],
                               alpha=0.2, color='gray', label='95% Confidence Interval')
        
        # Calculate and display metrics
        r2 = r2_score(self.y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(self.y_test, y_pred)
        
        axes[0, 0].text(0.05, 0.95, f'R² = {r2:.3f}\nRMSE = {rmse:.2f}\nMAE = {mae:.2f}', 
                       transform=axes[0, 0].transAxes, 
                       bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
                       verticalalignment='top')
        
        axes[0, 0].set_xlabel('Actual Fertility Score')
        axes[0, 0].set_ylabel('Predicted Fertility Score')
        axes[0, 0].set_title('Actual vs Predicted with Confidence Intervals')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Residuals vs Predicted
        axes[0, 1].scatter(y_pred, residuals, alpha=0.7, color='red')
        axes[0, 1].axhline(y=0, color='k', linestyle='--', alpha=0.5)
        axes[0, 1].set_xlabel('Predicted Values')
        axes[0, 1].set_ylabel('Residuals')
        axes[0, 1].set_title('Residuals vs Predicted')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Residuals histogram with normal distribution overlay
        axes[1, 0].hist(residuals, bins=8, alpha=0.7, color='green', edgecolor='black', density=True)
        
        # Overlay normal distribution
        mu, sigma = residuals.mean(), residuals.std()
        x = np.linspace(residuals.min(), residuals.max(), 100)
        normal_dist = (1/(sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)
        axes[1, 0].plot(x, normal_dist, 'r-', linewidth=2, label=f'Normal(μ={mu:.2f}, σ={sigma:.2f})')
        
        axes[1, 0].set_xlabel('Residuals')
        axes[1, 0].set_ylabel('Density')
        axes[1, 0].set_title('Residuals Distribution vs Normal')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Q-Q plot
        from scipy import stats
        stats.probplot(residuals, dist="norm", plot=axes[1, 1])
        axes[1, 1].set_title('Q-Q Plot of Residuals')
        axes[1, 1].grid(True, alpha=0.3)
        
        # 5. Prediction error by sample
        sample_errors = np.abs(residuals)
        axes[2, 0].bar(range(len(sample_errors)), sample_errors, alpha=0.7, color='orange')
        axes[2, 0].axhline(y=sample_errors.mean(), color='red', linestyle='--', 
                          label=f'Mean Error: {sample_errors.mean():.2f}')
        axes[2, 0].set_xlabel('Sample Index')
        axes[2, 0].set_ylabel('Absolute Error')
        axes[2, 0].set_title('Prediction Error by Sample')
        axes[2, 0].legend()
        axes[2, 0].grid(True, alpha=0.3)
        
        # 6. Model performance metrics
        metrics = {
            'R²': r2,
            'RMSE': rmse,
            'MAE': mae,
            'MSE': mse,
            'Max Error': max_error(self.y_test, y_pred),
            'Explained Variance': explained_variance_score(self.y_test, y_pred)
        }
        
        metric_names = list(metrics.keys())
        metric_values = list(metrics.values())
        
        # Normalize values for display
        normalized_values = []
        for name, value in zip(metric_names, metric_values):
            if name == 'R²':
                normalized_values.append(max(0, value))  # R² can be negative
            elif name == 'Explained Variance':
                normalized_values.append(max(0, value))
            else:
                normalized_values.append(min(1, value/50))  # Normalize to 0-1 scale
        
        bars = axes[2, 1].bar(metric_names, normalized_values, color=['blue', 'green', 'orange', 'red', 'purple', 'brown'])
        axes[2, 1].set_title('Model Performance Metrics (Normalized)')
        axes[2, 1].set_ylabel('Normalized Score')
        axes[2, 1].set_ylim(0, 1.1)
        axes[2, 1].grid(True, alpha=0.3)
        
        # Add actual values as text
        for bar, value in zip(bars, metric_values):
            height = bar.get_height()
            axes[2, 1].text(bar.get_x() + bar.get_width()/2., height + 0.01,
                           f'{value:.3f}', ha='center', va='bottom', fontsize=8)
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        return metrics
    
    def plot_validation_graphs(self, save_path='results/regression_validation_graphs.png'):
        """
        Create comprehensive validation graphs for regression
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Learning curve
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
        
        axes[0, 0].plot(train_sizes_abs, train_scores_mean, 'o-', color='blue', label='Training Score')
        axes[0, 0].fill_between(train_sizes_abs, 
                               train_scores_mean - train_scores_std,
                               train_scores_mean + train_scores_std, 
                               alpha=0.1, color='blue')
        
        axes[0, 0].plot(train_sizes_abs, val_scores_mean, 'o-', color='red', label='Validation Score')
        axes[0, 0].fill_between(train_sizes_abs,
                               val_scores_mean - val_scores_std,
                               val_scores_mean + val_scores_std,
                               alpha=0.1, color='red')
        
        axes[0, 0].set_xlabel('Training Set Size')
        axes[0, 0].set_ylabel('Mean Squared Error')
        axes[0, 0].set_title('Learning Curve - Regression')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Validation curve for n_estimators
        param_range = [10, 25, 50, 75, 100, 150, 200]
        
        train_scores, val_scores = validation_curve(
            RandomForestRegressor(random_state=42, n_jobs=-1),
            self.X_train_scaled, self.y_train,
            param_name='n_estimators', param_range=param_range,
            cv=3, scoring='neg_mean_squared_error', n_jobs=-1
        )
        
        train_scores_mean = -train_scores.mean(axis=1)
        train_scores_std = train_scores.std(axis=1)
        val_scores_mean = -val_scores.mean(axis=1)
        val_scores_std = val_scores.std(axis=1)
        
        axes[0, 1].plot(param_range, train_scores_mean, 'o-', color='blue', label='Training Score')
        axes[0, 1].fill_between(param_range,
                               train_scores_mean - train_scores_std,
                               train_scores_mean + train_scores_std,
                               alpha=0.1, color='blue')
        
        axes[0, 1].plot(param_range, val_scores_mean, 'o-', color='red', label='Validation Score')
        axes[0, 1].fill_between(param_range,
                               val_scores_mean - val_scores_std,
                               val_scores_mean + val_scores_std,
                               alpha=0.1, color='red')
        
        # Find best parameter
        best_idx = np.argmin(val_scores_mean)
        best_param = param_range[best_idx]
        best_score = val_scores_mean[best_idx]
        
        axes[0, 1].axvline(x=best_param, color='green', linestyle='--', alpha=0.7)
        axes[0, 1].annotate(f'Best: {best_param}\nMSE: {best_score:.2f}',
                           xy=(best_param, best_score),
                           xytext=(10, 10), textcoords='offset points',
                           bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7),
                           arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        
        axes[0, 1].set_xlabel('Number of Estimators')
        axes[0, 1].set_ylabel('Mean Squared Error')
        axes[0, 1].set_title('Validation Curve - n_estimators')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Cross-validation scores
        cv_scores = cross_val_score(
            self.model, 
            self.X_train_scaled, 
            self.y_train, 
            cv=3, 
            scoring='neg_mean_squared_error'
        )
        
        cv_scores = -cv_scores  # Convert back to positive MSE
        
        axes[1, 0].boxplot(cv_scores, labels=['CV Scores'])
        axes[1, 0].set_ylabel('Mean Squared Error')
        axes[1, 0].set_title('Cross-Validation Scores Distribution')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Add statistics
        stats_text = f"""
        CV Statistics:
        Mean: {cv_scores.mean():.2f}
        Std: {cv_scores.std():.2f}
        Min: {cv_scores.min():.2f}
        Max: {cv_scores.max():.2f}
        """
        axes[1, 0].text(0.02, 0.98, stats_text, transform=axes[1, 0].transAxes, 
                        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
        
        # 4. Feature importance with confidence intervals
        importance = self.model.feature_importances_
        
        # Calculate feature importance variance (if available)
        if hasattr(self.model, 'estimators_'):
            # Calculate std of feature importances across trees
            importances_std = np.std([tree.feature_importances_ for tree in self.model.estimators_], axis=0)
        else:
            importances_std = np.zeros_like(importance)
        
        # Sort by importance
        indices = np.argsort(importance)[::-1]
        
        axes[1, 1].bar(range(len(importance)), importance[indices], 
                      yerr=importances_std[indices], capsize=5, alpha=0.7, color='skyblue')
        axes[1, 1].set_xlabel('Features')
        axes[1, 1].set_ylabel('Importance')
        axes[1, 1].set_title('Feature Importance with Error Bars')
        axes[1, 1].set_xticks(range(len(importance)))
        axes[1, 1].set_xticklabels([self.feature_columns[i] for i in indices], rotation=45, ha='right')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        return cv_scores
    
    def generate_all_regression_validation_graphs(self):
        """
        Generate all regression-specific validation and testing graphs
        """
        print("🔄 Loading regressor model and data...")
        self.load_model_and_data()
        
        print("📊 Generating regression validation and testing graphs...")
        
        # Create results directory
        os.makedirs('results', exist_ok=True)
        
        # Generate all graphs
        print("1. Regression Confusion Matrix...")
        confusion_df = self.create_regression_confusion_matrix()
        
        print("2. Comprehensive Testing Graphs...")
        testing_metrics = self.plot_comprehensive_testing_graphs()
        
        print("3. Validation Graphs...")
        cv_scores = self.plot_validation_graphs()
        
        # Print summary
        print("\n✅ All regression validation and testing graphs generated!")
        print(f"📁 Graphs saved in: results/")
        print(f"🎯 Testing Metrics: {testing_metrics}")
        print(f"🔄 CV Scores Mean: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
        
        return {
            'confusion_df': confusion_df,
            'testing_metrics': testing_metrics,
            'cv_scores': cv_scores
        }


def main():
    """
    Main function to generate all regression validation and testing graphs
    """
    print("📊 Generating Regression Validation and Testing Graphs")
    print("=" * 60)
    
    # Initialize graph generator
    graph_generator = RegressionValidationGraphs()
    
    # Generate all graphs
    results = graph_generator.generate_all_regression_validation_graphs()
    
    print("\n🎉 Regression Validation and Testing Analysis Complete!")
    print("Check the 'results/' folder for all generated graphs.")
    
    return results


if __name__ == "__main__":
    results = main()
