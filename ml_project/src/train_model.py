"""
Random Forest Regressor Training Script
=====================================

This script trains a Random Forest Regressor model with the provided dataset.
It includes data preprocessing, model training, evaluation, and saving functionality.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
from pathlib import Path

class RandomForestTrainer:
    def __init__(self, data_path=None):
        """
        Initialize the Random Forest Trainer
        
        Args:
            data_path (str): Path to the dataset file
        """
        self.data_path = data_path
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = None
        self.target_column = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        
    def load_data(self, file_path=None):
        """
        Load dataset from file
        
        Args:
            file_path (str): Path to dataset file (CSV, Excel, etc.)
        """
        if file_path:
            self.data_path = file_path
            
        if not self.data_path:
            raise ValueError("No data path provided")
            
        # Determine file type and load accordingly
        file_extension = Path(self.data_path).suffix.lower()
        
        if file_extension == '.csv':
            self.data = pd.read_csv(self.data_path)
        elif file_extension in ['.xlsx', '.xls']:
            self.data = pd.read_excel(self.data_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
            
        print(f"Dataset loaded successfully!")
        print(f"Shape: {self.data.shape}")
        print(f"Columns: {list(self.data.columns)}")
        return self.data
    
    def preprocess_data(self, target_column, feature_columns=None, test_size=0.2, random_state=42):
        """
        Preprocess the data for training
        
        Args:
            target_column (str): Name of the target variable column
            feature_columns (list): List of feature column names (if None, uses all except target)
            test_size (float): Proportion of data for testing
            random_state (int): Random state for reproducibility
        """
        self.target_column = target_column
        self.data = self.data.dropna()  # Remove rows with missing values
        
        # Determine feature columns
        if feature_columns is None:
            self.feature_columns = [col for col in self.data.columns if col != target_column]
        else:
            self.feature_columns = feature_columns
            
        # Separate features and target
        X = self.data[self.feature_columns].copy()
        y = self.data[target_column].copy()
        
        # Handle categorical variables
        for column in X.select_dtypes(include=['object']).columns:
            le = LabelEncoder()
            X[column] = le.fit_transform(X[column].astype(str))
            self.label_encoders[column] = le
            
        # Split the data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        # Scale features (optional for Random Forest, but good practice)
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        
        print(f"Data preprocessing completed!")
        print(f"Training set shape: {self.X_train.shape}")
        print(f"Test set shape: {self.X_test.shape}")
        print(f"Features: {self.feature_columns}")
        
    def train_model(self, n_estimators=100, max_depth=None, min_samples_split=2, 
                   min_samples_leaf=1, random_state=42, use_scaled=True):
        """
        Train the Random Forest Regressor
        
        Args:
            n_estimators (int): Number of trees in the forest
            max_depth (int): Maximum depth of trees
            min_samples_split (int): Minimum samples required to split a node
            min_samples_leaf (int): Minimum samples required at a leaf node
            random_state (int): Random state for reproducibility
            use_scaled (bool): Whether to use scaled features
        """
        # Initialize the model
        self.model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            random_state=random_state,
            n_jobs=-1  # Use all available cores
        )
        
        # Choose data to use
        X_train_data = self.X_train_scaled if use_scaled else self.X_train
        X_test_data = self.X_test_scaled if use_scaled else self.X_test
        
        # Train the model
        print("Training Random Forest Regressor...")
        self.model.fit(X_train_data, self.y_train)
        
        # Make predictions
        y_train_pred = self.model.predict(X_train_data)
        y_test_pred = self.model.predict(X_test_data)
        
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
    
    def hyperparameter_tuning(self, cv=5, n_jobs=-1):
        """
        Perform hyperparameter tuning using GridSearchCV
        
        Args:
            cv (int): Number of cross-validation folds
            n_jobs (int): Number of jobs to run in parallel
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
            n_jobs=n_jobs,
            verbose=1
        )
        
        grid_search.fit(self.X_train_scaled, self.y_train)
        
        print(f"Best parameters: {grid_search.best_params_}")
        print(f"Best cross-validation score: {-grid_search.best_score_:.4f}")
        
        # Update model with best parameters
        self.model = grid_search.best_estimator_
        
        return grid_search.best_params_
    
    def cross_validate(self, cv=5):
        """
        Perform cross-validation
        
        Args:
            cv (int): Number of cross-validation folds
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
        
        print(f"Cross-validation scores: {-cv_scores}")
        print(f"Mean CV score: {-cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
        return cv_scores
    
    def plot_feature_importance(self, top_n=20, save_path=None):
        """
        Plot feature importance
        
        Args:
            top_n (int): Number of top features to display
            save_path (str): Path to save the plot
        """
        if self.model is None:
            raise ValueError("Model must be trained first")
            
        feature_importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        plt.figure(figsize=(10, 8))
        sns.barplot(data=feature_importance.head(top_n), x='importance', y='feature')
        plt.title(f'Top {top_n} Feature Importance')
        plt.xlabel('Importance')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        return feature_importance
    
    def plot_predictions(self, save_path=None):
        """
        Plot actual vs predicted values
        
        Args:
            save_path (str): Path to save the plot
        """
        if self.model is None:
            raise ValueError("Model must be trained first")
            
        y_test_pred = self.model.predict(self.X_test_scaled)
        
        plt.figure(figsize=(10, 8))
        plt.scatter(self.y_test, y_test_pred, alpha=0.6)
        plt.plot([self.y_test.min(), self.y_test.max()], 
                [self.y_test.min(), self.y_test.max()], 'r--', lw=2)
        plt.xlabel('Actual Values')
        plt.ylabel('Predicted Values')
        plt.title('Actual vs Predicted Values')
        
        # Add R² score to plot
        r2 = r2_score(self.y_test, y_test_pred)
        plt.text(0.05, 0.95, f'R² = {r2:.4f}', transform=plt.gca().transAxes, 
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def save_model(self, model_path='models/random_forest_model.pkl'):
        """
        Save the trained model and preprocessing objects
        
        Args:
            model_path (str): Path to save the model
        """
        if self.model is None:
            raise ValueError("Model must be trained first")
            
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        # Save model and preprocessing objects
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'feature_columns': self.feature_columns,
            'target_column': self.target_column
        }
        
        joblib.dump(model_data, model_path)
        print(f"Model saved to {model_path}")
    
    def load_model(self, model_path='models/random_forest_model.pkl'):
        """
        Load a trained model
        
        Args:
            model_path (str): Path to the saved model
        """
        model_data = joblib.load(model_path)
        
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.label_encoders = model_data['label_encoders']
        self.feature_columns = model_data['feature_columns']
        self.target_column = model_data['target_column']
        
        print(f"Model loaded from {model_path}")
    
    def predict(self, X_new):
        """
        Make predictions on new data
        
        Args:
            X_new (pd.DataFrame): New data to make predictions on
            
        Returns:
            np.array: Predictions
        """
        if self.model is None:
            raise ValueError("Model must be trained or loaded first")
            
        # Preprocess new data
        X_processed = X_new[self.feature_columns].copy()
        
        # Handle categorical variables
        for column in X_processed.select_dtypes(include=['object']).columns:
            if column in self.label_encoders:
                X_processed[column] = self.label_encoders[column].transform(
                    X_processed[column].astype(str)
                )
        
        # Scale features
        X_scaled = self.scaler.transform(X_processed)
        
        # Make predictions
        predictions = self.model.predict(X_scaled)
        
        return predictions


def main():
    """
    Example usage of the RandomForestTrainer
    """
    # Initialize trainer
    trainer = RandomForestTrainer()
    
    # Example workflow (uncomment and modify as needed):
    # trainer.load_data('data/your_dataset.csv')
    # trainer.preprocess_data(target_column='your_target_column')
    # trainer.train_model()
    # trainer.hyperparameter_tuning()
    # trainer.plot_feature_importance()
    # trainer.plot_predictions()
    # trainer.save_model()
    
    print("Random Forest Trainer initialized. Ready to load your dataset!")


if __name__ == "__main__":
    main()
