"""
Combined Comparison: Linear Regression vs Random Forest Regression
=================================================================

Generates side-by-side and combined plots comparing Linear Regression and
Random Forest Regressor on the soil fertility dataset. Produces:
- Combined training graph
- Combined testing graph
- Combined performance summary bars
- Combined evaluation (actual vs predicted overlays)
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import joblib
from sklearn.model_selection import learning_curve


def load_models():
    rf_bundle = joblib.load('models/soil_fertility_regressor.pkl')
    lin_bundle = joblib.load('models/soil_fertility_linear_regressor.pkl')
    return rf_bundle, lin_bundle


def prepare_scaled_features(lin_bundle):
    # Recreate the same data splits as training using the linear module
    from soil_fertility_linear_regressor import SoilFertilityLinearRegressor
    reg = SoilFertilityLinearRegressor()
    reg.load_and_preprocess_data('soil_nutrients.xlsx')
    reg.prepare_features()
    return reg


def combined_training_graph(reg):
    rf_bundle, lin_bundle = load_models()
    rf_model = rf_bundle['model']
    lin_model = lin_bundle['model']

    X_train_scaled = reg.X_train_scaled
    y_train = reg.y_train

    rf_train_pred = rf_model.predict(X_train_scaled)
    lin_train_pred = lin_model.predict(X_train_scaled)

    plt.figure(figsize=(12, 8))
    plt.scatter(y_train, rf_train_pred, alpha=0.6, s=70, label='Random Forest', edgecolors='black')
    plt.scatter(y_train, lin_train_pred, alpha=0.6, s=70, label='Linear Regression', edgecolors='black')
    min_val = min(y_train.min(), rf_train_pred.min(), lin_train_pred.min())
    max_val = max(y_train.max(), rf_train_pred.max(), lin_train_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val], 'k--', lw=2, label='Perfect Prediction')
    plt.xlabel('Actual Fertility Score (Train)')
    plt.ylabel('Predicted Fertility Score (Train)')
    plt.title('Combined Training Graph: Linear vs Random Forest')
    plt.legend()
    plt.grid(True, alpha=0.3)
    os.makedirs('results', exist_ok=True)
    plt.savefig('results/combined_training_graph.png', dpi=300, bbox_inches='tight')
    plt.show()


def combined_testing_graph(reg):
    rf_bundle, lin_bundle = load_models()
    rf_model = rf_bundle['model']
    lin_model = lin_bundle['model']

    X_test_scaled = reg.X_test_scaled
    y_test = reg.y_test

    rf_test_pred = rf_model.predict(X_test_scaled)
    lin_test_pred = lin_model.predict(X_test_scaled)

    plt.figure(figsize=(12, 8))
    plt.scatter(y_test, rf_test_pred, alpha=0.7, s=90, label='Random Forest', edgecolors='black')
    plt.scatter(y_test, lin_test_pred, alpha=0.7, s=90, label='Linear Regression', edgecolors='black')
    min_val = min(y_test.min(), rf_test_pred.min(), lin_test_pred.min())
    max_val = max(y_test.max(), rf_test_pred.max(), lin_test_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val], 'k--', lw=2, label='Perfect Prediction')
    plt.xlabel('Actual Fertility Score (Test)')
    plt.ylabel('Predicted Fertility Score (Test)')
    plt.title('Combined Testing Graph: Linear vs Random Forest')
    plt.legend()
    plt.grid(True, alpha=0.3)
    os.makedirs('results', exist_ok=True)
    plt.savefig('results/combined_testing_graph.png', dpi=300, bbox_inches='tight')
    plt.show()


def combined_performance_bars(reg):
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

    rf_bundle, lin_bundle = load_models()
    rf_model = rf_bundle['model']
    lin_model = lin_bundle['model']

    X_test_scaled = reg.X_test_scaled
    y_test = reg.y_test

    rf_pred = rf_model.predict(X_test_scaled)
    lin_pred = lin_model.predict(X_test_scaled)

    metrics = {
        'Random Forest': {
            'R²': r2_score(y_test, rf_pred),
            'RMSE': np.sqrt(mean_squared_error(y_test, rf_pred)),
            'MAE': mean_absolute_error(y_test, rf_pred)
        },
        'Linear Regression': {
            'R²': r2_score(y_test, lin_pred),
            'RMSE': np.sqrt(mean_squared_error(y_test, lin_pred)),
            'MAE': mean_absolute_error(y_test, lin_pred)
        }
    }

    categories = ['R²', 'RMSE', 'MAE']
    x = np.arange(len(categories))
    width = 0.35

    rf_vals = [metrics['Random Forest'][c] for c in categories]
    lin_vals = [metrics['Linear Regression'][c] for c in categories]

    plt.figure(figsize=(12, 8))
    plt.bar(x - width/2, rf_vals, width, label='Random Forest')
    plt.bar(x + width/2, lin_vals, width, label='Linear Regression')
    plt.xticks(x, categories)
    plt.ylabel('Score')
    plt.title('Performance Comparison (Test)')
    plt.legend()
    plt.grid(True, alpha=0.3, axis='y')
    os.makedirs('results', exist_ok=True)
    plt.savefig('results/combined_performance.png', dpi=300, bbox_inches='tight')
    plt.show()
    return metrics


def combined_evaluation_overlay(reg):
    rf_bundle, lin_bundle = load_models()
    rf_model = rf_bundle['model']
    lin_model = lin_bundle['model']

    X_test_scaled = reg.X_test_scaled
    y_test = reg.y_test

    rf_pred = rf_model.predict(X_test_scaled)
    lin_pred = lin_model.predict(X_test_scaled)

    plt.figure(figsize=(12, 8))
    plt.plot(range(len(y_test)), y_test.values, label='Actual', color='black', linewidth=2)
    plt.plot(range(len(y_test)), rf_pred, label='Random Forest Predicted', alpha=0.8)
    plt.plot(range(len(y_test)), lin_pred, label='Linear Regression Predicted', alpha=0.8)
    plt.xlabel('Sample Index')
    plt.ylabel('Fertility Score')
    plt.title('Evaluation Overlay: Actual vs Predicted (Test)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    os.makedirs('results', exist_ok=True)
    plt.savefig('results/combined_evaluation_overlay.png', dpi=300, bbox_inches='tight')
    plt.show()


def plot_combined_loss_curves(reg):
    """Plot training and validation MSE vs training sizes for both models side-by-side."""
    rf_bundle, lin_bundle = load_models()
    rf_model = rf_bundle['model']
    lin_model = lin_bundle['model']

    X_train_scaled = reg.X_train_scaled
    y_train = reg.y_train

    train_sizes = np.linspace(0.1, 1.0, 10)

    # RF learning curve (MSE)
    rf_sizes, rf_train_scores, rf_val_scores = learning_curve(
        rf_model, X_train_scaled, y_train,
        train_sizes=train_sizes, cv=3, scoring='neg_mean_squared_error', n_jobs=-1
    )

    # Linear learning curve (MSE)
    lin_sizes, lin_train_scores, lin_val_scores = learning_curve(
        lin_model, X_train_scaled, y_train,
        train_sizes=train_sizes, cv=3, scoring='neg_mean_squared_error', n_jobs=-1
    )

    rf_train_mse = -rf_train_scores.mean(axis=1)
    rf_val_mse = -rf_val_scores.mean(axis=1)
    lin_train_mse = -lin_train_scores.mean(axis=1)
    lin_val_mse = -lin_val_scores.mean(axis=1)

    plt.figure(figsize=(12, 8))
    plt.plot(rf_sizes, rf_train_mse, 'o-', label='RF Train MSE')
    plt.plot(rf_sizes, rf_val_mse, 'o-', label='RF Val MSE')
    plt.plot(lin_sizes, lin_train_mse, 'o-', label='Linear Train MSE')
    plt.plot(lin_sizes, lin_val_mse, 'o-', label='Linear Val MSE')
    plt.xlabel('Training Set Size')
    plt.ylabel('MSE (lower is better)')
    plt.title('Training and Validation Loss Curves (MSE)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    os.makedirs('results', exist_ok=True)
    plt.savefig('results/combined_loss_curves.png', dpi=300, bbox_inches='tight')
    plt.show()


def rf_loss_curves(reg, save_path='results/rf_loss_curves.png'):
    """Plot RF training and validation MSE vs training sizes."""
    rf_bundle, _ = load_models()
    rf_model = rf_bundle['model']
    X_train_scaled = reg.X_train_scaled
    y_train = reg.y_train
    train_sizes = np.linspace(0.1, 1.0, 10)
    sizes, train_scores, val_scores = learning_curve(
        rf_model, X_train_scaled, y_train,
        train_sizes=train_sizes, cv=3, scoring='neg_mean_squared_error', n_jobs=-1
    )
    train_mse = -train_scores.mean(axis=1)
    val_mse = -val_scores.mean(axis=1)
    plt.figure(figsize=(12, 8))
    plt.plot(sizes, train_mse, 'o-', label='RF Train MSE')
    plt.plot(sizes, val_mse, 'o-', label='RF Val MSE')
    plt.xlabel('Training Set Size')
    plt.ylabel('MSE (lower is better)')
    plt.title('Random Forest: Training and Validation Loss Curves (MSE)')
    plt.legend(); plt.grid(True, alpha=0.3)
    os.makedirs('results', exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def linear_loss_curves(reg, save_path='results/linear_loss_curves.png'):
    """Plot Linear Regression training and validation MSE vs training sizes."""
    _, lin_bundle = load_models()
    lin_model = lin_bundle['model']
    X_train_scaled = reg.X_train_scaled
    y_train = reg.y_train
    train_sizes = np.linspace(0.1, 1.0, 10)
    sizes, train_scores, val_scores = learning_curve(
        lin_model, X_train_scaled, y_train,
        train_sizes=train_sizes, cv=3, scoring='neg_mean_squared_error', n_jobs=-1
    )
    train_mse = -train_scores.mean(axis=1)
    val_mse = -val_scores.mean(axis=1)
    plt.figure(figsize=(12, 8))
    plt.plot(sizes, train_mse, 'o-', label='Linear Train MSE')
    plt.plot(sizes, val_mse, 'o-', label='Linear Val MSE')
    plt.xlabel('Training Set Size')
    plt.ylabel('MSE (lower is better)')
    plt.title('Linear Regression: Training and Validation Loss Curves (MSE)')
    plt.legend(); plt.grid(True, alpha=0.3)
    os.makedirs('results', exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def rf_training_graph(reg, save_path='results/rf_training_graph.png'):
    """Save a Random Forest-only training scatter from the same data used in combined plot."""
    rf_bundle, _ = load_models()
    rf_model = rf_bundle['model']

    X_train_scaled = reg.X_train_scaled
    y_train = reg.y_train

    rf_train_pred = rf_model.predict(X_train_scaled)

    plt.figure(figsize=(12, 8))
    plt.scatter(y_train, rf_train_pred, alpha=0.7, s=80, label='Random Forest', edgecolors='black', color='tab:blue')
    min_val = min(y_train.min(), rf_train_pred.min())
    max_val = max(y_train.max(), rf_train_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val], 'k--', lw=2, label='Perfect Prediction')
    plt.xlabel('Actual Fertility Score (Train)')
    plt.ylabel('Predicted Fertility Score (Train)')
    plt.title('Training Set: Actual vs Predicted - Random Forest Regressor')
    plt.legend()
    plt.grid(True, alpha=0.3)
    os.makedirs('results', exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def generate_all_combined_graphs():
    reg = prepare_scaled_features(None)
    print('📈 Creating combined training graph...')
    combined_training_graph(reg)
    print('📈 Creating combined testing graph...')
    combined_testing_graph(reg)
    print('📊 Creating combined performance bars...')
    metrics = combined_performance_bars(reg)
    print('📊 Creating combined evaluation overlay...')
    combined_evaluation_overlay(reg)
    # Loss curves per model and combined
    rf_loss_curves(reg)
    linear_loss_curves(reg)
    plot_combined_loss_curves(reg)
    print('✅ Combined comparison graphs saved to results/.')
    return metrics


def main():
    return generate_all_combined_graphs()


if __name__ == '__main__':
    main()


