# Publishing Guide for DSHelper

This guide will walk you through the complete process of publishing your DSHelper package to TestPyPI and PyPI.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Pre-Publishing Checklist](#pre-publishing-checklist)
3. [Publishing to TestPyPI](#publishing-to-testpypi)
4. [Testing from TestPyPI](#testing-from-testpypi)
5. [Publishing to PyPI](#publishing-to-pypi)
6. [Post-Publishing](#post-publishing)
7. [Troubleshooting](#troubleshooting)

---

## 🔧 Prerequisites

### 1. Create Accounts

#### TestPyPI Account (for testing)
1. Go to [https://test.pypi.org/account/register/](https://test.pypi.org/account/register/)
2. Fill in your details and create an account
3. Verify your email address

#### PyPI Account (for production)
1. Go to [https://pypi.org/account/register/](https://pypi.org/account/register/)
2. Fill in your details and create an account
3. Verify your email address

### 2. Generate API Tokens

#### For TestPyPI:
1. Log in to [https://test.pypi.org](https://test.pypi.org)
2. Go to Account Settings → API tokens
3. Click "Add API token"
4. Name it (e.g., "dshelper-upload")
5. Select "Entire account" for scope
6. Click "Add token"
7. **IMPORTANT**: Copy the token immediately (starts with `pypi-...`)
8. Save it securely - you won't see it again!

#### For PyPI (Production):
1. Log in to [https://pypi.org](https://pypi.org)
2. Go to Account Settings → API tokens
3. Click "Add API token"
4. Name it (e.g., "dshelper-upload")
5. Select "Entire account" for scope
6. Click "Add token"
7. **IMPORTANT**: Copy the token immediately
8. Save it securely

### 3. Install Required Tools

```powershell
# Navigate to your project directory
cd c:\Users\AYUSH\Desktop\Work\Mylib

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

---

## ✅ Pre-Publishing Checklist

Before publishing, make sure you complete these steps:

### 1. Update Package Information

Edit `setup.py` and `pyproject.toml`:
- [ ] Update author name and email
- [ ] Update GitHub repository URL
- [ ] Verify version number (currently 0.1.0)
- [ ] Update description if needed

```python
# In setup.py and pyproject.toml
author="Your Name"  # <- Change this
author_email="your.email@example.com"  # <- Change this
url="https://github.com/yourusername/dshelper"  # <- Change this
```

### 2. Update README.md

- [ ] Replace "Your Name" with your actual name
- [ ] Update contact email
- [ ] Update GitHub URLs
- [ ] Add any additional examples or documentation

### 3. Run Tests

```powershell
# Run all tests with coverage
.\scripts\test.ps1
```

All tests should pass! ✅

### 4. Run Code Quality Checks

```powershell
# Run linting and formatting checks
.\scripts\check.ps1
```

Fix any issues reported by the checks.

### 5. Format Code (if needed)

```powershell
# Auto-format all code
python -m black dshelper/ tests/
```

---

## 🚀 Publishing to TestPyPI

TestPyPI is a separate instance of PyPI for testing. Always publish here first!

### Step 1: Build the Package

```powershell
.\scripts\build.ps1
```

This will:
- Clean previous builds
- Create distribution files in `dist/` folder
- Generate both `.tar.gz` (source) and `.whl` (wheel) files

Expected output:
```
dist/
  ├── dshelper-0.1.0-py3-none-any.whl
  └── dshelper-0.1.0.tar.gz
```

### Step 2: Upload to TestPyPI

```powershell
.\scripts\publish_testpypi.ps1
```

When prompted:
- **Username**: Enter `__token__`
- **Password**: Paste your TestPyPI API token (starts with `pypi-`)

✅ Success! Your package is now on TestPyPI.

---

## 🧪 Testing from TestPyPI

Before publishing to production PyPI, test your package from TestPyPI:

### 1. Create a Test Environment

```powershell
# Create a new virtual environment for testing
python -m venv test_env

# Activate it
.\test_env\Scripts\Activate.ps1

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ dshelper
```

**Note**: The `--extra-index-url https://pypi.org/simple/` is needed because dependencies (numpy, pandas, etc.) are on regular PyPI, not TestPyPI.

### 2. Test Your Package

```python
# Test in Python
python

>>> from dshelper import missing, preprocessing, correlation, evaluation
>>> print("Import successful!")
>>> 
>>> # Quick test
>>> import pandas as pd
>>> df = pd.DataFrame({'A': [1, 2, None, 4], 'B': [5, None, 7, 8]})
>>> report = missing.analyze(df, show_plot=False)
>>> print(report)
```

### 3. Test All Features

Create a test script:

```python
# test_installation.py
from dshelper import missing, preprocessing, correlation, evaluation
import pandas as pd
import numpy as np

print("Testing DSHelper installation...")

# Test 1: Missing values
df = pd.DataFrame({'A': [1, 2, None, 4], 'B': [5, None, 7, 8]})
report = missing.analyze(df, show_plot=False)
print("✓ Missing values module working")

# Test 2: Preprocessing
X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
y = np.array([0, 1, 0, 1])
X_train, X_test, y_train, y_test = preprocessing.split_and_scale(X, y, test_size=0.25)
print("✓ Preprocessing module working")

# Test 3: Evaluation
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=10, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
metrics = evaluation.quick_eval(y_test, y_pred, show_plot=False)
print("✓ Evaluation module working")

print("\n🎉 All tests passed! Package is working correctly.")
```

Run the test:
```powershell
python test_installation.py
```

### 4. Deactivate Test Environment

```powershell
deactivate
```

---

## 🎯 Publishing to PyPI (Production)

Once you've verified everything works on TestPyPI, publish to production PyPI.

### Important Notes Before Publishing

⚠️ **WARNING**: 
- Once published to PyPI, you **cannot** delete or modify a release
- You **cannot** reuse version numbers
- Make absolutely sure everything is correct!

### Step 1: Final Verification

- [ ] Tested on TestPyPI successfully
- [ ] All tests passing
- [ ] Code quality checks passing
- [ ] Documentation is correct
- [ ] Version number is correct

### Step 2: Publish to PyPI

```powershell
.\scripts\publish_pypi.ps1
```

When prompted:
- Confirm you tested on TestPyPI: Enter `y`
- **Username**: Enter `__token__`
- **Password**: Paste your PyPI API token (starts with `pypi-`)
- Final confirmation: Enter `yes`

### Step 3: Verify Publication

1. Visit: [https://pypi.org/project/dshelper/](https://pypi.org/project/dshelper/)
2. Your package should be visible!

---

## 🎉 Post-Publishing

### 1. Install from PyPI

Anyone can now install your package:

```bash
pip install dshelper
```

Test it yourself:
```powershell
# In a new environment
python -m venv prod_test
.\prod_test\Scripts\Activate.ps1
pip install dshelper

# Test import
python -c "from dshelper import missing; print('Success!')"
```

### 2. Share Your Package

Update your README with:
- Installation badge: `[![PyPI version](https://badge.fury.io/py/dshelper.svg)](https://badge.fury.io/py/dshelper)`
- Installation instructions
- Usage examples

### 3. Create a Git Repository (Recommended)

```powershell
# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial release v0.1.0"

# Create GitHub repository and push
git remote add origin https://github.com/yourusername/dshelper.git
git branch -M main
git push -u origin main
```

### 4. Create a Release Tag

```powershell
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0
```

---

## 🔄 Publishing Updates

When you want to release a new version:

### 1. Update Version Number

Edit `setup.py` and `pyproject.toml`:
```python
version="0.2.0"  # Increment version
```

### 2. Update CHANGELOG.md

Document all changes in `CHANGELOG.md`

### 3. Rebuild and Republish

```powershell
# Build
.\scripts\build.ps1

# Test on TestPyPI first
.\scripts\publish_testpypi.ps1

# Then publish to PyPI
.\scripts\publish_pypi.ps1
```

---

## 🐛 Troubleshooting

### Issue: "File already exists"

**Problem**: You're trying to upload a version that already exists.

**Solution**: Increment the version number in `setup.py` and `pyproject.toml`, then rebuild.

### Issue: "Invalid username or password"

**Problem**: API token is incorrect or you're not using `__token__` as username.

**Solution**: 
- Username MUST be exactly `__token__` (not your account username)
- Password MUST be your full API token starting with `pypi-`

### Issue: Import errors after installation

**Problem**: Dependencies not installed correctly.

**Solution**:
```bash
pip install dshelper[dev]  # Install with dev dependencies
# or
pip install numpy pandas scikit-learn matplotlib seaborn  # Install dependencies manually
```

### Issue: "Module not found" when testing

**Problem**: Package not installed in current environment.

**Solution**:
```bash
pip install -e .  # Install in development mode
```

### Issue: Build fails

**Problem**: Missing build dependencies.

**Solution**:
```powershell
python -m pip install --upgrade pip setuptools wheel build
```

---

## 📊 Package Statistics

After publishing, you can track your package:

- **PyPI Stats**: https://pypistats.org/packages/dshelper
- **Downloads**: Check your PyPI project page
- **GitHub Stars**: If you created a repository

---

## 🎓 Best Practices

1. **Always test on TestPyPI first**
2. **Use semantic versioning** (MAJOR.MINOR.PATCH)
3. **Keep CHANGELOG.md updated**
4. **Write comprehensive documentation**
5. **Include usage examples**
6. **Respond to user issues and feedback**
7. **Keep dependencies up to date**
8. **Run tests before every release**

---

## 📞 Support

If you encounter issues:

1. Check the [Python Packaging Guide](https://packaging.python.org/)
2. Visit [PyPI Help](https://pypi.org/help/)
3. Check [TestPyPI](https://test.pypi.org/)

---

## 🎊 Congratulations!

You've successfully published a production-quality Python package!

Your package is now:
- ✅ Available worldwide via `pip install dshelper`
- ✅ Properly documented
- ✅ Tested and production-ready
- ✅ Following Python packaging best practices

**Next Steps**:
- Share your package on social media
- Write a blog post about it
- Submit to awesome-python lists
- Gather user feedback
- Plan new features

Happy packaging! 🚀
