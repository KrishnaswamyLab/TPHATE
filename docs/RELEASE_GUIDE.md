# TPHATE Pip Distribution Update Guide

This guide provides step-by-step instructions for updating the TPHATE package on PyPI after the dependency cleanup changes.

## Prerequisites

1. **Accounts & Access**
   - PyPI account with upload permissions for the TPHATE package
   - TestPyPI account for testing (recommended)

2. **Tools Installation**
   ```bash
   pip install --upgrade pip setuptools wheel twine
   ```

3. **Authentication Setup**
   ```bash
   # Configure PyPI credentials (one-time setup)
   # Option 1: Use API tokens (recommended)
   # Create API tokens at https://pypi.org/manage/account/token/
   
   # Option 2: Use ~/.pypirc file
   cat > ~/.pypirc << EOF
   [distutils]
   index-servers =
       pypi
       testpypi
   
   [pypi]
   repository = https://upload.pypi.org/legacy/
   username = __token__
   password = pypi-YOUR_API_TOKEN_HERE
   
   [testpypi]
   repository = https://test.pypi.org/legacy/
   username = __token__
   password = pypi-YOUR_TEST_API_TOKEN_HERE
   EOF
   ```

## Pre-Release Checklist

- [ ] All tests pass: `python -m pytest test/ -v`
- [ ] Version updated in `tphate/version.py` (currently 1.2.1)
- [ ] Changelog updated with release notes
- [ ] Dependencies verified in `setup.py` (11 total, phate & scprep removed)
- [ ] Clean workspace (no build artifacts)

## Release Process

### Step 1: Clean Build Environment
```bash
cd /Users/elb/Desktop/code_packages_maintainer_version/TPHATE/TPHATE

# Remove any existing build artifacts
rm -rf build/ dist/ *.egg-info/ .pytest_cache/
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -delete
```

### Step 2: Create Distribution Packages
```bash
# Activate virtual environment if needed
source test_env/bin/activate

# Build source distribution and wheel
python setup.py sdist bdist_wheel

# Verify the build
ls -la dist/
```

Expected output:
```
tphate-1.2.1.tar.gz      # Source distribution
tphate-1.2.1-py3-none-any.whl  # Universal wheel
```

### Step 3: Test the Distribution (Optional but Recommended)

#### Upload to TestPyPI First
```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ tphate==1.2.1

# Verify the test installation
python -c "import tphate; print('Version:', tphate.__version__)"
```

### Step 4: Upload to Production PyPI
```bash
# Upload to production PyPI
twine upload dist/*
```

### Step 5: Verify Production Release
```bash
# Test installation from production PyPI
pip install --upgrade tphate

# Verify installation
python -c "
import tphate
import numpy as np

print('✅ TPHATE Version:', tphate.__version__)

# Quick functionality test
data = np.random.randn(50, 10)
tphate_op = tphate.TPHATE(n_components=2, verbose=False)
embedding = tphate_op.fit_transform(data)
print('✅ Embedding shape:', embedding.shape)
print('✅ Dependencies reduced: phate & scprep removed')
print('✅ Release verification complete!')
"
```

## Post-Release Tasks

### 1. Update Repository Tags
```bash
# Tag the release
git add .
git commit -m "Release v1.2.1: Remove unnecessary PHATE/SCPREP dependencies"
git tag -a v1.2.1 -m "Version 1.2.1 - Dependency cleanup"
git push origin main --tags
```

### 2. Update Documentation
- [ ] Update GitHub README if needed
- [ ] Update documentation site (if applicable)
- [ ] Notify users of breaking changes (if applicable)

### 3. Monitor Release
- [ ] Check PyPI package page: https://pypi.org/project/tphate/
- [ ] Monitor download statistics
- [ ] Watch for user feedback or issues

## Rollback Procedure (if needed)

If issues are discovered after release:

```bash
# Option 1: Quick patch release
# 1. Fix the issue
# 2. Increment version (e.g., 1.2.2)
# 3. Follow release process above

# Option 2: Yank the problematic release (removes from new installs)
# This can only be done through PyPI web interface:
# https://pypi.org/manage/project/tphate/releases/
```

## Key Changes in v1.2.1

**Removed Dependencies:**
- `phate` - Only used in docstring examples
- `scprep>=1.0` - Only used for unused decorator

**Benefits:**
- 15% fewer dependencies (13 → 11 packages)
- Faster installation
- Fewer potential conflicts
- Cleaner dependency tree

**Migration for Users:**
If users need PHATE or SCPREP functionality:
```bash
pip install tphate phate scprep
```

## Troubleshooting

**Common Issues:**

1. **Twine authentication errors:**
   - Verify API tokens are correct
   - Check ~/.pypirc configuration

2. **Version conflicts:**
   - Ensure version in `setup.py` matches `tphate/version.py`
   - Check that version doesn't already exist on PyPI

3. **Build errors:**
   - Verify all dependencies are installed
   - Check `setup.py` syntax
   - Ensure Python version compatibility

4. **Upload permission errors:**
   - Verify PyPI account has upload permissions for TPHATE
   - Check if you're a maintainer of the project

For additional help, consult:
- [PyPI Documentation](https://packaging.python.org/)
- [Twine Documentation](https://twine.readthedocs.io/)
