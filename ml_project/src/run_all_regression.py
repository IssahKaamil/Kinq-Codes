"""
Run All Regression Workflows
===========================

This runner:
- Trains and evaluates Random Forest Regressor (with its graphs)
- Trains and evaluates Linear Regression (with its graphs)
- Generates combined comparison graphs (training, testing, performance, evaluation)

Outputs are saved under results/.
"""

import os


def main():
    os.makedirs('results', exist_ok=True)

    # 1) Random Forest regression end-to-end
    from soil_fertility_regressor import main as rf_main
    print('\n=== Running Random Forest Regressor workflow ===')
    rf_regressor, rf_metrics = rf_main()

    # 2) Linear regression end-to-end
    from soil_fertility_linear_regressor import main as lin_main
    print('\n=== Running Linear Regression workflow ===')
    lin_regressor, lin_metrics = lin_main()

    # 3) Combined comparison graphs
    from regression_comparison_plots import generate_all_combined_graphs
    print('\n=== Generating Combined Comparison Graphs ===')
    combined_metrics = generate_all_combined_graphs()

    print('\nAll regression analyses completed. Check the results/ folder for images.')
    return {
        'random_forest': rf_metrics,
        'linear_regression': lin_metrics,
        'combined': combined_metrics
    }


if __name__ == '__main__':
    main()


