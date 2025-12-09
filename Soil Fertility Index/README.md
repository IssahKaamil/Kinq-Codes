# 🌱 Soil Fertility Index - Advanced GIS & ML Platform

A comprehensive machine learning application that combines advanced Random Forest regression with GIS functionality, user authentication, and real-time soil fertility assessment to provide agricultural recommendations.

## 🚀 Features

- **Advanced Machine Learning**: Random Forest Regressor with hyperparameter tuning and 5-fold cross-validation
- **GIS Integration**: Interactive maps with NDVI, DEM layers, and soil data visualization
- **User Authentication**: Secure login/signup system with session management
- **Automatic Soil Analysis**: Location-based soil data retrieval and fertility assessment
- **Soil Fertility Index (SFI)**: Calculated fertility scores with color-coded categories
- **Comprehensive Recommendations**: AI-powered soil management suggestions with specific application rates
- **Model Evaluation**: Confusion matrix, accuracy graphs, and detailed performance metrics
- **Modern Web Interface**: Clean, responsive design with neutral aesthetics
- **Real-time Analysis**: Instant soil fertility assessment based on nearest soil sample
- **Extended Coverage**: Analyzes locations within 100km of soil samples
- **Data Visualization**: Interactive heatmaps and prediction markers on maps

## 📊 Soil Fertility Categories

| Category | SFI Score | Color | Description |
|----------|-----------|-------|-------------|
| **Excellent** | 80-100 | 🟢 Green | Optimal soil conditions |
| **Good** | 60-79 | 🔵 Blue | Good soil health |
| **Average** | 40-59 | 🟠 Orange | Moderate soil quality |
| **Below Average** | 0-39 | 🔴 Red | Needs improvement |

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Modern web browser with JavaScript enabled

### Setup Steps

1. **Clone or download the project files**
   ```bash
   # Ensure you have these files in your project directory:
   # - soil_fertility_model.py
   # - app.py
   # - soil_nutrients.xlsx
   # - requirements.txt
   # - templates/index.html
   # - templates/login.html
   # - templates/signup.html
   # - templates/logged_out.html
   # - design.json
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify your dataset**
   - Ensure `soil_nutrients.xlsx` is in the project root directory
   - The dataset should contain soil properties and coordinates
   - The application will automatically detect and handle various column name formats

## 🚀 Usage

### 1. Run the Web Application
```bash
python app.py
```
The application will:
- Initialize the user database
- Load or train the machine learning model automatically
- Start a Flask web server
- Open at `http://localhost:5000`

### 2. User Authentication
- **Sign Up**: Create a new account with email and password
- **Login**: Access the application with your credentials
- **Logout**: Secure session termination

### 3. Use the Web Interface

#### **GIS & Mapping Features**
- **Interactive Map**: Leaflet-based map with multiple layers
- **NDVI Layer**: NASA GIBS vegetation index overlay
- **DEM Layer**: Digital Elevation Model from OpenTopoMap
- **Soil Data Points**: Visual representation of all soil samples
- **Prediction Markers**: Color-coded SFI predictions with detailed popups

#### **Location & Analysis**
- **Get My Location**: Click to get your current GPS coordinates
- **Automatic Analysis**: Instantly analyzes soil fertility based on nearest sample data
- **Real-time Predictions**: Live SFI calculations with recommendations

#### **Model Training & Evaluation**
- **Automatic Training**: Model trains on all available data from `soil_nutrients.xlsx`
- **Performance Metrics**: 5-fold cross-validation with comprehensive evaluation
- **Hyperparameter Tuning**: RandomizedSearchCV for optimal model performance
- **Visualization**: Confusion matrix and accuracy graphs saved as images

#### **Analysis Results**
After analysis, you'll see:
- **SFI Score**: Numerical fertility index (0-100)
- **Category**: Color-coded fertility classification (🟢🔵🟠🔴)
- **Specific Recommendations**: Detailed soil management advice with quantities
- **Data Source**: Distance from nearest soil sample
- **Model Performance**: Training and validation metrics

## 🔬 How It Works

### Advanced Machine Learning Pipeline
1. **Data Preprocessing**: Robust column detection and safe data conversion
2. **Feature Engineering**: Automatic categorical variable encoding and normalization
3. **Hyperparameter Tuning**: RandomizedSearchCV optimizes model parameters
4. **Cross-Validation**: 5-fold CV ensures robust model evaluation
5. **Model Training**: Random Forest Regressor with optimal parameters
6. **Prediction**: Real-time soil fertility estimation with confidence metrics

### Soil Fertility Index Calculation
The SFI considers multiple factors with weighted importance:
- **pH (15%)**: Optimal range around 6.5
- **Organic Carbon (15%)**: Higher values improve fertility
- **Organic Matter (15%)**: Essential for soil structure
- **Nitrogen (15%)**: Primary nutrient for plant growth
- **Phosphorus (10%)**: Critical for root development
- **Potassium (10%)**: Important for plant health
- **Calcium (5%)**: Affects soil structure
- **Magnesium (5%)**: Secondary nutrient
- **ECEC (10%)**: Soil's ability to hold nutrients

### GIS Integration & Visualization
- **Location Detection**: Browser geolocation API with fallback options
- **Nearest Neighbor**: Finds closest soil sample within 100km radius
- **Interactive Mapping**: Leaflet.js with multiple overlay layers
- **NDVI Integration**: NASA GIBS vegetation index for environmental context
- **DEM Integration**: Digital elevation data for terrain analysis
- **Heatmap Visualization**: Color-coded soil data representation
- **Prediction Markers**: Real-time SFI predictions with detailed popups

