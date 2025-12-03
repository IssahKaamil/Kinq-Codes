"""
Validation and Testing Graphs for Soil Fertility Classification
============================================================

This script generates comprehensive validation and testing graphs including:
- Learning curves
- Validation curves
- ROC curves (for multi-class)
- Precision-Recall curves
- Prediction confidence analysis
- Error analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import learning_curve, validation_curve, cross_val_score
from sklearn.metrics import (
    roc_curve, auc, precision_recall_curve, confusion_matrix,
    classification_report, accuracy_score, precision_score, recall_score, f1_score
)
from sklearn.preprocessing import label_binarize
import joblib
import os
from itertools import cycle
import warnings
warnings.filterwarnings('ignore')

class ValidationTestingGraphs:
    def __init__(self, model_path='models/soil_fertility_model.pkl'):
        """
        Initialize with trained model
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
        self.classes = ['High', 'Medium', 'Low']
        
    def load_model_and_data(self):
        """
        Load the trained model and prepare data
        """
        # Load model
        model_data = joblib.load(self.model_path)
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.label_encoders = model_data['label_encoders']
        self.feature_columns = model_data['feature_columns']
        
        # Load and preprocess data (same as training)
        from soil_fertility_classifier_fixed import SoilFertilityClassifier
        classifier = SoilFertilityClassifier()
        data = classifier.load_and_preprocess_data('soil_nutrients.xlsx')
        classifier.prepare_features()
        
        self.X_train = classifier.X_train
        self.X_test = classifier.X_test
        self.y_train = classifier.y_train
        self.y_test = classifier.y_test
        
        print(f"Model and data loaded successfully!")
        print(f"Training set: {self.X_train.shape}")
        print(f"Test set: {self.X_test.shape}")
        
    def plot_learning_curve(self, save_path='results/learning_curve.png'):
        """
        Plot learning curve showing training and validation scores
        """
        train_sizes = np.linspace(0.1, 1.0, 10)
        
        train_sizes_abs, train_scores, val_scores = learning_curve(
            self.model, self.X_train, self.y_train,
            train_sizes=train_sizes, cv=5, scoring='accuracy',
            n_jobs=-1, random_state=42
        )
        
        train_scores_mean = train_scores.mean(axis=1)
        train_scores_std = train_scores.std(axis=1)
        val_scores_mean = val_scores.mean(axis=1)
        val_scores_std = val_scores.std(axis=1)
        
        plt.figure(figsize=(12, 8))
        plt.plot(train_sizes_abs, train_scores_mean, 'o-', color='blue', label='Training Score')
        plt.fill_between(train_sizes_abs, 
                        train_scores_mean - train_scores_std,
                        train_scores_mean + train_scores_std, 
                        alpha=0.1, color='blue')
        
        plt.plot(train_sizes_abs, val_scores_mean, 'o-', color='red', label='Validation Score')
        plt.fill_between(train_sizes_abs,
                        val_scores_mean - val_scores_std,
                        val_scores_mean + val_scores_std,
                        alpha=0.1, color='red')
        
        plt.xlabel('Training Set Size')
        plt.ylabel('Accuracy Score')
        plt.title('Learning Curve - Soil Fertility Classification')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.ylim(0, 1.1)
        
        # Add annotations
        plt.annotate(f'Final Training Score: {train_scores_mean[-1]:.3f}',
                    xy=(train_sizes_abs[-1], train_scores_mean[-1]),
                    xytext=(10, 10), textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.7),
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        
        plt.annotate(f'Final Validation Score: {val_scores_mean[-1]:.3f}',
                    xy=(train_sizes_abs[-1], val_scores_mean[-1]),
                    xytext=(10, -20), textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='lightcoral', alpha=0.7),
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        return train_sizes_abs, train_scores_mean, val_scores_mean
    
    def plot_validation_curve(self, param_name='n_estimators', param_range=None, 
                            save_path='results/validation_curve.png'):
        """
        Plot validation curve for hyperparameter tuning
        """
        if param_range is None:
            if param_name == 'n_estimators':
                param_range = [10, 25, 50, 75, 100, 150, 200]
            elif param_name == 'max_depth':
                param_range = [None, 5, 10, 15, 20, 25, 30]
            elif param_name == 'min_samples_split':
                param_range = [2, 5, 10, 15, 20]
            else:
                param_range = [1, 2, 3, 4, 5]
        
        train_scores, val_scores = validation_curve(
            RandomForestClassifier(random_state=42, n_jobs=-1),
            self.X_train, self.y_train,
            param_name=param_name, param_range=param_range,
            cv=5, scoring='accuracy', n_jobs=-1
        )
        
        train_scores_mean = train_scores.mean(axis=1)
        train_scores_std = train_scores.std(axis=1)
        val_scores_mean = val_scores.mean(axis=1)
        val_scores_std = val_scores.std(axis=1)
        
        plt.figure(figsize=(12, 8))
        plt.plot(param_range, train_scores_mean, 'o-', color='blue', label='Training Score')
        plt.fill_between(param_range,
                        train_scores_mean - train_scores_std,
                        train_scores_mean + train_scores_std,
                        alpha=0.1, color='blue')
        
        plt.plot(param_range, val_scores_mean, 'o-', color='red', label='Validation Score')
        plt.fill_between(param_range,
                        val_scores_mean - val_scores_std,
                        val_scores_mean + val_scores_std,
                        alpha=0.1, color='red')
        
        plt.xlabel(param_name.replace('_', ' ').title())
        plt.ylabel('Accuracy Score')
        plt.title(f'Validation Curve - {param_name.replace("_", " ").title()}')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.ylim(0, 1.1)
        
        # Find best parameter
        best_idx = np.argmax(val_scores_mean)
        best_param = param_range[best_idx]
        best_score = val_scores_mean[best_idx]
        
        plt.axvline(x=best_param, color='green', linestyle='--', alpha=0.7)
        plt.annotate(f'Best {param_name}: {best_param}\nScore: {best_score:.3f}',
                    xy=(best_param, best_score),
                    xytext=(10, 10), textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgreen', alpha=0.7),
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        return param_range, train_scores_mean, val_scores_mean, best_param
    
    def plot_roc_curves(self, save_path='results/roc_curves.png'):
        """
        Plot ROC curves for multi-class classification
        """
        # Get prediction probabilities
        y_score = self.model.predict_proba(self.X_test)
        
        # Binarize the output
        y_test_bin = label_binarize(self.y_test, classes=self.classes)
        n_classes = y_test_bin.shape[1]
        
        # Compute ROC curve and ROC area for each class
        fpr = dict()
        tpr = dict()
        roc_auc = dict()
        
        for i in range(n_classes):
            fpr[i], tpr[i], _ = roc_curve(y_test_bin[:, i], y_score[:, i])
            roc_auc[i] = auc(fpr[i], tpr[i])
        
        # Compute micro-average ROC curve and ROC area
        fpr["micro"], tpr["micro"], _ = roc_curve(y_test_bin.ravel(), y_score.ravel())
        roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
        
        # Plot ROC curves
        plt.figure(figsize=(12, 8))
        colors = cycle(['blue', 'red', 'green', 'orange', 'purple'])
        
        for i, color in zip(range(n_classes), colors):
            plt.plot(fpr[i], tpr[i], color=color, lw=2,
                    label=f'ROC curve of class {self.classes[i]} (area = {roc_auc[i]:.2f})')
        
        plt.plot(fpr["micro"], tpr["micro"], color='deeppink', linestyle=':', linewidth=4,
                label=f'Micro-average ROC curve (area = {roc_auc["micro"]:.2f})')
        
        plt.plot([0, 1], [0, 1], 'k--', lw=2, label='Random Classifier')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curves - Soil Fertility Classification')
        plt.legend(loc="lower right")
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        return roc_auc
    
    def plot_precision_recall_curves(self, save_path='results/precision_recall_curves.png'):
        """
        Plot Precision-Recall curves for each class
        """
        # Get prediction probabilities
        y_score = self.model.predict_proba(self.X_test)
        
        # Binarize the output
        y_test_bin = label_binarize(self.y_test, classes=self.classes)
        n_classes = y_test_bin.shape[1]
        
        # Compute Precision-Recall curve for each class
        precision = dict()
        recall = dict()
        average_precision = dict()
        
        for i in range(n_classes):
            precision[i], recall[i], _ = precision_recall_curve(y_test_bin[:, i], y_score[:, i])
            average_precision[i] = auc(recall[i], precision[i])
        
        # Compute micro-average Precision-Recall curve
        precision["micro"], recall["micro"], _ = precision_recall_curve(
            y_test_bin.ravel(), y_score.ravel())
        average_precision["micro"] = auc(recall["micro"], precision["micro"])
        
        # Plot Precision-Recall curves
        plt.figure(figsize=(12, 8))
        colors = cycle(['blue', 'red', 'green', 'orange', 'purple'])
        
        for i, color in zip(range(n_classes), colors):
            plt.plot(recall[i], precision[i], color=color, lw=2,
                    label=f'PR curve of class {self.classes[i]} (AP = {average_precision[i]:.2f})')
        
        plt.plot(recall["micro"], precision["micro"], color='deeppink', linestyle=':', linewidth=4,
                label=f'Micro-average PR curve (AP = {average_precision["micro"]:.2f})')
        
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title('Precision-Recall Curves - Soil Fertility Classification')
        plt.legend(loc="lower left")
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        return average_precision
    
    def plot_prediction_confidence(self, save_path='results/prediction_confidence.png'):
        """
        Plot prediction confidence analysis
        """
        # Get prediction probabilities
        y_proba = self.model.predict_proba(self.X_test)
        y_pred = self.model.predict(self.X_test)
        
        # Calculate confidence (max probability)
        confidence = np.max(y_proba, axis=1)
        
        # Create subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Confidence distribution
        axes[0, 0].hist(confidence, bins=10, alpha=0.7, edgecolor='black')
        axes[0, 0].set_xlabel('Prediction Confidence')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].set_title('Distribution of Prediction Confidence')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Confidence vs Accuracy
        correct_predictions = (y_pred == self.y_test)
        axes[0, 1].scatter(confidence, correct_predictions.astype(int), alpha=0.7)
        axes[0, 1].set_xlabel('Prediction Confidence')
        axes[0, 1].set_ylabel('Correct Prediction (1=Yes, 0=No)')
        axes[0, 1].set_title('Confidence vs Prediction Accuracy')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Confidence by predicted class
        confidence_by_class = {}
        for class_name in self.classes:
            mask = y_pred == class_name
            if np.any(mask):
                confidence_by_class[class_name] = confidence[mask]
        
        axes[1, 0].boxplot([confidence_by_class.get(cls, []) for cls in self.classes], 
                          labels=self.classes)
        axes[1, 0].set_xlabel('Predicted Class')
        axes[1, 0].set_ylabel('Prediction Confidence')
        axes[1, 0].set_title('Confidence by Predicted Class')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Probability distribution for each class
        for i, class_name in enumerate(self.classes):
            axes[1, 1].hist(y_proba[:, i], alpha=0.6, label=f'{class_name}', bins=10)
        axes[1, 1].set_xlabel('Predicted Probability')
        axes[1, 1].set_ylabel('Frequency')
        axes[1, 1].set_title('Probability Distribution by Class')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        return confidence
    
    def plot_error_analysis(self, save_path='results/error_analysis.png'):
        """
        Plot error analysis and misclassification patterns
        """
        y_pred = self.model.predict(self.X_test)
        y_proba = self.model.predict_proba(self.X_test)
        
        # Create subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Confusion matrix with percentages
        cm = confusion_matrix(self.y_test, y_pred)
        cm_percent = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis] * 100
        
        im = axes[0, 0].imshow(cm_percent, interpolation='nearest', cmap='Blues')
        axes[0, 0].set_title('Confusion Matrix (Percentages)')
        axes[0, 0].set_xlabel('Predicted')
        axes[0, 0].set_ylabel('Actual')
        
        # Add text annotations
        thresh = cm_percent.max() / 2.
        for i in range(cm_percent.shape[0]):
            for j in range(cm_percent.shape[1]):
                axes[0, 0].text(j, i, f'{cm_percent[i, j]:.1f}%\n({cm[i, j]})',
                               ha="center", va="center",
                               color="white" if cm_percent[i, j] > thresh else "black")
        
        axes[0, 0].set_xticks(range(len(self.classes)))
        axes[0, 0].set_yticks(range(len(self.classes)))
        axes[0, 0].set_xticklabels(self.classes)
        axes[0, 0].set_yticklabels(self.classes)
        
        # 2. Feature importance for misclassified samples
        misclassified_mask = y_pred != self.y_test
        if np.any(misclassified_mask):
            misclassified_indices = np.where(misclassified_mask)[0]
            
            # Get feature importance
            feature_importance = self.model.feature_importances_
            
            axes[0, 1].barh(range(len(self.feature_columns)), feature_importance)
            axes[0, 1].set_yticks(range(len(self.feature_columns)))
            axes[0, 1].set_yticklabels(self.feature_columns)
            axes[0, 1].set_xlabel('Feature Importance')
            axes[0, 1].set_title('Feature Importance (All Samples)')
            axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Prediction probability for misclassified samples
        if np.any(misclassified_mask):
            misclassified_proba = y_proba[misclassified_mask]
            misclassified_true = self.y_test[misclassified_mask]
            misclassified_pred = y_pred[misclassified_mask]
            
            for i, (true_class, pred_class) in enumerate(zip(misclassified_true, misclassified_pred)):
                true_idx = self.classes.index(true_class)
                pred_idx = self.classes.index(pred_class)
                
                axes[1, 0].bar([f'True: {true_class}', f'Pred: {pred_class}'], 
                              [misclassified_proba[i, true_idx], misclassified_proba[i, pred_idx]],
                              alpha=0.7, label=f'Sample {i+1}')
        
        axes[1, 0].set_ylabel('Predicted Probability')
        axes[1, 0].set_title('Prediction Probabilities for Misclassified Samples')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Error rate by class
        error_rates = []
        for class_name in self.classes:
            class_mask = self.y_test == class_name
            if np.any(class_mask):
                class_errors = np.sum((y_pred[class_mask] != self.y_test[class_mask]))
                class_total = np.sum(class_mask)
                error_rate = class_errors / class_total * 100
                error_rates.append(error_rate)
            else:
                error_rates.append(0)
        
        bars = axes[1, 1].bar(self.classes, error_rates, color=['red', 'orange', 'green'])
        axes[1, 1].set_ylabel('Error Rate (%)')
        axes[1, 1].set_title('Error Rate by True Class')
        axes[1, 1].grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, rate in zip(bars, error_rates):
            height = bar.get_height()
            axes[1, 1].text(bar.get_x() + bar.get_width()/2., height + 0.5,
                           f'{rate:.1f}%', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        return misclassified_mask
    
    def plot_cross_validation_scores(self, save_path='results/cross_validation_scores.png'):
        """
        Plot cross-validation scores distribution
        """
        # Perform cross-validation (use 3-fold due to small dataset)
        cv_scores = cross_val_score(self.model, self.X_train, self.y_train, cv=3, scoring='accuracy')
        
        plt.figure(figsize=(12, 8))
        
        # Box plot of CV scores
        plt.subplot(2, 2, 1)
        plt.boxplot(cv_scores, labels=['CV Scores'])
        plt.ylabel('Accuracy Score')
        plt.title('Cross-Validation Scores Distribution')
        plt.grid(True, alpha=0.3)
        
        # Histogram of CV scores
        plt.subplot(2, 2, 2)
        plt.hist(cv_scores, bins=3, alpha=0.7, edgecolor='black')
        plt.xlabel('Accuracy Score')
        plt.ylabel('Frequency')
        plt.title('Cross-Validation Scores Histogram')
        plt.grid(True, alpha=0.3)
        
        # CV scores over folds
        plt.subplot(2, 2, 3)
        plt.plot(range(1, len(cv_scores) + 1), cv_scores, 'o-', linewidth=2, markersize=8)
        plt.axhline(y=cv_scores.mean(), color='red', linestyle='--', label=f'Mean: {cv_scores.mean():.3f}')
        plt.axhline(y=cv_scores.mean() + cv_scores.std(), color='orange', linestyle=':', 
                   label=f'+1 Std: {cv_scores.mean() + cv_scores.std():.3f}')
        plt.axhline(y=cv_scores.mean() - cv_scores.std(), color='orange', linestyle=':', 
                   label=f'-1 Std: {cv_scores.mean() - cv_scores.std():.3f}')
        plt.xlabel('CV Fold')
        plt.ylabel('Accuracy Score')
        plt.title('Cross-Validation Scores by Fold')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Summary statistics
        plt.subplot(2, 2, 4)
        stats_text = f"""
        Mean: {cv_scores.mean():.3f}
        Std: {cv_scores.std():.3f}
        Min: {cv_scores.min():.3f}
        Max: {cv_scores.max():.3f}
        Range: {cv_scores.max() - cv_scores.min():.3f}
        """
        plt.text(0.1, 0.5, stats_text, transform=plt.gca().transAxes, fontsize=12,
                verticalalignment='center', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
        plt.axis('off')
        plt.title('Cross-Validation Statistics')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        return cv_scores
    
    def generate_all_validation_graphs(self):
        """
        Generate all validation and testing graphs
        """
        print("🔄 Loading model and data...")
        self.load_model_and_data()
        
        print("📊 Generating validation and testing graphs...")
        
        # Create results directory
        os.makedirs('results', exist_ok=True)
        
        # Generate all graphs
        print("1. Learning Curve...")
        self.plot_learning_curve()
        
        print("2. Validation Curve (n_estimators)...")
        self.plot_validation_curve('n_estimators')
        
        print("3. ROC Curves...")
        roc_auc = self.plot_roc_curves()
        
        print("4. Precision-Recall Curves...")
        avg_precision = self.plot_precision_recall_curves()
        
        print("5. Prediction Confidence Analysis...")
        confidence = self.plot_prediction_confidence()
        
        print("6. Error Analysis...")
        misclassified = self.plot_error_analysis()
        
        print("7. Cross-Validation Scores...")
        cv_scores = self.plot_cross_validation_scores()
        
        # Print summary
        print("\n✅ All validation and testing graphs generated!")
        print(f"📁 Graphs saved in: results/")
        print(f"🎯 ROC AUC Scores: {roc_auc}")
        print(f"📈 Average Precision: {avg_precision}")
        print(f"🔄 CV Scores Mean: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
        
        return {
            'roc_auc': roc_auc,
            'average_precision': avg_precision,
            'cv_scores': cv_scores,
            'confidence': confidence,
            'misclassified': misclassified
        }


def main():
    """
    Main function to generate all validation and testing graphs
    """
    print("📊 Generating Validation and Testing Graphs")
    print("=" * 50)
    
    # Initialize graph generator
    graph_generator = ValidationTestingGraphs()
    
    # Generate all graphs
    results = graph_generator.generate_all_validation_graphs()
    
    print("\n🎉 Validation and Testing Analysis Complete!")
    print("Check the 'results/' folder for all generated graphs.")
    
    return results


if __name__ == "__main__":
    results = main()
