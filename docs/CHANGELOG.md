# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.1] - 2025-11-11

### Removed
- **BREAKING**: Removed `phate` dependency from install_requires
  - PHATE was only used in docstring examples, not in actual code
  - Reduces dependency conflicts and installation complexity
- **BREAKING**: Removed `scprep>=1.0` dependency from install_requires  
  - SCPREP was only used for an unused decorator that has been removed
  - Import statement removed from `tphate/mds.py`

### Changed
- Updated `requirements.txt` to remove `phate` dependency for consistency
- Updated `examples/usage.ipynb` with cleaned dependency list
- Updated unit test version assertion from '0.1.0' to '1.2.0'

### Added
- Added `__version__` export to `tphate/__init__.py` for proper version access
- Added comprehensive dependency verification in example notebook

### Fixed
- Fixed version accessibility issue - `tphate.__version__` now works correctly
- Ensured all core functionality works without removed dependencies

### Dependencies
**Before (13 dependencies):**
- statsmodels>=0.13.5, pytest>=7.2.1, numpy>=1.16.0, scipy>=1.1.0, 
- scikit-learn>=0.24, tasklogger>=1.0, graphtools>=1.5.3, matplotlib>=3.0,
- s_gd2>=1.8.1, pygsp, Deprecated, **phate**, **scprep>=1.0**

**After (11 dependencies):**
- statsmodels>=0.13.5, pytest>=7.2.1, numpy>=1.16.0, scipy>=1.1.0,
- scikit-learn>=0.24, tasklogger>=1.0, graphtools>=1.5.3, matplotlib>=3.0,
- s_gd2>=1.8.1, pygsp, Deprecated

### Technical Details
- **Reduction**: 15% fewer dependencies (13 → 11 packages)
- **Compatibility**: 100% backward compatible for core functionality
- **Testing**: All existing functionality verified working
- **Performance**: Faster installation, fewer potential conflicts

### Files Modified
- `setup.py` - Removed phate and scprep from install_requires
- `requirements.txt` - Removed phate dependency  
- `tphate/__init__.py` - Added __version__ export
- `tphate/mds.py` - Removed unused scprep import
- `test/test_tphate.py` - Updated version assertion
- `examples/usage.ipynb` - Updated with cleaned dependencies

### Migration Notes
This is a **breaking change** only for code that directly imported `phate` or `scprep` 
expecting them to be available through TPHATE's dependencies. Core TPHATE functionality 
remains 100% compatible.

If your code requires PHATE or SCPREP, install them separately:
```bash
pip install phate scprep
```
