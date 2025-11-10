# Example Usage of DSHelper

This notebook demonstrates all features of the DSHelper library.

## Installation

```python
# Install the package
!pip install dshelper
```

## Import Libraries

```python
import pandas as pd
import numpy as np
from dshelper import missing, correlation, preprocessing, evaluation
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
import warnings
warnings.filterwarnings('ignore')
```

## 1. Missing Values Analysis

```python
# Create sample data with missing values
df = pd.DataFrame({
    'age': [25, 30, np.nan, 45, 50, np.nan, 35, 40],
    'salary': [50000, 60000, 70000, np.nan, 90000, 85000, np.nan, 75000],
    'department': ['IT', 'HR', 'IT', np.nan, 'Finance', 'IT', 'HR', 'Finance'],
    'experience': [2, 5, 7, 12, 15, np.nan, 6, 10]
})

print("Original DataFrame:")
print(df)
```

### Analyze Missing Values

```python
# Get comprehensive missing values report
missing_report = missing.analyze(df, show_plot=True)
print("\nMissing Values Report:")
print(missing_report)
```

### Quick Summary

```python
# Get quick summary
summary = missing.quick_summary(df)
print("\nQuick Summary:")
for key, value in summary.items():
    print(f"{key}: {value}")
```

### Fill Missing Values

```python
# Fill numeric columns with median
df_filled = missing.fill_missing(df.copy(), strategy='median', columns=['age', 'salary', 'experience'])

# Fill categorical with mode
df_filled = missing.fill_missing(df_filled, strategy='mode', columns=['department'])

print("\nDataFrame after filling:")
print(df_filled)
```

## 2. Correlation Analysis

```python
# Load breast cancer dataset
data = load_breast_cancer()
df_cancer = pd.DataFrame(data.data, columns=data.feature_names)
df_cancer['target'] = data.target

print(f"Dataset shape: {df_cancer.shape}")
print(f"Features: {len(data.feature_names)}")
```

### Correlation Heatmap

```python
# Create correlation heatmap (first 10 features for visibility)
corr_matrix = correlation.heatmap(
    df_cancer.iloc[:, :10], 
    method='pearson',
    figsize=(10, 8),
    threshold=0.3  # Only show correlations > 0.3
)
```

### Top Correlations with Target

```python
# Find features most correlated with target
top_features = correlation.top_correlations(
    df_cancer, 
    target='target', 
    n=10
)
print("\nTop 10 features correlated with target:")
print(top_features)
```

### Visualize Target Correlations

```python
# Visualize correlations with target
X_cancer = df_cancer.drop('target', axis=1)
y_cancer = df_cancer['target']

correlations = correlation.correlation_with_target(
    X_cancer, 
    y_cancer, 
    plot=True, 
    top_n=15
)
```

### Remove Highly Correlated Features

```python
# Remove multicollinear features
df_reduced, removed_cols = correlation.remove_highly_correlated(
    df_cancer, 
    threshold=0.95
)
print(f"\nOriginal features: {df_cancer.shape[1]}")
print(f"After removing highly correlated: {df_reduced.shape[1]}")
print(f"Removed features: {removed_cols}")
```

## 3. Data Preprocessing

```python
# Prepare data for modeling
X = df_reduced.drop('target', axis=1)
y = df_reduced['target']

print(f"Features shape: {X.shape}")
print(f"Target shape: {y.shape}")
```

### Split and Scale in One Step

```python
# Split data and apply StandardScaler
X_train, X_test, y_train, y_test = preprocessing.split_and_scale(
    X, y,
    test_size=0.2,
    scaler='standard',
    stratify=True,
    random_state=42
)

print(f"\nTrain set: {X_train.shape}")
print(f"Test set: {X_test.shape}")
print(f"Train mean: {X_train.mean():.6f}")
print(f"Train std: {X_train.std():.6f}")
```

### Try Different Scalers

```python
# MinMax Scaler
X_train_mm, X_test_mm, _, _ = preprocessing.split_and_scale(
    X, y, scaler='minmax', random_state=42
)
print(f"\nMinMax - Min: {X_train_mm.min():.2f}, Max: {X_train_mm.max():.2f}")

# Robust Scaler (good for outliers)
X_train_rb, X_test_rb, _, _ = preprocessing.split_and_scale(
    X, y, scaler='robust', random_state=42
)
print(f"Robust - Shape: {X_train_rb.shape}")
```

### Handle Outliers

```python
# Create data with outliers
df_outliers = pd.DataFrame({
    'value1': [1, 2, 3, 4, 5, 100],  # 100 is an outlier
    'value2': [10, 20, 30, 40, 50, 500]  # 500 is an outlier
})

print("Before outlier removal:")
print(df_outliers)

# Remove outliers
df_clean = preprocessing.handle_outliers(
    df_outliers, 
    method='iqr', 
    action='remove'
)

print("\nAfter outlier removal:")
print(df_clean)
```

### Encode Categorical Variables

```python
# Create sample data with categories
df_cat = pd.DataFrame({
    'color': ['red', 'blue', 'red', 'green', 'blue'],
    'size': ['S', 'M', 'L', 'M', 'S'],
    'value': [10, 20, 30, 40, 50]
})

# One-hot encoding
df_encoded = preprocessing.encode_categorical(
    df_cat, 
    columns=['color', 'size'], 
    method='onehot'
)

print("\nOriginal:")
print(df_cat)
print("\nOne-hot encoded:")
print(df_encoded)
```