### User Authentication & Security
- **SQLite Database**: Secure user credential storage
- **Password Hashing**: Werkzeug security for password protection
- **Session Management**: Flask session handling with logout functionality
- **Protected Routes**: Login-required access to main application

## 📁 Project Structure

```
Soil Fertility Index/
├── soil_fertility_model.py    # Advanced ML model with hyperparameter tuning
├── app.py                     # Flask web application with authentication
├── soil_nutrients.xlsx        # Soil dataset with coordinates
├── requirements.txt           # Python dependencies
├── design.json               # UI design system configuration
├── templates/
│   ├── index.html            # Main GIS interface
│   ├── login.html            # User login page
│   ├── signup.html           # User registration page
│   └── logged_out.html       # Logout confirmation page
├── static/
│   └── evaluation/           # Model evaluation images (generated)
├── users.db                  # SQLite user database (generated)
├── soil_fertility_model.pkl  # Trained model (generated)
├── confusion_matrix.png      # Model confusion matrix (generated)
├── accuracy_per_fold.png     # Model accuracy graph (generated)
└── README.md                 # This file
```

## 🔧 Customization

### Adding New Soil Properties
1. Update the `calculate_soil_fertility_index()` method in `soil_fertility_model.py`
2. Modify the weights and scoring logic as needed
3. Update the web interface in `templates/index.html`
4. The application automatically detects various column name formats

### Modifying Recommendations
Edit the `get_recommendations()` method in `soil_fertility_model.py` to:
- Add new recommendation criteria
- Adjust threshold values
- Include region-specific advice
- Customize application rates and timing

### Changing the Dataset
- Replace `soil_nutrients.xlsx` with your own data
- Include latitude/longitude coordinates for GIS functionality
- The application handles various column name formats automatically
- Ensure data quality for optimal model performance

### Model Fine-tuning
- Adjust hyperparameter search ranges in `soil_fertility_model.py`
- Modify cross-validation folds for different evaluation strategies
- Customize Random Forest parameters for specific datasets
- Add new evaluation metrics as needed

### UI Customization
- Modify `design.json` for consistent styling changes
- Update color schemes and typography
- Add new GIS layers or modify existing ones
- Customize map interactions and popup content

## 🚨 Troubleshooting

### Common Issues

1. **Model Training Errors**
   - Check that `soil_nutrients.xlsx` exists and is readable
   - Verify data format and column names
   - Ensure no missing values in critical columns
   - Check console logs for specific error messages

2. **Web App Not Starting**
   - Check if port 5000 is available
   - Verify all dependencies are installed: `pip install -r requirements.txt`
   - Check console for error messages
   - Ensure Python 3.8+ is being used

3. **Authentication Issues**
   - Clear browser cookies and try again
   - Check if `users.db` file has proper permissions
   - Verify email format during signup
   - Ensure passwords meet minimum requirements

4. **GIS/Location Issues**
   - Ensure browser has location permissions
   - Check if HTTPS is required (some browsers require secure context)
   - Verify geolocation API support
   - For NDVI layer: ensure zoom level is 9 or lower
   - Check internet connection for external map tiles

5. **Prediction Errors**
   - Ensure all required soil properties are provided
   - Check input value ranges
   - Verify the model file exists and is not corrupted
   - Check if location is within 100km of any soil sample

6. **Map Display Issues**
   - Clear browser cache
   - Check internet connection for map tiles
   - Verify JavaScript is enabled
   - Try different browsers if issues persist

### Performance Optimization
- For large datasets, consider using a subset for training
- Adjust Random Forest parameters in `soil_fertility_model.py`
- Use model caching for faster predictions
- Optimize hyperparameter search ranges for faster tuning

## 📈 Future Enhancements

- **Mobile App**: Native mobile application with offline capabilities
- **Advanced Database**: PostgreSQL/MySQL integration for large-scale data
- **Deep Learning**: Neural networks for improved prediction accuracy
- **Weather Integration**: Real-time climate data integration
- **Crop-Specific Recommendations**: Tailored advice for different crop types
- **Historical Tracking**: Long-term soil health monitoring and trends
- **Multi-language Support**: Internationalization for global users
- **API Development**: RESTful API for third-party integrations
- **Advanced Analytics**: Statistical analysis and reporting features
- **Cloud Deployment**: Scalable cloud infrastructure support

## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 Python style guidelines
- Add comprehensive docstrings to new functions
- Include unit tests for new features
- Update documentation for any API changes
- Test with different datasets and browsers

## 📞 Support

For questions or issues:
1. Check the troubleshooting section above
2. Review the code comments and documentation
3. Search existing issues in the project repository
4. Create a new issue with detailed description and error logs

### Getting Help
- **Documentation**: This README and inline code comments
- **Issues**: GitHub Issues for bug reports and feature requests
- **Discussions**: GitHub Discussions for general questions

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **NASA GIBS**: For providing NDVI satellite imagery
- **OpenTopoMap**: For DEM elevation data
- **Leaflet.js**: For interactive mapping capabilities
- **Scikit-learn**: For machine learning algorithms
- **Flask**: For web framework functionality

---

**Disclaimer**: This application is designed for educational and research purposes. Always consult with agricultural experts and soil scientists for critical farming decisions. The predictions and recommendations should be used as guidance only and not as the sole basis for agricultural practices.
