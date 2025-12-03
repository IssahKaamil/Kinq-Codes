"""
Model Evaluation and Visualization Tools
=======================================

This module provides comprehensive model evaluation tools including:
- Performance metrics calculation
- Visualization of results
- Model comparison
- Cross-validation analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score,
    explained_variance_score, max_error, median_absolute_error
)
from sklearn.model_selection import cross_val_score, learning_curve, validation_curve
from typing import Dict, List, Tuple, Optional, Any
import joblib
import os

class ModelEvaluator:
    def __init__(self):
        """Initialize the ModelEvaluator"""
        self.results = {}
        self.models = {}
        
    def calculate_metrics(self, y_true: np.ndarray, y_pred: np.ndarray, 
                         model_name: str = "Model") -> Dict[str, float]:
        """
        Calculate comprehensive regression metrics
        
        Args:
            y_true (np.ndarray): True values
            y_pred (np.ndarray): Predicted values
            model_name (str): Name of the model
            
        Returns:
            Dict[str, float]: Dictionary of metrics
        """
        metrics = {
            'MSE': mean_squared_error(y_true, y_pred),
            'RMSE': np.sqrt(mean_squared_error(y_true, y_pred)),
            'MAE': mean_absolute_error(y_true, y_pred),
            'R²': r2_score(y_true, y_pred),
            'Explained Variance': explained_variance_score(y_true, y_pred),
            'Max Error': max_error(y_true, y_pred),
            'Median Absolute Error': median_absolute_error(y_true, y_pred),
            'Mean Absolute Percentage Error': np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        }
        
        self.results[model_name] = metrics
        
        print(f"\n=== {model_name} Performance Metrics ===")
        for metric, value in metrics.items():
            print(f"{metric}: {value:.4f}")
            
        return metrics
    
    def compare_models(self, models_results: Dict[str, Dict[str, float]], 
                      metric: str = 'R²') -> pd.DataFrame:
        """
        Compare multiple models based on a specific metric
        
        Args:
            models_results (Dict): Dictionary of model results
            metric (str): Metric to compare on
            
        Returns:
            pd.DataFrame: Comparison table
        """
        comparison_data = []
        
        for model_name, results in models_results.items():
            comparison_data.append({
                'Model': model_name,
                'MSE': results.get('MSE', 0),
                'RMSE': results.get('RMSE', 0),
                'MAE': results.get('MAE', 0),
                'R²': results.get('R²', 0),
                'Explained Variance': results.get('Explained Variance', 0)
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        comparison_df = comparison_df.sort_values(metric, ascending=False)
        
        print(f"\n=== Model Comparison (sorted by {metric}) ===")
        print(comparison_df.to_string(index=False, float_format='%.4f'))
        
        return comparison_df
    
    def plot_predictions(self, y_true: np.ndarray, y_pred: np.ndarray, 
                        model_name: str = "Model", save_path: Optional[str] = None) -> None:
        """
        Plot actual vs predicted values
        
        Args:
            y_true (np.ndarray): True values
            y_pred (np.ndarray): Predicted values
            model_name (str): Name of the model
            save_path (str): Path to save the plot
        """
        plt.figure(figsize=(10, 8))
        
        # Scatter plot
        plt.scatter(y_true, y_pred, alpha=0.6, s=50)
        
        # Perfect prediction line
        min_val = min(y_true.min(), y_pred.min())
        max_val = max(y_true.max(), y_pred.max())
        plt.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Prediction')
        
        # Calculate and display R²
        r2 = r2_score(y_true, y_pred)
        plt.text(0.05, 0.95, f'R² = {r2:.4f}', transform=plt.gca().transAxes, 
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        plt.xlabel('Actual Values')
        plt.ylabel('Predicted Values')
        plt.title(f'Actual vs Predicted Values - {model_name}')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_residuals(self, y_true: np.ndarray, y_pred: np.ndarray, 
                      model_name: str = "Model", save_path: Optional[str] = None) -> None:
        """
        Plot residuals analysis
        
        Args:
            y_true (np.ndarray): True values
            y_pred (np.ndarray): Predicted values
            model_name (str): Name of the model
            save_path (str): Path to save the plot
        """
        residuals = y_true - y_pred
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Residuals vs Predicted
        axes[0, 0].scatter(y_pred, residuals, alpha=0.6)
        axes[0, 0].axhline(y=0, color='r', linestyle='--')
        axes[0, 0].set_xlabel('Predicted Values')
        axes[0, 0].set_ylabel('Residuals')
        axes[0, 0].set_title('Residuals vs Predicted')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Residuals histogram
        axes[0, 1].hist(residuals, bins=30, alpha=0.7, edgecolor='black')
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
        axes[1, 1].plot(residuals, alpha=0.6)
        axes[1, 1].axhline(y=0, color='r', linestyle='--')
        axes[1, 1].set_xlabel('Index')
        axes[1, 1].set_ylabel('Residuals')
        axes[1, 1].set_title('Residuals vs Index')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.suptitle(f'Residuals Analysis - {model_name}', fontsize=16)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_feature_importance(self, model, feature_names: List[str], 
                               top_n: int = 20, save_path: Optional[str] = None) -> None:
        """
        Plot feature importance
        
        Args:
            model: Trained model with feature_importances_ attribute
            feature_names (List[str]): Names of features
            top_n (int): Number of top features to display
            save_path (str): Path to save the plot
        """
        if not hasattr(model, 'feature_importances_'):
            print("Model does not have feature_importances_ attribute")
            return
        
        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        plt.figure(figsize=(12, 8))
        sns.barplot(data=importance_df.head(top_n), x='importance', y='feature')
        plt.title(f'Top {top_n} Feature Importance')
        plt.xlabel('Importance')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        return importance_df
    
    def plot_learning_curve(self, model, X: np.ndarray, y: np.ndarray, 
                           cv: int = 5, train_sizes: np.ndarray = None,
                           model_name: str = "Model", save_path: Optional[str] = None) -> None:
        """
        Plot learning curve
        
        Args:
            model: Model to evaluate
            X (np.ndarray): Features
            y (np.ndarray): Target
            cv (int): Number of cross-validation folds
            train_sizes (np.ndarray): Training set sizes
            model_name (str): Name of the model
            save_path (str): Path to save the plot
        """
        if train_sizes is None:
            train_sizes = np.linspace(0.1, 1.0, 10)
        
        train_sizes_abs, train_scores, val_scores = learning_curve(
            model, X, y, cv=cv, train_sizes=train_sizes, 
            scoring='neg_mean_squared_error', n_jobs=-1
        )
        
        train_scores_mean = -train_scores.mean(axis=1)
        train_scores_std = train_scores.std(axis=1)
        val_scores_mean = -val_scores.mean(axis=1)
        val_scores_std = val_scores.std(axis=1)
        
        plt.figure(figsize=(10, 6))
        plt.plot(train_sizes_abs, train_scores_mean, 'o-', label='Training Score')
        plt.fill_between(train_sizes_abs, 
                        train_scores_mean - train_scores_std,
                        train_scores_mean + train_scores_std, alpha=0.1)
        
        plt.plot(train_sizes_abs, val_scores_mean, 'o-', label='Validation Score')
        plt.fill_between(train_sizes_abs,
                        val_scores_mean - val_scores_std,
                        val_scores_mean + val_scores_std, alpha=0.1)
        
        plt.xlabel('Training Set Size')
        plt.ylabel('Mean Squared Error')
        plt.title(f'Learning Curve - {model_name}')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_validation_curve(self, model, X: np.ndarray, y: np.ndarray,
                             param_name: str, param_range: np.ndarray,
                             cv: int = 5, model_name: str = "Model", 
                             save_path: Optional[str] = None) -> None:
        """
        Plot validation curve
        
        Args:
            model: Model to evaluate
            X (np.ndarray): Features
            y (np.ndarray): Target
            param_name (str): Parameter name to vary
            param_range (np.ndarray): Parameter values to test
            cv (int): Number of cross-validation folds
            model_name (str): Name of the model
            save_path (str): Path to save the plot
        """
        train_scores, val_scores = validation_curve(
            model, X, y, param_name=param_name, param_range=param_range,
            cv=cv, scoring='neg_mean_squared_error', n_jobs=-1
        )
        
        train_scores_mean = -train_scores.mean(axis=1)
        train_scores_std = train_scores.std(axis=1)
        val_scores_mean = -val_scores.mean(axis=1)
        val_scores_std = val_scores.std(axis=1)
        
        plt.figure(figsize=(10, 6))
        plt.plot(param_range, train_scores_mean, 'o-', label='Training Score')
        plt.fill_between(param_range,
                        train_scores_mean - train_scores_std,
                        train_scores_mean + train_scores_std, alpha=0.1)
        
        plt.plot(param_range, val_scores_mean, 'o-', label='Validation Score')
        plt.fill_between(param_range,
                        val_scores_mean - val_scores_std,
                        val_scores_mean + val_scores_std, alpha=0.1)
        
        plt.xlabel(param_name)
        plt.ylabel('Mean Squared Error')
        plt.title(f'Validation Curve - {model_name}')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def cross_validate_model(self, model, X: np.ndarray, y: np.ndarray,
                           cv: int = 5, scoring: str = 'neg_mean_squared_error') -> Dict[str, float]:
        """
        Perform cross-validation
        
        Args:
            model: Model to evaluate
            X (np.ndarray): Features
            y (np.ndarray): Target
            cv (int): Number of cross-validation folds
            scoring (str): Scoring metric
            
        Returns:
            Dict[str, float]: Cross-validation results
        """
        cv_scores = cross_val_score(model, X, y, cv=cv, scoring=scoring, n_jobs=-1)
        
        results = {
            'mean_score': cv_scores.mean(),
            'std_score': cv_scores.std(),
            'scores': cv_scores
        }
        
        print(f"\n=== Cross-Validation Results ===")
        print(f"Mean Score: {results['mean_score']:.4f}")
        print(f"Standard Deviation: {results['std_score']:.4f}")
        print(f"Individual Scores: {cv_scores}")
        
        return results
    
    def generate_report(self, model_name: str, save_path: Optional[str] = None) -> str:
        """
        Generate a comprehensive evaluation report
        
        Args:
            model_name (str): Name of the model
            save_path (str): Path to save the report
            
        Returns:
            str: Report content
        """
        if model_name not in self.results:
            raise ValueError(f"No results found for model: {model_name}")
        
        results = self.results[model_name]
        
        report = f"""
