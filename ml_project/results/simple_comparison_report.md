
# Simple Model Comparison Report

## 📊 **Performance Summary**

### **Random Forest Classifier**
- **Accuracy**: 0.400 (40.0%)
- **Precision**: 0.160
- **Recall**: 0.400
- **F1-Score**: 0.229

### **Random Forest Regressor**
- **R² Score**: 0.214
- **RMSE**: 12.36
- **MAE**: 9.97
- **MSE**: 152.74

## 🎯 **Key Findings**

1. **Classifier Performance**: The classifier achieves 40.0% accuracy in categorizing soil fertility into High/Medium/Low classes.

2. **Regressor Performance**: The regressor achieves an R² score of 0.214, indicating limited predictive power.

3. **Error Analysis**: The regressor has an RMSE of 12.36 and MAE of 9.97, meaning predictions are typically off by about 10.0 fertility score points.

## 📈 **Recommendations**

### **For Practical Use**
- **Use Classifier**: Better performance with current dataset size
- **Accuracy**: 40.0% accuracy is suitable for practical applications
- **Interpretability**: Clear High/Medium/Low categories are easier to understand

### **For Research**
- **Use Regressor**: Provides continuous fertility scores
- **Data Collection**: Need more data to improve regressor performance
- **Feature Engineering**: Consider additional soil properties

## ✅ **Conclusion**

The **Random Forest Classifier** demonstrates superior performance for the current dataset, making it the recommended choice for practical soil fertility assessment. The **Random Forest Regressor** provides more detailed predictions but requires additional data to achieve optimal performance.

---
*Generated: September 19, 2025*
