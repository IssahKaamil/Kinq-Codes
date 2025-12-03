"""
Data Preprocessing Utilities
===========================

This module provides utilities for data preprocessing including:
- Data cleaning
- Feature engineering
- Data validation
- Data splitting strategies
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer, KNNImputer
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Tuple, Optional, Dict, Any

class DataPreprocessor:
    def __init__(self):
        """Initialize the DataPreprocessor"""
        self.scalers = {}
        self.encoders = {}
        self.imputers = {}
        self.feature_info = {}
        
    def load_data(self, file_path: str, **kwargs) -> pd.DataFrame:
        """
        Load data from various file formats
        
        Args:
            file_path (str): Path to the data file
            **kwargs: Additional arguments for pandas read functions
            
        Returns:
            pd.DataFrame: Loaded dataset
        """
        file_extension = file_path.split('.')[-1].lower()
        
        if file_extension == 'csv':
            data = pd.read_csv(file_path, **kwargs)
        elif file_extension in ['xlsx', 'xls']:
            data = pd.read_excel(file_path, **kwargs)
        elif file_extension == 'json':
            data = pd.read_json(file_path, **kwargs)
        elif file_extension == 'parquet':
            data = pd.read_parquet(file_path, **kwargs)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
            
        print(f"Data loaded successfully! Shape: {data.shape}")
        return data
    
    def explore_data(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Perform exploratory data analysis
        
        Args:
            data (pd.DataFrame): Input dataset
            
        Returns:
            Dict[str, Any]: Summary statistics and information
        """
        info = {
            'shape': data.shape,
            'columns': list(data.columns),
            'dtypes': data.dtypes.to_dict(),
            'missing_values': data.isnull().sum().to_dict(),
            'missing_percentage': (data.isnull().sum() / len(data) * 100).to_dict(),
            'numeric_columns': data.select_dtypes(include=[np.number]).columns.tolist(),
            'categorical_columns': data.select_dtypes(include=['object']).columns.tolist(),
            'duplicate_rows': data.duplicated().sum(),
            'memory_usage': data.memory_usage(deep=True).sum() / 1024**2  # MB
        }
        
        print("=== Data Exploration Summary ===")
        print(f"Shape: {info['shape']}")
        print(f"Memory Usage: {info['memory_usage']:.2f} MB")
        print(f"Duplicate Rows: {info['duplicate_rows']}")
        print(f"Numeric Columns: {len(info['numeric_columns'])}")
        print(f"Categorical Columns: {len(info['categorical_columns'])}")
        
        if info['missing_values']:
            print("\nMissing Values:")
            for col, missing in info['missing_values'].items():
                if missing > 0:
                    print(f"  {col}: {missing} ({info['missing_percentage'][col]:.1f}%)")
        
        return info
    
    def clean_data(self, data: pd.DataFrame, 
                   remove_duplicates: bool = True,
                   handle_outliers: bool = False,
                   outlier_method: str = 'iqr') -> pd.DataFrame:
        """
        Clean the dataset
        
        Args:
            data (pd.DataFrame): Input dataset
            remove_duplicates (bool): Whether to remove duplicate rows
            handle_outliers (bool): Whether to handle outliers
            outlier_method (str): Method for outlier detection ('iqr' or 'zscore')
            
        Returns:
            pd.DataFrame: Cleaned dataset
        """
        cleaned_data = data.copy()
        
        # Remove duplicates
        if remove_duplicates:
            initial_rows = len(cleaned_data)
            cleaned_data = cleaned_data.drop_duplicates()
            removed_duplicates = initial_rows - len(cleaned_data)
            if removed_duplicates > 0:
                print(f"Removed {removed_duplicates} duplicate rows")
        
        # Handle outliers
        if handle_outliers:
            numeric_columns = cleaned_data.select_dtypes(include=[np.number]).columns
            
            for col in numeric_columns:
                if outlier_method == 'iqr':
                    Q1 = cleaned_data[col].quantile(0.25)
                    Q3 = cleaned_data[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    outliers = (cleaned_data[col] < lower_bound) | (cleaned_data[col] > upper_bound)
                    
                elif outlier_method == 'zscore':
                    z_scores = np.abs((cleaned_data[col] - cleaned_data[col].mean()) / cleaned_data[col].std())
                    outliers = z_scores > 3
                
                outlier_count = outliers.sum()
                if outlier_count > 0:
                    print(f"Found {outlier_count} outliers in {col}")
                    # Option 1: Remove outliers
                    # cleaned_data = cleaned_data[~outliers]
                    
                    # Option 2: Cap outliers (more conservative)
                    if outlier_method == 'iqr':
                        cleaned_data.loc[cleaned_data[col] < lower_bound, col] = lower_bound
                        cleaned_data.loc[cleaned_data[col] > upper_bound, col] = upper_bound
                    else:
                        cleaned_data.loc[outliers, col] = cleaned_data[col].median()
        
        print(f"Data cleaning completed. Final shape: {cleaned_data.shape}")
        return cleaned_data
    
    def handle_missing_values(self, data: pd.DataFrame, 
                            strategy: str = 'auto',
                            numeric_strategy: str = 'mean',
                            categorical_strategy: str = 'most_frequent') -> pd.DataFrame:
        """
        Handle missing values in the dataset
        
        Args:
            data (pd.DataFrame): Input dataset
            strategy (str): Overall strategy ('auto', 'drop', 'impute')
            numeric_strategy (str): Strategy for numeric columns ('mean', 'median', 'mode', 'knn')
            categorical_strategy (str): Strategy for categorical columns ('most_frequent', 'constant')
            
        Returns:
            pd.DataFrame: Dataset with missing values handled
        """
        processed_data = data.copy()
        
        if strategy == 'drop':
            processed_data = processed_data.dropna()
            print(f"Dropped rows with missing values. New shape: {processed_data.shape}")
            
        elif strategy == 'impute' or strategy == 'auto':
            numeric_columns = processed_data.select_dtypes(include=[np.number]).columns
            categorical_columns = processed_data.select_dtypes(include=['object']).columns
            
            # Handle numeric columns
            if len(numeric_columns) > 0:
                if numeric_strategy == 'knn':
                    imputer = KNNImputer(n_neighbors=5)
                else:
                    imputer = SimpleImputer(strategy=numeric_strategy)
                
                processed_data[numeric_columns] = imputer.fit_transform(processed_data[numeric_columns])
                self.imputers['numeric'] = imputer
                print(f"Imputed missing values in numeric columns using {numeric_strategy}")
            
            # Handle categorical columns
            if len(categorical_columns) > 0:
                imputer = SimpleImputer(strategy=categorical_strategy)
                processed_data[categorical_columns] = imputer.fit_transform(processed_data[categorical_columns])
                self.imputers['categorical'] = imputer
                print(f"Imputed missing values in categorical columns using {categorical_strategy}")
        
        return processed_data
    
    def encode_categorical_features(self, data: pd.DataFrame, 
                                  method: str = 'label',
                                  columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Encode categorical features
        
        Args:
            data (pd.DataFrame): Input dataset
            method (str): Encoding method ('label', 'onehot')
            columns (List[str]): Specific columns to encode (if None, encodes all categorical)
            
        Returns:
            pd.DataFrame: Dataset with encoded categorical features
        """
        processed_data = data.copy()
        
        if columns is None:
            categorical_columns = processed_data.select_dtypes(include=['object']).columns
        else:
            categorical_columns = columns
        
        if method == 'label':
            for col in categorical_columns:
                le = LabelEncoder()
                processed_data[col] = le.fit_transform(processed_data[col].astype(str))
                self.encoders[col] = le
                print(f"Label encoded {col}")
                
        elif method == 'onehot':
            for col in categorical_columns:
                ohe = OneHotEncoder(sparse_output=False, drop='first')
                encoded_features = ohe.fit_transform(processed_data[[col]])
                feature_names = [f"{col}_{cat}" for cat in ohe.categories_[0][1:]]
                
                # Create DataFrame with encoded features
                encoded_df = pd.DataFrame(encoded_features, columns=feature_names, index=processed_data.index)
                
                # Drop original column and add encoded features
                processed_data = processed_data.drop(columns=[col])
                processed_data = pd.concat([processed_data, encoded_df], axis=1)
                
                self.encoders[col] = ohe
                print(f"One-hot encoded {col} into {len(feature_names)} features")
        
        return processed_data
    
    def scale_features(self, data: pd.DataFrame, 
                      method: str = 'standard',
                      columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Scale numerical features
        
        Args:
            data (pd.DataFrame): Input dataset
            method (str): Scaling method ('standard', 'minmax', 'robust')
            columns (List[str]): Specific columns to scale (if None, scales all numeric)
            
        Returns:
            pd.DataFrame: Dataset with scaled features
        """
        processed_data = data.copy()
        
        if columns is None:
            numeric_columns = processed_data.select_dtypes(include=[np.number]).columns
        else:
            numeric_columns = columns
        
        if method == 'standard':
            scaler = StandardScaler()
        elif method == 'minmax':
            scaler = MinMaxScaler()
        elif method == 'robust':
            scaler = RobustScaler()
        else:
            raise ValueError(f"Unknown scaling method: {method}")
        
        processed_data[numeric_columns] = scaler.fit_transform(processed_data[numeric_columns])
        self.scalers[method] = scaler
        print(f"Scaled {len(numeric_columns)} features using {method} scaling")
        
        return processed_data
    
    def create_features(self, data: pd.DataFrame, 
                       feature_engineering_config: Dict[str, Any]) -> pd.DataFrame:
        """
        Create new features through feature engineering
        
        Args:
            data (pd.DataFrame): Input dataset
            feature_engineering_config (Dict): Configuration for feature engineering
            
        Returns:
            pd.DataFrame: Dataset with new features
        """
        processed_data = data.copy()
        
        # Polynomial features
        if 'polynomial_features' in feature_engineering_config:
            from sklearn.preprocessing import PolynomialFeatures
            
            poly_config = feature_engineering_config['polynomial_features']
            columns = poly_config.get('columns', [])
            degree = poly_config.get('degree', 2)
            
            if columns:
                poly = PolynomialFeatures(degree=degree, include_bias=False)
                poly_features = poly.fit_transform(processed_data[columns])
                feature_names = poly.get_feature_names_out(columns)
                
                poly_df = pd.DataFrame(poly_features, columns=feature_names, index=processed_data.index)
                processed_data = pd.concat([processed_data, poly_df], axis=1)
                print(f"Created polynomial features for {columns} with degree {degree}")
        
        # Interaction features
        if 'interaction_features' in feature_engineering_config:
            interactions = feature_engineering_config['interaction_features']
            for feature1, feature2 in interactions:
                if feature1 in processed_data.columns and feature2 in processed_data.columns:
                    processed_data[f"{feature1}_x_{feature2}"] = (
                        processed_data[feature1] * processed_data[feature2]
                    )
                    print(f"Created interaction feature: {feature1}_x_{feature2}")
        
        # Custom transformations
        if 'custom_transformations' in feature_engineering_config:
            transformations = feature_engineering_config['custom_transformations']
            for new_feature, expression in transformations.items():
                try:
                    processed_data[new_feature] = processed_data.eval(expression)
                    print(f"Created custom feature: {new_feature}")
                except Exception as e:
                    print(f"Failed to create feature {new_feature}: {e}")
        
        return processed_data
    
    def split_data(self, data: pd.DataFrame, 
                  target_column: str,
                  test_size: float = 0.2,
                  val_size: float = 0.1,
                  random_state: int = 42,
                  stratify: Optional[str] = None) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.Series]:
        """
        Split data into train, validation, and test sets
        
        Args:
            data (pd.DataFrame): Input dataset
            target_column (str): Name of the target column
            test_size (float): Proportion of data for test set
            val_size (float): Proportion of data for validation set
            random_state (int): Random state for reproducibility
            stratify (str): Column to stratify on (for classification tasks)
            
        Returns:
            Tuple: (X_train, X_val, X_test, y_train, y_val, y_test)
        """
        X = data.drop(columns=[target_column])
        y = data[target_column]
        
        # First split: train+val vs test
        X_temp, X_test, y_temp, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=stratify
        )
        
        # Second split: train vs val
        val_size_adjusted = val_size / (1 - test_size)
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp, test_size=val_size_adjusted, random_state=random_state, stratify=stratify
        )
        
        print(f"Data split completed:")
        print(f"  Training set: {X_train.shape[0]} samples")
        print(f"  Validation set: {X_val.shape[0]} samples")
        print(f"  Test set: {X_test.shape[0]} samples")
        
        return X_train, X_val, X_test, y_train, y_val, y_test
    
    def plot_data_distribution(self, data: pd.DataFrame, 
                              columns: Optional[List[str]] = None,
                              figsize: Tuple[int, int] = (15, 10)) -> None:
        """
        Plot distribution of data
        
        Args:
            data (pd.DataFrame): Input dataset
            columns (List[str]): Columns to plot (if None, plots all numeric columns)
            figsize (Tuple): Figure size
        """
        if columns is None:
            numeric_columns = data.select_dtypes(include=[np.number]).columns
        else:
            numeric_columns = columns
        
        n_cols = min(3, len(numeric_columns))
        n_rows = (len(numeric_columns) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
        if n_rows == 1:
            axes = [axes] if n_cols == 1 else axes
        else:
            axes = axes.flatten()
        
        for i, col in enumerate(numeric_columns):
            if i < len(axes):
                axes[i].hist(data[col].dropna(), bins=30, alpha=0.7, edgecolor='black')
                axes[i].set_title(f'Distribution of {col}')
                axes[i].set_xlabel(col)
                axes[i].set_ylabel('Frequency')
        
        # Hide empty subplots
        for i in range(len(numeric_columns), len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        plt.show()
    
    def plot_correlation_matrix(self, data: pd.DataFrame, 
                               figsize: Tuple[int, int] = (12, 10)) -> None:
        """
        Plot correlation matrix
        
        Args:
            data (pd.DataFrame): Input dataset
            figsize (Tuple): Figure size
        """
        numeric_data = data.select_dtypes(include=[np.number])
        
        plt.figure(figsize=figsize)
        correlation_matrix = numeric_data.corr()
        
        sns.heatmap(correlation_matrix, 
                   annot=True, 
                   cmap='coolwarm', 
                   center=0,
                   square=True,
                   fmt='.2f')
        
        plt.title('Correlation Matrix')
        plt.tight_layout()
        plt.show()


def main():
    """
    Example usage of the DataPreprocessor
    """
    preprocessor = DataPreprocessor()
    
    # Example workflow:
    # data = preprocessor.load_data('data/your_dataset.csv')
    # info = preprocessor.explore_data(data)
    # cleaned_data = preprocessor.clean_data(data)
    # processed_data = preprocessor.handle_missing_values(cleaned_data)
    # encoded_data = preprocessor.encode_categorical_features(processed_data)
    # scaled_data = preprocessor.scale_features(encoded_data)
    # X_train, X_val, X_test, y_train, y_val, y_test = preprocessor.split_data(scaled_data, 'target_column')
    
    print("DataPreprocessor initialized. Ready to process your dataset!")


if __name__ == "__main__":
    main()
