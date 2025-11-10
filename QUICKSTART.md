# Quick Start Guide

Follow these steps to publish your DSHelper package:

## 1️⃣ Setup (One-time)

### Create Accounts
- TestPyPI: https://test.pypi.org/account/register/
- PyPI: https://pypi.org/account/register/

### Generate API Tokens
- TestPyPI: https://test.pypi.org/manage/account/#api-tokens
- PyPI: https://pypi.org/manage/account/#api-tokens

Save your tokens securely!

## 2️⃣ Update Package Info

Edit `setup.py` and `pyproject.toml`:
```python
author="YOUR NAME HERE"
author_email="YOUR.EMAIL@example.com"
url="https://github.com/YOURUSERNAME/dshelper"
```

## 3️⃣ Test Your Code

```powershell
# Run tests
.\scripts\test.ps1

# Run quality checks
.\scripts\check.ps1
```

## 4️⃣ Build Package

```powershell
.\scripts\build.ps1
```

## 5️⃣ Test on TestPyPI

```powershell
# Upload to TestPyPI
.\scripts\publish_testpypi.ps1
```
Enter credentials when prompted:
- Username: `__token__`
- Password: Your TestPyPI token

Test installation:
```powershell
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ dshelper
```

## 6️⃣ Publish to PyPI

```powershell
# Upload to PyPI (Production)
.\scripts\publish_pypi.ps1
```
Enter credentials when prompted:
- Username: `__token__`
- Password: Your PyPI token

## 7️⃣ Celebrate! 🎉

Your package is now live:
```bash
pip install dshelper
```

---

## 📚 Need More Details?

See [PUBLISHING_GUIDE.md](PUBLISHING_GUIDE.md) for the complete guide.

## 🆘 Quick Troubleshooting

**"File already exists"** → Increment version number in setup.py

**"Invalid credentials"** → Username must be `__token__`, not your account name

**"Build failed"** → Run: `pip install --upgrade pip build wheel twine`

---

**Your credentials reminder:**
- Username: `__token__` (always this, not your account name!)
- Password: Your API token (starts with `pypi-`)
