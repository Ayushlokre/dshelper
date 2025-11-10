"""
Unit tests for preprocessing module
"""

import pytest
import pandas as pd
import numpy as np
from dshelper import preprocessing


class TestSplitAndScale:
    """Test preprocessing.split_and_scale function"""
    
    def test_split_and_scale_basic(self):
        """Test basic split and scale"""
        X = pd.DataFrame({
            'feature1': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'feature2': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        })
        y = pd.Series([0, 1, 0, 1, 0, 1, 0, 1, 0, 1])
        
        X_train, X_test, y_train, y_test = preprocessing.split_and_scale(
            X, y, test_size=0.2, random_state=42
        )
        
        assert len(X_train) == 8
        assert len(X_test) == 2
        assert X_train.shape[1] == 2
        # Check that data is scaled (mean ≈ 0, std ≈ 1)
        assert np.abs(X_train.mean()) < 0.5
    
    def test_different_scalers(self):
        """Test different scaler types"""
        X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
        y = np.array([0, 1, 0, 1])
        
        # Test minmax
        X_train, X_test, _, _ = preprocessing.split_and_scale(
            X, y, test_size=0.25, scaler='minmax', random_state=42
        )
        assert X_train.min() >= 0
        assert X_train.max() <= 1
        
        # Test robust
        X_train, X_test, _, _ = preprocessing.split_and_scale(
            X, y, test_size=0.25, scaler='robust', random_state=42
        )
        assert X_train is not None
        
        # Test none
        X_train, X_test, _, _ = preprocessing.split_and_scale(
            X, y, test_size=0.25, scaler='none', random_state=42
        )
        assert not (np.abs(X_train.mean()) < 0.5)  # Should not be scaled


class TestEncodeCategorical:
    """Test preprocessing.encode_categorical function"""
    
    def test_onehot_encoding(self):
        """Test one-hot encoding"""
        df = pd.DataFrame({
            'category': ['A', 'B', 'A', 'C'],
            'value': [1, 2, 3, 4]
        })
        
        df_encoded = preprocessing.encode_categorical(
            df, columns=['category'], method='onehot'
        )
        
        assert 'category_A' in df_encoded.columns
        assert 'category_B' in df_encoded.columns
        assert 'category_C' in df_encoded.columns
        assert 'category' not in df_encoded.columns
    
    def test_label_encoding(self):
        """Test label encoding"""
        df = pd.DataFrame({'category': ['A', 'B', 'A', 'C']})
        
        df_encoded = preprocessing.encode_categorical(
            df, columns=['category'], method='label'
        )
        
        assert df_encoded['category'].dtype in [np.int64, np.int32]
        assert len(df_encoded['category'].unique()) == 3


class TestHandleOutliers:
    """Test preprocessing.handle_outliers function"""
    
    def test_remove_outliers_iqr(self):
        """Test removing outliers with IQR method"""
        df = pd.DataFrame({
            'A': [1, 2, 3, 4, 5, 6, 7, 8, 9, 100]  # 100 is outlier
        })
        
        df_clean = preprocessing.handle_outliers(
            df, method='iqr', action='remove', threshold=1.5
        )
        
        assert len(df_clean) < len(df)
        assert df_clean['A'].max() < 100
    
    def test_clip_outliers(self):
        """Test clipping outliers"""
        df = pd.DataFrame({
            'A': [1, 2, 3, 4, 5, 6, 7, 8, 9, 100]
        })
        
        df_clipped = preprocessing.handle_outliers(
            df, method='iqr', action='clip'
        )
        
        assert len(df_clipped) == len(df)
        assert df_clipped['A'].max() < 100


class TestFeatureSelectionQuick:
    """Test preprocessing.feature_selection_quick function"""
    
    def test_feature_selection(self):
        """Test quick feature selection"""
        X = pd.DataFrame({
            'f1': [1, 2, 3, 4, 5],
            'f2': [2, 4, 6, 8, 10],
            'f3': [5, 4, 3, 2, 1],
            'noise': [1, 1, 1, 1, 1]
        })
        y = pd.Series([0, 0, 1, 1, 1])
        
        X_selected, selected_features = preprocessing.feature_selection_quick(
            X, y, k=2, method='f_classif'
        )
        
        assert X_selected.shape[1] == 2
        assert len(selected_features) == 2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
