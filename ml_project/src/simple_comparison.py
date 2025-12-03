"""
Simple Model Comparison: Classifier vs Regressor
==============================================

This script provides a simple comparison between the Random Forest Classifier and Regressor
for soil fertility prediction.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

def load_models_and_data():
    """Load both models and test data"""
    print("Loading models and data...")
    
    # Load classifier
    classifier_data = joblib.load('models/soil_fertility_model.pkl')
    classifier = classifier_data['model']
    
    # Load regressor
    regressor_data = joblib.load('models/soil_fertility_regressor.pkl')
    regressor = regressor_data['model']
    
    # Load test data
    from soil_fertility_classifier_fixed import SoilFertilityClassifier
    classifier_obj = SoilFertilityClassifier()
    data = classifier_obj.load_and_preprocess_data('soil_nutrients.xlsx')
    classifier_obj.prepare_features()
    
    X_test = classifier_obj.X_test
    y_test_class = classifier_obj.y_test
    y_test_score = classifier_obj.data.loc[classifier_obj.X_test.index, 'Fertility_Score']
    
    return classifier, regressor, X_test, y_test_class, y_test_score

def evaluate_models(classifier, regressor, X_test, y_test_class, y_test_score):
    """Evaluate both models"""
    print("Evaluating models...")
    
    # Classifier evaluation
    y_pred_class = classifier.predict(X_test)
    classifier_metrics = {
        'accuracy': accuracy_score(y_test_class, y_pred_class),
        'precision': precision_score(y_test_class, y_pred_class, average='weighted'),
        'recall': recall_score(y_test_class, y_pred_class, average='weighted'),
        'f1_score': f1_score(y_test_class, y_pred_class, average='weighted')
    }
    
    # Regressor evaluation
    y_pred_score = regressor.predict(X_test)
    regressor_metrics = {
        'mse': mean_squared_error(y_test_score, y_pred_score),
        'rmse': np.sqrt(mean_squared_error(y_test_score, y_pred_score)),
        'mae': mean_absolute_error(y_test_score, y_pred_score),
        'r2': r2_score(y_test_score, y_pred_score)
    }
    
    return classifier_metrics, regressor_metrics, y_pred_class, y_pred_score

def plot_simple_comparison(classifier, regressor, classifier_metrics, regressor_metrics, save_path='results/simple_model_comparison.png'):
    """Create simple comparison plots"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # 1. Classification metrics
    metrics = ['accuracy', 'precision', 'recall', 'f1_score']
    values = [classifier_metrics[m] for m in metrics]
    
    bars = axes[0, 0].bar(metrics, values, color=['blue', 'green', 'orange', 'red'])
    axes[0, 0].set_title('Classifier Performance')
    axes[0, 0].set_ylabel('Score')
    axes[0, 0].set_ylim(0, 1.1)
    axes[0, 0].grid(True, alpha=0.3)
    
    for bar, value in zip(bars, values):
        height = bar.get_height()
        axes[0, 0].text(bar.get_x() + bar.get_width()/2., height + 0.01,
                       f'{value:.3f}', ha='center', va='bottom')
    
    # 2. Regression metrics (normalized)
    metrics = ['mse', 'rmse', 'mae', 'r2']
    values = [regressor_metrics[m] for m in metrics]
    
    # Normalize for display
    normalized_values = [v/100 if m != 'r2' else max(0, v) for m, v in zip(metrics, values)]
    
    bars = axes[0, 1].bar(metrics, normalized_values, color=['purple', 'brown', 'pink', 'cyan'])
    axes[0, 1].set_title('Regressor Performance (Normalized)')
    axes[0, 1].set_ylabel('Score')
    axes[0, 1].set_ylim(0, 1.1)
    axes[0, 1].grid(True, alpha=0.3)
    
    for bar, value in zip(bars, values):
        height = bar.get_height()
        axes[0, 1].text(bar.get_x() + bar.get_width()/2., height + 0.01,
                       f'{value:.3f}', ha='center', va='bottom')
    
    # 3. Feature importance comparison
    classifier_importance = classifier.feature_importances_
    regressor_importance = regressor.feature_importances_
    
    feature_names = ['Sand', 'Silt', 'Clay', 'pH', 'OC', 'TN', 'AP', 'EP', 'CEC', 'BS', 'SS', 'SC']
    
    x = np.arange(len(feature_names))
    width = 0.35
    
    axes[1, 0].bar(x - width/2, classifier_importance, width, label='Classifier', alpha=0.7)
    axes[1, 0].bar(x + width/2, regressor_importance, width, label='Regressor', alpha=0.7)
    axes[1, 0].set_title('Feature Importance Comparison')
    axes[1, 0].set_ylabel('Importance')
    axes[1, 0].set_xticks(x)
    axes[1, 0].set_xticklabels(feature_names, rotation=45)
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # 4. Summary text
    summary_text = f"""
    Classifier Results:
    Accuracy: {classifier_metrics['accuracy']:.3f}
    F1-Score: {classifier_metrics['f1_score']:.3f}
    
    Regressor Results:
    R² Score: {regressor_metrics['r2']:.3f}
    RMSE: {regressor_metrics['rmse']:.2f}
    MAE: {regressor_metrics['mae']:.2f}
    
    Recommendation:
    {'Use Classifier' if classifier_metrics['accuracy'] > 0.7 else 'Collect More Data'}
    """
    
    axes[1, 1].text(0.1, 0.5, summary_text, transform=axes[1, 1].transAxes, fontsize=12,
                    verticalalignment='center', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
    axes[1, 1].set_title('Summary & Recommendation')
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()

def generate_simple_report(classifier_metrics, regressor_metrics, save_path='results/simple_comparison_report.md'):
    """Generate simple comparison report"""
    report = f"""
# Simple Model Comparison Report

## 📊 **Performance Summary**

### **Random Forest Classifier**
- **Accuracy**: {classifier_metrics['accuracy']:.3f} ({classifier_metrics['accuracy']*100:.1f}%)
- **Precision**: {classifier_metrics['precision']:.3f}
- **Recall**: {classifier_metrics['recall']:.3f}
- **F1-Score**: {classifier_metrics['f1_score']:.3f}

### **Random Forest Regressor**
- **R² Score**: {regressor_metrics['r2']:.3f}
- **RMSE**: {regressor_metrics['rmse']:.2f}
- **MAE**: {regressor_metrics['mae']:.2f}
- **MSE**: {regressor_metrics['mse']:.2f}

## 🎯 **Key Findings**

1. **Classifier Performance**: The classifier achieves {classifier_metrics['accuracy']*100:.1f}% accuracy in categorizing soil fertility into High/Medium/Low classes.

2. **Regressor Performance**: The regressor achieves an R² score of {regressor_metrics['r2']:.3f}, indicating {'good' if regressor_metrics['r2'] > 0.7 else 'moderate' if regressor_metrics['r2'] > 0.3 else 'limited'} predictive power.

3. **Error Analysis**: The regressor has an RMSE of {regressor_metrics['rmse']:.2f} and MAE of {regressor_metrics['mae']:.2f}, meaning predictions are typically off by about {regressor_metrics['mae']:.1f} fertility score points.

## 📈 **Recommendations**

### **For Practical Use**
- **Use Classifier**: Better performance with current dataset size
- **Accuracy**: {classifier_metrics['accuracy']*100:.1f}% accuracy is suitable for practical applications
- **Interpretability**: Clear High/Medium/Low categories are easier to understand

### **For Research**
- **Use Regressor**: Provides continuous fertility scores
- **Data Collection**: Need more data to improve regressor performance
- **Feature Engineering**: Consider additional soil properties

## ✅ **Conclusion**

The **Random Forest Classifier** demonstrates superior performance for the current dataset, making it the recommended choice for practical soil fertility assessment. The **Random Forest Regressor** provides more detailed predictions but requires additional data to achieve optimal performance.

---
*Generated: September 19, 2025*
"""
    
    with open(save_path, 'w') as f:
        f.write(report)
    
    print(f"Simple comparison report saved to {save_path}")

def main():
    """Main function"""
    print("🔄 Simple Model Comparison Analysis")
    print("=" * 40)
    
    # Load models and data
    classifier, regressor, X_test, y_test_class, y_test_score = load_models_and_data()
    
    # Evaluate models
    classifier_metrics, regressor_metrics, y_pred_class, y_pred_score = evaluate_models(
        classifier, regressor, X_test, y_test_class, y_test_score
    )
    
    # Print results
    print("\n📊 Model Performance Results:")
    print(f"Classifier Accuracy: {classifier_metrics['accuracy']:.3f}")
    print(f"Regressor R²: {regressor_metrics['r2']:.3f}")
    print(f"Regressor RMSE: {regressor_metrics['rmse']:.2f}")
    
    # Create visualizations
    print("\n📈 Creating comparison visualization...")
    plot_simple_comparison(classifier, regressor, classifier_metrics, regressor_metrics)
    
    # Generate report
    print("📝 Generating comparison report...")
    generate_simple_report(classifier_metrics, regressor_metrics)
    
    print("\n✅ Simple comparison completed!")
    print("Check 'results/' folder for outputs.")
    
    return classifier_metrics, regressor_metrics

if __name__ == "__main__":
    classifier_metrics, regressor_metrics = main()
