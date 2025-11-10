"""
Unit tests for missing values module
"""

import pytest
import pandas as pd
import numpy as np
from dshelper import missing


class TestMissingAnalyze:
    """Test missing.analyze function"""
    
    def test_analyze_basic(self):
        """Test basic missing value analysis"""
        df = pd.DataFrame({
            'A': [1, 2, None, 4],
            'B': [1, None, None, 4],
            'C': [1, 2, 3, 4]
        })
        
        report = missing.analyze(df, show_plot=False)
        
        assert len(report) == 2  # Only A and B have missing values
        assert report.iloc[0]['Column'] == 'B'  # B has more missing
        assert report.iloc[0]['Missing_Count'] == 2
        assert report.iloc[0]['Missing_Percent'] == 50.0
    
    def test_analyze_with_threshold(self):
        """Test analysis with threshold"""
        df = pd.DataFrame({
            'A': [1, 2, None, 4],
            'B': [1, None, None, 4],
            'C': [1, 2, 3, 4]
        })
        
        report = missing.analyze(df, threshold=30.0, show_plot=False)
        
        assert len(report) == 1  # Only B has >30% missing
        assert report.iloc[0]['Column'] == 'B'
    
    def test_analyze_no_missing(self):
        """Test with no missing values"""
        df = pd.DataFrame({
            'A': [1, 2, 3, 4],
            'B': [5, 6, 7, 8]
        })
        
        report = missing.analyze(df, show_plot=False)
        
        assert len(report) == 0


class TestQuickSummary:
    """Test missing.quick_summary function"""
    
    def test_quick_summary(self):
        """Test quick summary"""
        df = pd.DataFrame({
            'A': [1, None, 3],
            'B': [1, 2, 3],
            'C': [None, None, None]
        })
        
        summary = missing.quick_summary(df)
        
        assert summary['total_missing'] == 4
        assert summary['total_cells'] == 9
        assert summary['num_columns_with_missing'] == 2
        assert summary['num_complete_columns'] == 1
    
    def test_quick_summary_no_missing(self):
        """Test with no missing values"""
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        
        summary = missing.quick_summary(df)
        
        assert summary['total_missing'] == 0
        assert summary['missing_percentage'] == 0.0


class TestDropMissingColumns:
    """Test missing.drop_missing_columns function"""
    
    def test_drop_columns(self):
        """Test dropping columns above threshold"""
        df = pd.DataFrame({
            'A': [1, 2, 3, 4],
            'B': [1, None, None, None],  # 75% missing
            'C': [1, None, 3, 4]  # 25% missing
        })
        
        df_clean = missing.drop_missing_columns(df, threshold=50.0)
        
        assert 'A' in df_clean.columns
        assert 'B' not in df_clean.columns
        assert 'C' in df_clean.columns


class TestFillMissing:
    """Test missing.fill_missing function"""
    
    def test_fill_mean(self):
        """Test filling with mean"""
        df = pd.DataFrame({'A': [1.0, 2.0, None, 4.0]})
        
        df_filled = missing.fill_missing(df, strategy='mean')
        
        assert not df_filled['A'].isnull().any()
        assert df_filled['A'].iloc[2] == pytest.approx(2.333, rel=0.01)
    
    def test_fill_median(self):
        """Test filling with median"""
        df = pd.DataFrame({'A': [1.0, 2.0, None, 10.0]})
        
        df_filled = missing.fill_missing(df, strategy='median')
        
        assert df_filled['A'].iloc[2] == 2.0
    
    def test_fill_constant(self):
        """Test filling with constant"""
        df = pd.DataFrame({'A': [1, None, 3]})
        
        df_filled = missing.fill_missing(df, strategy='constant', fill_value=999)
        
        assert df_filled['A'].iloc[1] == 999


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