# Model Evaluation Report: {model_name}

## Performance Metrics
- **Mean Squared Error (MSE)**: {results['MSE']:.4f}
- **Root Mean Squared Error (RMSE)**: {results['RMSE']:.4f}
- **Mean Absolute Error (MAE)**: {results['MAE']:.4f}
- **R² Score**: {results['R²']:.4f}
- **Explained Variance**: {results['Explained Variance']:.4f}
- **Max Error**: {results['Max Error']:.4f}
- **Median Absolute Error**: {results['Median Absolute Error']:.4f}
- **Mean Absolute Percentage Error**: {results['Mean Absolute Percentage Error']:.4f}%

## Model Interpretation
- **R² Score**: {results['R²']:.1%} of the variance in the target variable is explained by the model
- **RMSE**: The model's predictions are typically off by {results['RMSE']:.2f} units
- **MAE**: The average absolute error is {results['MAE']:.2f} units

## Recommendations
"""
        
        if results['R²'] > 0.8:
            report += "- Excellent model performance with high explanatory power\n"
        elif results['R²'] > 0.6:
            report += "- Good model performance with moderate explanatory power\n"
        elif results['R²'] > 0.4:
            report += "- Fair model performance, consider feature engineering or hyperparameter tuning\n"
        else:
            report += "- Poor model performance, consider different algorithms or more data\n"
        
        if results['Mean Absolute Percentage Error'] < 10:
            report += "- Low percentage error indicates good prediction accuracy\n"
        elif results['Mean Absolute Percentage Error'] < 20:
            report += "- Moderate percentage error, model is reasonably accurate\n"
        else:
            report += "- High percentage error, model needs improvement\n"
        
        if save_path:
            with open(save_path, 'w') as f:
                f.write(report)
            print(f"Report saved to {save_path}")
        
        return report


def main():
    """
    Example usage of the ModelEvaluator
    """
    evaluator = ModelEvaluator()
    
    # Example workflow:
    # y_true = np.array([1, 2, 3, 4, 5])
    # y_pred = np.array([1.1, 1.9, 3.1, 3.9, 5.1])
    # metrics = evaluator.calculate_metrics(y_true, y_pred, "Example Model")
    # evaluator.plot_predictions(y_true, y_pred, "Example Model")
    # report = evaluator.generate_report("Example Model")
    
    print("ModelEvaluator initialized. Ready to evaluate your models!")


if __name__ == "__main__":
    main()
