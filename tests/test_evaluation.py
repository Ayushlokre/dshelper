"""
Unit tests for evaluation module
"""

import pytest
import pandas as pd
import numpy as np
from dshelper import evaluation
from sklearn.datasets import make_classification, make_regression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor


class TestQuickEval:
    """Test evaluation.quick_eval function"""
    
    def test_classification_eval(self):
        """Test classification evaluation"""
        y_true = np.array([0, 1, 0, 1, 0, 1, 0, 1])
        y_pred = np.array([0, 1, 0, 0, 0, 1, 1, 1])
        
        metrics = evaluation.quick_eval(
            y_true, y_pred, task_type='classification', show_plot=False
        )
        
        assert 'accuracy' in metrics
        assert 'precision' in metrics
        assert 'recall' in metrics
        assert 'f1_score' in metrics
        assert metrics['accuracy'] > 0
        assert metrics['accuracy'] <= 1
    
    def test_regression_eval(self):
        """Test regression evaluation"""
        y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        y_pred = np.array([1.1, 2.1, 2.9, 4.2, 4.8])
        
        metrics = evaluation.quick_eval(
            y_true, y_pred, task_type='regression', show_plot=False
        )
        
        assert 'r2_score' in metrics
        assert 'rmse' in metrics
        assert 'mae' in metrics
        assert 'mse' in metrics
        assert metrics['r2_score'] > 0.8  # Should be high for this data
    
    def test_auto_detect_task(self):
        """Test automatic task type detection"""
        # Should detect classification
        y_true = np.array([0, 1, 0, 1])
        y_pred = np.array([0, 1, 1, 1])
        
        metrics = evaluation.quick_eval(
            y_true, y_pred, task_type='auto', show_plot=False
        )
        
        assert 'accuracy' in metrics


class TestCompareModels:
    """Test evaluation.compare_models function"""
    
    def test_compare_models(self):
        """Test model comparison"""
        results = {
            'Model1': {'accuracy': 0.85, 'f1': 0.83},
            'Model2': {'accuracy': 0.88, 'f1': 0.86},
            'Model3': {'accuracy': 0.82, 'f1': 0.80}
        }
        
        comparison = evaluation.compare_models(
            results, metric='accuracy', figsize=(8, 5)
        )
        
        assert isinstance(comparison, pd.DataFrame)
        assert len(comparison) == 3
        assert comparison.index[0] == 'Model2'  # Highest accuracy


class TestCrossValSummary:
    """Test evaluation.cross_val_summary function"""
    
    def test_cross_validation(self):
        """Test cross-validation summary"""
        X, y = make_classification(n_samples=100, n_features=10, random_state=42)
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        
        cv_results = evaluation.cross_val_summary(
            model, X, y, cv=3, show_plot=False
        )
        
        assert isinstance(cv_results, pd.DataFrame)
        assert 'mean' in cv_results.columns
        assert 'std' in cv_results.columns


class TestFeatureImportancePlot:
    """Test evaluation.feature_importance_plot function"""
    
    def test_feature_importance(self):
        """Test feature importance plotting"""
        X, y = make_classification(n_samples=100, n_features=10, random_state=42)
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X, y)
        
        feature_names = [f'feature_{i}' for i in range(10)]
        
        importance_df = evaluation.feature_importance_plot(
            model, feature_names, top_n=5
        )
        
        assert isinstance(importance_df, pd.DataFrame)
        assert len(importance_df) == 10
        assert 'Feature' in importance_df.columns
        assert 'Importance' in importance_df.columns


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
