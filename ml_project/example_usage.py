"""
Example Usage Script
===================

This script demonstrates how to use the Random Forest training framework
with a sample dataset. Modify this script to work with your own data.
"""

import pandas as pd
import numpy as np
from src.train_model import RandomForestTrainer
from src.data_preprocessing import DataPreprocessor
from src.model_evaluation import ModelEvaluator

def create_sample_data():
    """
    Create a sample dataset for demonstration purposes.
    Replace this with your actual data loading logic.
    """
    np.random.seed(42)
    n_samples = 1000
    
    # Generate sample features
    data = {
        'feature_1': np.random.normal(100, 15, n_samples),
        'feature_2': np.random.normal(50, 10, n_samples),
        'feature_3': np.random.normal(25, 5, n_samples),
        'category': np.random.choice(['A', 'B', 'C'], n_samples),
        'target': 0  # Will be calculated
    }
    
    # Create target variable with some relationship to features
    data['target'] = (
        2 * data['feature_1'] + 
        1.5 * data['feature_2'] + 
        0.8 * data['feature_3'] + 
        np.random.normal(0, 10, n_samples)
    )
    
    df = pd.DataFrame(data)
    
    # Add some missing values for demonstration
    df.loc[np.random.choice(df.index, 50), 'feature_2'] = np.nan
    df.loc[np.random.choice(df.index, 30), 'category'] = np.nan
    
    return df

def main():
    """
    Main example workflow
    """
    print("🚀 Starting Random Forest Training Example")
    print("=" * 50)
    
    # Step 1: Create or load your dataset
    print("\n📊 Step 1: Loading Dataset")
    data = create_sample_data()
    print(f"Dataset shape: {data.shape}")
    print(f"Columns: {list(data.columns)}")
    
    # Save sample data for future use
    data.to_csv('data/sample_dataset.csv', index=False)
    print("Sample dataset saved to data/sample_dataset.csv")
    
    # Step 2: Data Preprocessing
    print("\n🔧 Step 2: Data Preprocessing")
    preprocessor = DataPreprocessor()
    
    # Explore the data
    info = preprocessor.explore_data(data)
    
    # Clean the data
    cleaned_data = preprocessor.clean_data(data, handle_outliers=True)
    
    # Handle missing values
    processed_data = preprocessor.handle_missing_values(cleaned_data, strategy='impute')
    
    # Encode categorical features
    encoded_data = preprocessor.encode_categorical_features(processed_data, method='label')
    
    # Scale features
    scaled_data = preprocessor.scale_features(encoded_data, method='standard')
    
    # Split the data
    X_train, X_val, X_test, y_train, y_val, y_test = preprocessor.split_data(
        scaled_data, target_column='target', test_size=0.2, val_size=0.1
    )
    
    # Step 3: Model Training
    print("\n🤖 Step 3: Model Training")
    trainer = RandomForestTrainer()
    
    # Set up the data
    trainer.X_train = X_train
    trainer.X_test = X_test
    trainer.y_train = y_train
    trainer.y_test = y_test
    trainer.feature_columns = X_train.columns.tolist()
    trainer.target_column = 'target'
    
    # Train the model
    print("Training Random Forest Regressor...")
    metrics = trainer.train_model(n_estimators=100, random_state=42)
    
    # Step 4: Hyperparameter Tuning (Optional)
    print("\n⚙️ Step 4: Hyperparameter Tuning")
    try:
        best_params = trainer.hyperparameter_tuning(cv=3)  # Reduced CV for speed
        print(f"Best parameters found: {best_params}")
        
        # Retrain with best parameters
        print("Retraining with best parameters...")
        trainer.train_model(**best_params)
    except Exception as e:
        print(f"Hyperparameter tuning skipped: {e}")
    
    # Step 5: Model Evaluation
    print("\n📈 Step 5: Model Evaluation")
    evaluator = ModelEvaluator()
    
    # Make predictions
    y_pred = trainer.model.predict(trainer.X_test_scaled)
    
    # Calculate metrics
    metrics = evaluator.calculate_metrics(trainer.y_test, y_pred, "Random Forest")
    
    # Generate visualizations
    print("Generating visualizations...")
    evaluator.plot_predictions(trainer.y_test, y_pred, "Random Forest")
    evaluator.plot_residuals(trainer.y_test, y_pred, "Random Forest")
    
    # Feature importance
    importance_df = evaluator.plot_feature_importance(
        trainer.model, trainer.feature_columns, top_n=10
    )
    
    # Learning curve
    try:
        evaluator.plot_learning_curve(
            trainer.model, trainer.X_train_scaled, trainer.y_train, 
            cv=3, model_name="Random Forest"
        )
    except Exception as e:
        print(f"Learning curve skipped: {e}")
    
    # Generate report
    report = evaluator.generate_report("Random Forest", "results/evaluation_report.md")
    print("Evaluation report saved to results/evaluation_report.md")
    
    # Step 6: Save Model
    print("\n💾 Step 6: Saving Model")
    trainer.save_model("models/random_forest_model.pkl")
    
    # Step 7: Make Predictions on New Data
    print("\n🔮 Step 7: Making Predictions")
    
    # Create some new data for prediction
    new_data = pd.DataFrame({
        'feature_1': [95, 110, 85],
        'feature_2': [45, 55, 40],
        'feature_3': [20, 30, 15],
        'category': ['A', 'B', 'C']
    })
    
    # Preprocess new data (using the same preprocessing steps)
    new_data_processed = preprocessor.handle_missing_values(new_data, strategy='impute')
    new_data_encoded = preprocessor.encode_categorical_features(new_data_processed, method='label')
    new_data_scaled = preprocessor.scale_features(new_data_encoded, method='standard')
    
    # Make predictions
    predictions = trainer.predict(new_data_scaled)
    
    print("Predictions on new data:")
    for i, pred in enumerate(predictions):
        print(f"Sample {i+1}: {pred:.2f}")
    
    print("\n✅ Example completed successfully!")
    print("Check the 'results/' folder for visualizations and reports.")
    print("Check the 'models/' folder for the saved model.")

if __name__ == "__main__":
    main()
