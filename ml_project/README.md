# Machine Learning Project - Random Forest Regressor

This project provides a comprehensive framework for training and evaluating Random Forest Regressor models with your dataset.

## Project Structure

```
ml_project/
├── data/                   # Dataset files
├── models/                 # Trained model files
├── notebooks/              # Jupyter notebooks for analysis
├── src/                    # Source code
│   ├── train_model.py      # Main training script
│   ├── data_preprocessing.py # Data preprocessing utilities
│   └── model_evaluation.py  # Model evaluation tools
├── results/                # Results and visualizations
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Features

### 🚀 **Random Forest Regressor Training**
- Complete training pipeline with hyperparameter tuning
- Cross-validation and model evaluation
- Feature importance analysis
- Model persistence (save/load)

### 📊 **Data Preprocessing**
- Data loading from multiple formats (CSV, Excel, JSON, Parquet)
- Missing value handling (imputation, dropping)
- Categorical encoding (label, one-hot)
- Feature scaling (standard, min-max, robust)
- Outlier detection and handling
- Feature engineering capabilities

### 📈 **Model Evaluation**
- Comprehensive performance metrics
- Visualization tools (predictions, residuals, learning curves)
- Model comparison utilities
- Cross-validation analysis
- Automated report generation

## Installation

1. **Clone or download this project**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start

### 1. Prepare Your Dataset

Place your dataset in the `data/` folder. Supported formats:
- CSV files (`.csv`)
- Excel files (`.xlsx`, `.xls`)
- JSON files (`.json`)
- Parquet files (`.parquet`)

### 2. Basic Usage

```python
from src.train_model import RandomForestTrainer

# Initialize trainer
trainer = RandomForestTrainer()

# Load your dataset
trainer.load_data('data/your_dataset.csv')

# Preprocess data (specify your target column)
trainer.preprocess_data(target_column='your_target_column')

# Train the model
trainer.train_model()

# Evaluate and visualize
trainer.plot_feature_importance()
trainer.plot_predictions()

# Save the trained model
trainer.save_model('models/my_model.pkl')
```

### 3. Advanced Usage with Preprocessing

```python
from src.data_preprocessing import DataPreprocessor
from src.train_model import RandomForestTrainer

# Initialize preprocessor
preprocessor = DataPreprocessor()

# Load and explore data
data = preprocessor.load_data('data/your_dataset.csv')
info = preprocessor.explore_data(data)

# Clean and preprocess
cleaned_data = preprocessor.clean_data(data, handle_outliers=True)
processed_data = preprocessor.handle_missing_values(cleaned_data)
encoded_data = preprocessor.encode_categorical_features(processed_data)
scaled_data = preprocessor.scale_features(encoded_data)

# Split data
X_train, X_val, X_test, y_train, y_val, y_test = preprocessor.split_data(
    scaled_data, target_column='your_target_column'
)

# Train model
trainer = RandomForestTrainer()
trainer.X_train = X_train
trainer.X_test = X_test
trainer.y_train = y_train
trainer.y_test = y_test
trainer.feature_columns = X_train.columns.tolist()

trainer.train_model()
```

### 4. Hyperparameter Tuning

```python
# Perform hyperparameter tuning
best_params = trainer.hyperparameter_tuning()

# Train with best parameters
trainer.train_model(**best_params)
```

### 5. Model Evaluation

```python
from src.model_evaluation import ModelEvaluator

# Initialize evaluator
evaluator = ModelEvaluator()

# Calculate metrics
y_pred = trainer.model.predict(trainer.X_test_scaled)
metrics = evaluator.calculate_metrics(trainer.y_test, y_pred, "Random Forest")

# Generate visualizations
evaluator.plot_predictions(trainer.y_test, y_pred, "Random Forest")
evaluator.plot_residuals(trainer.y_test, y_pred, "Random Forest")
evaluator.plot_feature_importance(trainer.model, trainer.feature_columns)

# Generate report
report = evaluator.generate_report("Random Forest", "results/evaluation_report.md")
```

## Configuration Options

### Training Parameters
- `n_estimators`: Number of trees (default: 100)
- `max_depth`: Maximum tree depth (default: None)
- `min_samples_split`: Minimum samples to split (default: 2)
- `min_samples_leaf`: Minimum samples per leaf (default: 1)
- `random_state`: Random seed (default: 42)

### Preprocessing Options
- Missing value strategies: 'auto', 'drop', 'impute'
- Encoding methods: 'label', 'onehot'
- Scaling methods: 'standard', 'minmax', 'robust'
- Outlier handling: 'iqr', 'zscore'

## Example Datasets

The framework works with any regression dataset. Common examples:
- **Housing prices** (features: size, location, age, etc.)
- **Sales forecasting** (features: marketing spend, season, etc.)
- **Stock prices** (features: volume, indicators, etc.)
- **Temperature prediction** (features: humidity, pressure, etc.)

## Output Files

After training, you'll find:
- **Trained model**: `models/random_forest_model.pkl`
- **Feature importance plot**: `results/feature_importance.png`
- **Predictions plot**: `results/predictions.png`
- **Evaluation report**: `results/evaluation_report.md`

## Tips for Better Results

1. **Data Quality**: Ensure your dataset is clean and well-preprocessed
2. **Feature Engineering**: Create meaningful features from your raw data
3. **Hyperparameter Tuning**: Use the built-in tuning to find optimal parameters
4. **Cross-Validation**: Always validate your model with cross-validation
5. **Feature Selection**: Use feature importance to identify the most relevant features

## Troubleshooting

### Common Issues

1. **Memory Error**: Reduce dataset size or use fewer trees
2. **Poor Performance**: Try feature engineering or different preprocessing
3. **Convergence Issues**: Adjust hyperparameters or check data quality

### Getting Help

- Check the console output for detailed error messages
- Ensure all dependencies are installed correctly
- Verify your dataset format and column names

## Next Steps

1. **Load your dataset** into the `data/` folder
2. **Run the training script** with your specific parameters
3. **Analyze the results** using the evaluation tools
4. **Iterate and improve** your model based on the insights

Happy modeling! 🎯