### Feature Selection

```python
# Quick feature selection
X_selected, selected_features = preprocessing.feature_selection_quick(
    X, y, 
    k=10, 
    method='f_classif'
)

print(f"\nSelected {len(selected_features)} best features:")
print(selected_features)
```

## 4. Model Evaluation

```python
# Train a model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

print("Model trained successfully!")
```

### Quick Evaluation

```python
# Comprehensive evaluation in one line
metrics = evaluation.quick_eval(
    y_test, 
    y_pred, 
    task_type='classification',
    show_plot=True
)

print("\nDetailed Metrics:")
for key, value in metrics.items():
    if key not in ['confusion_matrix', 'classification_report']:
        print(f"{key}: {value}")
```

### Cross-Validation Summary

```python
# Perform cross-validation
cv_results = evaluation.cross_val_summary(
    model, 
    X_train, 
    y_train, 
    cv=5,
    scoring=['accuracy', 'precision', 'recall', 'f1'],
    show_plot=True
)

print("\nCross-Validation Results:")
print(cv_results)
```

### Feature Importance

```python
# Visualize feature importances
importance_df = evaluation.feature_importance_plot(
    model, 
    feature_names=X.columns.tolist(),
    top_n=15,
    figsize=(10, 8)
)

print("\nTop 10 Most Important Features:")
print(importance_df.head(10))
```

### Compare Multiple Models

```python
# Train different models
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

models_results = {}

# Random Forest (already trained)
models_results['Random Forest'] = {
    'accuracy': metrics['accuracy'],
    'precision': metrics['precision'],
    'recall': metrics['recall'],
    'f1_score': metrics['f1_score']
}

# Logistic Regression
lr = LogisticRegression(max_iter=1000, random_state=42)
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)
metrics_lr = evaluation.quick_eval(y_test, y_pred_lr, show_plot=False)
models_results['Logistic Regression'] = {
    'accuracy': metrics_lr['accuracy'],
    'precision': metrics_lr['precision'],
    'recall': metrics_lr['recall'],
    'f1_score': metrics_lr['f1_score']
}

# SVM
svm = SVC(random_state=42)
svm.fit(X_train, y_train)
y_pred_svm = svm.predict(X_test)
metrics_svm = evaluation.quick_eval(y_test, y_pred_svm, show_plot=False)
models_results['SVM'] = {
    'accuracy': metrics_svm['accuracy'],
    'precision': metrics_svm['precision'],
    'recall': metrics_svm['recall'],
    'f1_score': metrics_svm['f1_score']
}

# Compare all models
comparison_df = evaluation.compare_models(
    models_results, 
    metric='accuracy',
    figsize=(12, 6)
)
```

## 5. Complete Pipeline Example

```python
print("="*60)
print("COMPLETE DATA SCIENCE PIPELINE WITH DSHELPER")
print("="*60)

# 1. Load data
from sklearn.datasets import load_iris
iris = load_iris()
df_iris = pd.DataFrame(iris.data, columns=iris.feature_names)
df_iris['target'] = iris.target

# 2. Check missing values
print("\n1. Checking missing values...")
summary = missing.quick_summary(df_iris)
print(f"   Missing values: {summary['total_missing']}")

# 3. Analyze correlations
print("\n2. Analyzing correlations...")
corr_matrix = correlation.heatmap(df_iris, show_plot=False)
top_corr = correlation.top_correlations(df_iris, target='target', n=3)
print(f"   Top 3 correlated features with target:")
for idx, row in top_corr.iterrows():
    print(f"   - {row['Feature']}: {row['Correlation']:.3f}")

# 4. Prepare data
print("\n3. Preparing data...")
X = df_iris.drop('target', axis=1)
y = df_iris['target']

# 5. Split and scale
print("\n4. Splitting and scaling...")
X_train, X_test, y_train, y_test = preprocessing.split_and_scale(
    X, y, test_size=0.2, scaler='standard', stratify=True, random_state=42
)

# 6. Train model
print("\n5. Training model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 7. Evaluate
print("\n6. Evaluating model...")
y_pred = model.predict(X_test)
metrics = evaluation.quick_eval(y_test, y_pred, show_plot=False)
print(f"   Accuracy: {metrics['accuracy']:.4f}")
print(f"   F1 Score: {metrics['f1_score']:.4f}")

# 8. Cross-validation
print("\n7. Cross-validation...")
cv_results = evaluation.cross_val_summary(
    model, X_train, y_train, cv=5, show_plot=False
)
print(f"   CV Accuracy: {cv_results.loc['score', 'mean']:.4f} ± {cv_results.loc['score', 'std']:.4f}")

print("\n" + "="*60)
print("PIPELINE COMPLETED SUCCESSFULLY! 🎉")
print("="*60)
```

## Summary

This example demonstrated:
- ✅ Missing value analysis and handling
- ✅ Correlation analysis and visualization
- ✅ Data preprocessing (scaling, encoding, outliers)
- ✅ Model evaluation and comparison
- ✅ Cross-validation
- ✅ Feature importance
- ✅ Complete end-to-end pipeline

DSHelper makes data science workflows faster and cleaner! 🚀
