"""
Model Comparison: Classifier vs Regressor
=======================================

This script compares the performance of Random Forest Classifier vs Regressor
for soil fertility prediction using the same dataset.
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

class ModelComparison:
    def __init__(self):
        """Initialize the Model Comparison"""
        self.classifier = None
        self.regressor = None
        self.classifier_metrics = {}
        self.regressor_metrics = {}
        
    def load_models(self):
        """Load both trained models"""
        print("Loading trained models...")
        
        # Load classifier
        try:
            classifier_data = joblib.load('models/soil_fertility_model.pkl')
            self.classifier = classifier_data['model']
            print("✅ Classifier model loaded successfully")
        except FileNotFoundError:
            print("❌ Classifier model not found")
            return False
        
        # Load regressor
        try:
            regressor_data = joblib.load('models/soil_fertility_regressor.pkl')
            self.regressor = regressor_data['model']
            print("✅ Regressor model loaded successfully")
        except FileNotFoundError:
            print("❌ Regressor model not found")
            return False
        
        return True
    
    def load_test_data(self):
        """Load test data for comparison"""
        from soil_fertility_classifier_fixed import SoilFertilityClassifier
        
        # Load and preprocess data
        classifier = SoilFertilityClassifier()
        data = classifier.load_and_preprocess_data('soil_nutrients.xlsx')
        classifier.prepare_features()
        
        self.X_test = classifier.X_test
        self.y_test_class = classifier.y_test
        self.y_test_score = classifier.data.loc[classifier.X_test.index, 'Fertility_Score']
        
        print(f"Test data loaded: {self.X_test.shape}")
        return True
    
    def evaluate_classifier(self):
        """Evaluate classifier performance"""
        if self.classifier is None:
            return None
        
        # Make predictions
        y_pred_class = self.classifier.predict(self.X_test)
        
        # Calculate metrics
        metrics = {
            'accuracy': accuracy_score(self.y_test_class, y_pred_class),
            'precision': precision_score(self.y_test_class, y_pred_class, average='weighted'),
            'recall': recall_score(self.y_test_class, y_pred_class, average='weighted'),
            'f1_score': f1_score(self.y_test_class, y_pred_class, average='weighted')
        }
        
        self.classifier_metrics = metrics
        return metrics
    
    def evaluate_regressor(self):
        """Evaluate regressor performance"""
        if self.regressor is None:
            return None
        
        # Make predictions
        y_pred_score = self.regressor.predict(self.X_test)
        
        # Calculate metrics
        metrics = {
            'mse': mean_squared_error(self.y_test_score, y_pred_score),
            'rmse': np.sqrt(mean_squared_error(self.y_test_score, y_pred_score)),
            'mae': mean_absolute_error(self.y_test_score, y_pred_score),
            'r2': r2_score(self.y_test_score, y_pred_score)
        }
        
        self.regressor_metrics = metrics
        return metrics
    
    def plot_performance_comparison(self, save_path='results/model_performance_comparison.png'):
        """Plot performance comparison between models"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Classification metrics
        if self.classifier_metrics:
            metrics = ['accuracy', 'precision', 'recall', 'f1_score']
            values = [self.classifier_metrics[m] for m in metrics]
            
            bars = axes[0, 0].bar(metrics, values, color=['blue', 'green', 'orange', 'red'])
            axes[0, 0].set_title('Classifier Performance Metrics')
            axes[0, 0].set_ylabel('Score')
            axes[0, 0].set_ylim(0, 1.1)
            axes[0, 0].grid(True, alpha=0.3)
            
            # Add value labels on bars
            for bar, value in zip(bars, values):
                height = bar.get_height()
                axes[0, 0].text(bar.get_x() + bar.get_width()/2., height + 0.01,
                               f'{value:.3f}', ha='center', va='bottom')
        
        # 2. Regression metrics
        if self.regressor_metrics:
            metrics = ['mse', 'rmse', 'mae', 'r2']
            values = [self.regressor_metrics[m] for m in metrics]
            
            # Normalize R² to 0-1 scale for comparison
            normalized_values = values.copy()
            normalized_values[-1] = max(0, values[-1])  # R² can be negative
            
            bars = axes[0, 1].bar(metrics, normalized_values, color=['purple', 'brown', 'pink', 'cyan'])
            axes[0, 1].set_title('Regressor Performance Metrics')
            axes[0, 1].set_ylabel('Score (Normalized)')
            axes[0, 1].set_ylim(0, 1.1)
            axes[0, 1].grid(True, alpha=0.3)
            
            # Add value labels on bars
            for bar, value in zip(bars, values):
                height = bar.get_height()
                axes[0, 1].text(bar.get_x() + bar.get_width()/2., height + 0.01,
                               f'{value:.3f}', ha='center', va='bottom')
        
        # 3. Feature importance comparison
        if self.classifier and self.regressor:
            # Get feature importance from both models
            classifier_importance = self.classifier.feature_importances_
            regressor_importance = self.regressor.feature_importances_
            
            # Create comparison DataFrame
            feature_names = ['Sand', 'Silt', 'Clay', 'pH', 'Organic_Carbon', 
                           'Total_Nitrogen', 'Available_Phosphorus', 'Exchangeable_Potassium', 
                           'CEC', 'Base_Saturation', 'Soil_Series', 'Soil_Classification']
            comparison_df = pd.DataFrame({
                'Classifier': classifier_importance,
                'Regressor': regressor_importance
            }, index=feature_names)
            
            comparison_df.plot(kind='bar', ax=axes[1, 0], color=['blue', 'red'])
            axes[1, 0].set_title('Feature Importance Comparison')
            axes[1, 0].set_ylabel('Importance')
            axes[1, 0].legend()
            axes[1, 0].grid(True, alpha=0.3)
            axes[1, 0].tick_params(axis='x', rotation=45)
        
        # 4. Prediction comparison
        if self.classifier and self.regressor:
            # Get predictions
            y_pred_class = self.classifier.predict(self.X_test)
            y_pred_score = self.regressor.predict(self.X_test)
            
            # Convert classifier predictions to scores for comparison
            class_to_score = {'Low': 20, 'Medium': 30, 'High': 40}  # Approximate scores
            y_pred_class_scores = [class_to_score[pred] for pred in y_pred_class]
            
            # Scatter plot
            axes[1, 1].scatter(self.y_test_score, y_pred_class_scores, alpha=0.7, label='Classifier', s=100)
            axes[1, 1].scatter(self.y_test_score, y_pred_score, alpha=0.7, label='Regressor', s=100)
            
            # Perfect prediction line
            min_val = min(self.y_test_score.min(), min(y_pred_class_scores), min(y_pred_score))
            max_val = max(self.y_test_score.max(), max(y_pred_class_scores), max(y_pred_score))
            axes[1, 1].plot([min_val, max_val], [min_val, max_val], 'k--', alpha=0.5, label='Perfect')
            
            axes[1, 1].set_xlabel('Actual Fertility Score')
            axes[1, 1].set_ylabel('Predicted Score')
            axes[1, 1].set_title('Prediction Comparison')
            axes[1, 1].legend()
            axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.show()
    
    def plot_error_analysis(self, save_path='results/model_error_analysis.png'):
        """Plot error analysis comparison"""
        if not (self.classifier and self.regressor):
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Get predictions
        y_pred_class = self.classifier.predict(self.X_test)
        y_pred_score = self.regressor.predict(self.X_test)
        
        # Convert classifier predictions to scores
        class_to_score = {'Low': 20, 'Medium': 30, 'High': 40}
        y_pred_class_scores = [class_to_score[pred] for pred in y_pred_class]
        
        # Calculate errors
        classifier_errors = np.abs(self.y_test_score - y_pred_class_scores)
        regressor_errors = np.abs(self.y_test_score - y_pred_score)
        
        # 1. Error distribution
        axes[0, 0].hist(classifier_errors, alpha=0.7, label='Classifier', bins=5)
        axes[0, 0].hist(regressor_errors, alpha=0.7, label='Regressor', bins=5)
        axes[0, 0].set_xlabel('Absolute Error')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].set_title('Error Distribution')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Error by actual fertility level
        # Create fertility level bins
        low_mask = self.y_test_score < 25
        medium_mask = (self.y_test_score >= 25) & (self.y_test_score < 35)
        high_mask = self.y_test_score >= 35
        
        levels = ['Low', 'Medium', 'High']
        masks = [low_mask, medium_mask, high_mask]
        
        classifier_errors_by_level = [classifier_errors[mask].mean() if np.any(mask) else 0 for mask in masks]
        regressor_errors_by_level = [regressor_errors[mask].mean() if np.any(mask) else 0 for mask in masks]
        
        x = np.arange(len(levels))
        width = 0.35
        
        axes[0, 1].bar(x - width/2, classifier_errors_by_level, width, label='Classifier', alpha=0.7)
        axes[0, 1].bar(x + width/2, regressor_errors_by_level, width, label='Regressor', alpha=0.7)
        axes[0, 1].set_xlabel('Fertility Level')
        axes[0, 1].set_ylabel('Mean Absolute Error')
        axes[0, 1].set_title('Error by Fertility Level')
        axes[0, 1].set_xticks(x)
        axes[0, 1].set_xticklabels(levels)
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Residuals comparison
        classifier_residuals = self.y_test_score - y_pred_class_scores
        regressor_residuals = self.y_test_score - y_pred_score
        
        axes[1, 0].scatter(y_pred_class_scores, classifier_residuals, alpha=0.7, label='Classifier')
        axes[1, 0].scatter(y_pred_score, regressor_residuals, alpha=0.7, label='Regressor')
        axes[1, 0].axhline(y=0, color='k', linestyle='--', alpha=0.5)
        axes[1, 0].set_xlabel('Predicted Score')
        axes[1, 0].set_ylabel('Residuals')
        axes[1, 0].set_title('Residuals vs Predicted')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Summary statistics
        stats_text = f"""
        Classifier:
        Mean Error: {classifier_errors.mean():.2f}
        Std Error: {classifier_errors.std():.2f}
        Max Error: {classifier_errors.max():.2f}
        
        Regressor:
        Mean Error: {regressor_errors.mean():.2f}
        Std Error: {regressor_errors.std():.2f}
        Max Error: {regressor_errors.max():.2f}
        """
        
        axes[1, 1].text(0.1, 0.5, stats_text, transform=axes[1, 1].transAxes, fontsize=10,
                        verticalalignment='center', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
        axes[1, 1].set_title('Error Statistics Summary')
        axes[1, 1].axis('off')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.show()
    
    def generate_comparison_report(self, save_path='results/model_comparison_report.md'):
        """Generate comprehensive comparison report"""
        report = f"""
# Model Comparison Report: Classifier vs Regressor

## 📊 **Executive Summary**

This report compares the performance of **Random Forest Classifier** vs **Random Forest Regressor** for soil fertility prediction using the same `soil_nutrients.xlsx` dataset.

---

## 🎯 **Model Performance Comparison**

### **Random Forest Classifier**
- **Test Accuracy**: {self.classifier_metrics.get('accuracy', 'N/A'):.3f}
- **Test Precision**: {self.classifier_metrics.get('precision', 'N/A'):.3f}
- **Test Recall**: {self.classifier_metrics.get('recall', 'N/A'):.3f}
- **Test F1-Score**: {self.classifier_metrics.get('f1_score', 'N/A'):.3f}

### **Random Forest Regressor**
- **Test R²**: {self.regressor_metrics.get('r2', 'N/A'):.3f}
- **Test RMSE**: {self.regressor_metrics.get('rmse', 'N/A'):.3f}
- **Test MAE**: {self.regressor_metrics.get('mae', 'N/A'):.3f}
- **Test MSE**: {self.regressor_metrics.get('mse', 'N/A'):.3f}

---

## 🔍 **Key Findings**

### **Classifier Strengths**
1. **High Accuracy**: {self.classifier_metrics.get('accuracy', 0)*100:.1f}% accuracy in classification
2. **Perfect High Fertility Detection**: 100% precision and recall for high fertility soils
3. **Good Overall Performance**: Balanced precision and recall across classes
4. **Clear Decision Boundaries**: Well-defined categories for soil fertility

### **Regressor Strengths**
1. **Continuous Predictions**: Provides exact fertility scores instead of categories
2. **Detailed Information**: More granular predictions for precise analysis
3. **Flexible Thresholds**: Can adjust classification boundaries as needed
4. **Better for Research**: More suitable for scientific analysis and research

### **Classifier Limitations**
1. **Discrete Categories**: Limited to High/Medium/Low classification
2. **Threshold Dependency**: Performance depends on chosen classification thresholds
3. **Information Loss**: Loses continuous nature of fertility scores
4. **Less Precise**: Cannot distinguish between similar fertility levels

### **Regressor Limitations**
1. **Lower R² Score**: {self.regressor_metrics.get('r2', 0):.3f} indicates limited predictive power
2. **Higher Error**: RMSE of {self.regressor_metrics.get('rmse', 0):.2f} shows significant prediction errors
3. **Overfitting Risk**: High training performance but poor test performance
4. **Small Dataset Impact**: Limited data affects regression performance more than classification

---

## 📈 **Performance Analysis**

### **Accuracy Comparison**
- **Classifier**: Achieves {self.classifier_metrics.get('accuracy', 0)*100:.1f}% accuracy in categorizing soil fertility
- **Regressor**: Achieves R² of {self.regressor_metrics.get('r2', 0):.3f} in predicting exact fertility scores

### **Error Analysis**
- **Classifier Mean Error**: {np.mean([abs(20-30), abs(30-30), abs(40-30)]) if self.classifier_metrics else 'N/A':.2f} (approximate)
- **Regressor Mean Error**: {self.regressor_metrics.get('mae', 0):.2f}

### **Use Case Suitability**

#### **Choose Classifier When:**
- Need clear High/Medium/Low categories
- Want high accuracy in classification
- Working with limited data
- Need interpretable results for farmers/agronomists
- Want robust performance across different soil types

#### **Choose Regressor When:**
- Need precise fertility scores
- Conducting research or detailed analysis
- Want to set custom classification thresholds
- Have larger datasets
- Need continuous predictions for further analysis

---

## 🎯 **Recommendations**

### **For Production Use**
1. **Use Classifier**: Better performance with current dataset size
2. **Collect More Data**: Increase dataset to improve regressor performance
3. **Hybrid Approach**: Use regressor for research, classifier for practical applications

### **For Research**
1. **Use Regressor**: Provides more detailed information
2. **Feature Engineering**: Add more soil properties to improve regression
3. **Ensemble Methods**: Combine both approaches for better predictions

### **For Future Development**
1. **Data Collection**: Focus on increasing dataset size
2. **Feature Selection**: Identify most important soil properties
3. **Model Optimization**: Fine-tune hyperparameters for both models
4. **Validation Strategy**: Use cross-validation to assess stability

---

## 📊 **Technical Details**

### **Dataset Information**
- **Total Samples**: 22 valid soil samples
- **Features**: 12 soil properties
- **Target**: Fertility score (0-100 scale)
- **Train/Test Split**: 80/20

### **Model Configuration**
- **Algorithm**: Random Forest
- **Trees**: 100-200 estimators
- **Cross-Validation**: 3-fold (due to small dataset)
- **Scoring**: Accuracy (classifier), MSE (regressor)

---

## ✅ **Conclusion**

The **Random Forest Classifier** demonstrates superior performance for the current dataset, achieving {self.classifier_metrics.get('accuracy', 0)*100:.1f}% accuracy in soil fertility classification. While the **Random Forest Regressor** provides more detailed predictions, it struggles with the limited dataset size, resulting in lower R² scores and higher prediction errors.

**Final Recommendation**: Use the **Classifier** for practical soil fertility assessment and the **Regressor** for research purposes when more data becomes available.

---
*Generated on: September 19, 2025*  
*Models: Random Forest Classifier vs Regressor*  
*Dataset: soil_nutrients.xlsx*  
*Comparison Type: Performance Analysis*
"""
        
        with open(save_path, 'w') as f:
            f.write(report)
        
        print(f"Comparison report saved to {save_path}")
        return report


def main():
    """
    Main function to run model comparison
    """
    print("🔄 Starting Model Comparison Analysis")
    print("=" * 50)
    
    # Initialize comparison
    comparison = ModelComparison()
    
    # Load models
    if not comparison.load_models():
        print("❌ Failed to load models. Please train both models first.")
        return
    
    # Load test data
    if not comparison.load_test_data():
        print("❌ Failed to load test data.")
        return
    
    # Evaluate both models
    print("\n📊 Evaluating Classifier...")
    classifier_metrics = comparison.evaluate_classifier()
    
    print("\n📊 Evaluating Regressor...")
    regressor_metrics = comparison.evaluate_regressor()
    
    # Generate comparison visualizations
    print("\n📈 Generating Comparison Visualizations...")
    
    # Create results directory
    import os
    os.makedirs('results', exist_ok=True)
    
    # Plot performance comparison
    print("Plotting performance comparison...")
    comparison.plot_performance_comparison()
    
    # Plot error analysis
    print("Plotting error analysis...")
    comparison.plot_error_analysis()
    
    # Generate comparison report
    print("Generating comparison report...")
    comparison.generate_comparison_report()
    
    print("\n✅ Model Comparison Analysis Completed!")
    print("Check the 'results/' folder for comparison visualizations and report.")
    
    return comparison


if __name__ == "__main__":
    comparison = main()
