"""
Unit tests for correlation module
"""

import pytest
import pandas as pd
import numpy as np
from dshelper import correlation


class TestHeatmap:
    """Test correlation.heatmap function"""
    
    def test_heatmap_basic(self):
        """Test basic heatmap generation"""
        df = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [2, 4, 6, 8, 10],
            'C': [5, 4, 3, 2, 1]
        })
        
        corr_matrix = correlation.heatmap(df, show_plot=False)
        
        assert isinstance(corr_matrix, pd.DataFrame)
        assert corr_matrix.shape == (3, 3)
        assert corr_matrix.loc['A', 'A'] == 1.0
    
    def test_different_methods(self):
        """Test different correlation methods"""
        df = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [2, 4, 6, 8, 10]
        })
        
        # Pearson
        corr_p = correlation.heatmap(df, method='pearson', show_plot=False)
        assert abs(corr_p.loc['A', 'B']) > 0.9
        
        # Spearman
        corr_s = correlation.heatmap(df, method='spearman', show_plot=False)
        assert abs(corr_s.loc['A', 'B']) > 0.9


class TestTopCorrelations:
    """Test correlation.top_correlations function"""
    
    def test_top_correlations_with_target(self):
        """Test finding top correlations with target"""
        df = pd.DataFrame({
            'target': [1, 2, 3, 4, 5],
            'f1': [2, 4, 6, 8, 10],  # High correlation
            'f2': [5, 4, 3, 2, 1],   # Negative correlation
            'f3': [1, 1, 1, 1, 1]    # No correlation
        })
        
        top_corr = correlation.top_correlations(
            df, target='target', n=2
        )
        
        assert len(top_corr) == 2
        assert 'Feature' in top_corr.columns
        assert 'Correlation' in top_corr.columns
    
    def test_top_correlations_pairwise(self):
        """Test finding top pairwise correlations"""
        df = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [2, 4, 6, 8, 10],
            'C': [1, 1, 1, 1, 1]
        })
        
        top_corr = correlation.top_correlations(df, n=2)
        
        assert len(top_corr) == 2
        assert 'Feature_1' in top_corr.columns
        assert 'Feature_2' in top_corr.columns


class TestRemoveHighlyCorrelated:
    """Test correlation.remove_highly_correlated function"""
    
    def test_remove_correlated_features(self):
        """Test removing highly correlated features"""
        df = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [1.01, 2.01, 3.01, 4.01, 5.01],  # Highly correlated with A
            'C': [5, 4, 3, 2, 1]
        })
        
        df_reduced, removed = correlation.remove_highly_correlated(
            df, threshold=0.99
        )
        
        assert len(removed) > 0
        assert len(df_reduced.columns) < len(df.columns)


class TestCorrelationWithTarget:
    """Test correlation.correlation_with_target function"""
    
    def test_correlation_with_target(self):
        """Test correlation with target variable"""
        X = pd.DataFrame({
            'f1': [1, 2, 3, 4, 5],
            'f2': [2, 4, 6, 8, 10],
            'f3': [5, 4, 3, 2, 1]
        })
        y = pd.Series([1, 2, 3, 4, 5])
        
        correlations = correlation.correlation_with_target(
            X, y, plot=False
        )
        
        assert isinstance(correlations, pd.Series)
        assert len(correlations) == 3
        assert abs(correlations['f1']) > 0.9


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
