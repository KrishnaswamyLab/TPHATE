#!/usr/bin/env python3
# 
"""
Pre-release verification script for TPHATE v1.2.1
Run this script to verify all changes are correct before releasing to PyPI.

Usage:
    python verify_release.py                    # Run all checks and update pyproject.toml
    python verify_release.py --update-only      # Only update pyproject.toml
    python verify_release.py --no-update        # Run checks without updating pyproject.toml
"""

import sys
import importlib.util
import subprocess
import argparse
from pathlib import Path

def check_version():
    """Check that version is correctly set and accessible."""
    print("🔍 Checking version...")
    
    # Check version.py
    version_file = Path("tphate/version.py")
    if not version_file.exists():
        print("❌ tphate/version.py not found")
        return False
    
    with open(version_file) as f:
        content = f.read()
        if '__version__ = "1.2.1"' not in content:
            print("❌ Version not set to 1.2.1 in version.py")
            return False
    
    # Check that version is importable
    try:
        import tphate
        if tphate.__version__ != "1.2.1":
            print(f"❌ Import version mismatch: {tphate.__version__} != 1.2.1")
            return False
        print("✅ Version 1.2.1 correctly set and importable")
        return True
    except ImportError as e:
        print(f"❌ Cannot import tphate: {e}")
        return False

def check_dependencies():
    """Check that dependencies are correctly cleaned."""
    print("\n🔍 Checking dependencies...")
    
    setup_file = Path("setup.py")
    if not setup_file.exists():
        print("❌ setup.py not found")
        return False
    
    with open(setup_file) as f:
        content = f.read()
        
        # Check removed dependencies
        if '"phate"' in content or "'phate'" in content:
            print("❌ PHATE dependency still present in setup.py")
            return False
            
        if '"scprep' in content or "'scprep" in content:
            print("❌ SCPREP dependency still present in setup.py")
            return False
        
        # Check expected dependencies are present
        expected_deps = [
            "numpy>=1.16.0", "scipy>=1.1.0", "scikit-learn>=0.24",
            "tasklogger>=1.0", "graphtools>=1.5.3", "matplotlib>=3.0",
            "s_gd2>=1.8.1", "pygsp", "Deprecated"
        ]
        
        missing_deps = []
        for dep in expected_deps:
            if dep.split(">=")[0] not in content and dep.split("==")[0] not in content:
                missing_deps.append(dep)
        
        if missing_deps:
            print(f"❌ Missing dependencies: {missing_deps}")
            return False
    
    print("✅ Dependencies correctly cleaned (phate & scprep removed)")
    return True

def check_functionality():
    """Test core TPHATE functionality."""
    print("\n🔍 Testing core functionality...")
    
    try:
        import numpy as np
        import tphate
        
        # Create test data
        np.random.seed(42)
        data = np.random.randn(50, 10)
        
        # Test TPHATE embedding
        tphate_op = tphate.TPHATE(n_components=2, verbose=False)
        embedding = tphate_op.fit_transform(data)
        
        # Check result shape
        if embedding.shape != (50, 2):
            print(f"❌ Embedding shape incorrect: {embedding.shape} != (50, 2)")
            return False
        
        # Check attributes
        required_attrs = ['diff_op', 'autocorr_op', 'phate_diffop']
        for attr in required_attrs:
            if not hasattr(tphate_op, attr):
                print(f"❌ Missing attribute: {attr}")
                return False
        
        print("✅ Core functionality working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def check_tests():
    """Run unit tests."""
    print("\n🔍 Running unit tests...")
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", "test/", "-v", "--tb=short"
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            print("❌ Tests failed:")
            print(result.stdout)
            print(result.stderr)
            return False
        
        print("✅ All tests pass")
        return True
        
    except subprocess.TimeoutExpired:
        print("❌ Tests timed out")
        return False
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        return False

def check_files():
    """Check for clean workspace and required files."""
    print("\n🔍 Checking file status...")
    
    # Check for build artifacts (ignore pytest cache as it's created during testing)
    build_dirs = ["build/", "dist/", "*.egg-info/", "__pycache__/"]
    found_artifacts = []
    
    for pattern in build_dirs:
        if pattern.endswith("/"):
            # Directory check
            if Path(pattern.rstrip("/")).exists():
                found_artifacts.append(pattern)
        else:
            # Glob check
            import glob
            if glob.glob(pattern):
                found_artifacts.extend(glob.glob(pattern))
    
    if found_artifacts:
        print(f"⚠️  Build artifacts found (should clean): {found_artifacts}")
    
    # Check required files
    required_files = [
        "setup.py", "tphate/__init__.py", "tphate/version.py", 
        "docs/CHANGELOG.md", "docs/RELEASE_GUIDE.md", "requirements.txt"
    ]
    
    missing_files = [f for f in required_files if not Path(f).exists()]
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    print("✅ All required files present")
    return len(found_artifacts) == 0

def update_pyproject_toml():
    """Update pyproject.toml with correct version and dependencies from setup.py."""
    print("🔄 Updating pyproject.toml...")
    
    # Read current version from version.py
    version_file = Path("tphate/version.py")
    if not version_file.exists():
        print("❌ tphate/version.py not found")
        return False
    
    with open(version_file) as f:
        version_content = f.read()
        version_line = [line for line in version_content.split('\n') if '__version__' in line]
        if not version_line:
            print("❌ Could not find __version__ in version.py")
            return False
        
        # Extract version string
        version = version_line[0].split('=')[1].strip().strip('"').strip("'")
    
    # Read dependencies from setup.py
    setup_file = Path("setup.py")
    if not setup_file.exists():
        print("❌ setup.py not found")
        return False
    
    with open(setup_file) as f:
        setup_content = f.read()
    
    # Extract install_requires list
    import re
    
    # Find install_requires in setup.py
    install_requires_match = re.search(r'install_requires\s*=\s*\[(.*?)\]', setup_content, re.DOTALL)
    if not install_requires_match:
        print("❌ Could not find install_requires in setup.py")
        return False
    
    # Parse the dependency list
    deps_str = install_requires_match.group(1)
    deps_lines = [line.strip().strip(',').strip('"').strip("'") 
                  for line in deps_str.split('\n') 
                  if line.strip() and not line.strip().startswith('#')]
    dependencies = [dep for dep in deps_lines if dep]
    
    # Read current pyproject.toml
    pyproject_file = Path("pyproject.toml")
    if not pyproject_file.exists():
        print("❌ pyproject.toml not found")
        return False
    
    with open(pyproject_file) as f:
        pyproject_content = f.read()
    
    # Update version in pyproject.toml
    updated_content = re.sub(
        r'version\s*=\s*["\'][^"\']*["\']',
        f'version = "{version}"',
        pyproject_content
    )
    
    # Update build-system requires (build dependencies + runtime dependencies)
    build_requires = [
        '"setuptools>=61.0"',
        '"wheel"'
    ] + [f'"{dep}"' for dep in dependencies]
    
    build_requires_str = ',\n\t'.join(build_requires)
    
    updated_content = re.sub(
        r'requires\s*=\s*\[(.*?)\]',
        f'requires = [\n\t{build_requires_str}\n]',
        updated_content,
        flags=re.DOTALL
    )
    
    # Add dependencies section if it doesn't exist
    if 'dependencies =' not in updated_content:
        # Find the [project] section and add dependencies
        project_section = re.search(r'\[project\]', updated_content)
        if project_section:
            # Find the end of the [project] section
            next_section = re.search(r'\n\[', updated_content[project_section.end():])
            if next_section:
                insert_pos = project_section.end() + next_section.start()
            else:
                insert_pos = len(updated_content)
            
            deps_list = [f'"{dep}"' for dep in dependencies]
            deps_str = ',\n    '.join(deps_list)
            dependencies_section = f'\ndependencies = [\n    {deps_str}\n]\n'
            
            updated_content = (updated_content[:insert_pos] + 
                             dependencies_section + 
                             updated_content[insert_pos:])
    else:
        # Update existing dependencies section
        deps_list = [f'"{dep}"' for dep in dependencies]
        deps_str = ',\n    '.join(deps_list)
        
        updated_content = re.sub(
            r'dependencies\s*=\s*\[(.*?)\]',
            f'dependencies = [\n    {deps_str}\n]',
            updated_content,
            flags=re.DOTALL
        )
    
    # Write updated content back
    with open(pyproject_file, 'w') as f:
        f.write(updated_content)
    
    print(f"✅ Updated pyproject.toml with version {version} and {len(dependencies)} dependencies")
    return True

def check_pyproject_toml():
    """Check that pyproject.toml has correct version and dependencies."""
    print("\n🔍 Checking pyproject.toml...")
    
    pyproject_file = Path("pyproject.toml")
    if not pyproject_file.exists():
        print("❌ pyproject.toml not found")
        return False
    
    with open(pyproject_file) as f:
        pyproject_content = f.read()
    
    # Check version matches
    try:
        import tphate
        expected_version = tphate.__version__
    except ImportError:
        print("❌ Cannot import tphate to check version")
        return False
    
    if f'version = "{expected_version}"' not in pyproject_content:
        print(f"❌ Version in pyproject.toml doesn't match {expected_version}")
        return False
    
    # Check that dependencies section exists
    if 'dependencies =' not in pyproject_content:
        print("❌ dependencies section missing from pyproject.toml")
        return False
    
    # Get dependencies from setup.py for comparison
    setup_file = Path("setup.py")
    with open(setup_file) as f:
        setup_content = f.read()
    
    import re
    install_requires_match = re.search(r'install_requires\s*=\s*\[(.*?)\]', setup_content, re.DOTALL)
    if install_requires_match:
        deps_str = install_requires_match.group(1)
        setup_deps = [line.strip().strip(',').strip('"').strip("'") 
                      for line in deps_str.split('\n') 
                      if line.strip() and not line.strip().startswith('#')]
        setup_deps = [dep for dep in setup_deps if dep]
        
        # Check that all setup.py dependencies are in pyproject.toml
        missing_deps = []
        for dep in setup_deps:
            if f'"{dep}"' not in pyproject_content:
                missing_deps.append(dep)
        
        if missing_deps:
            print(f"❌ Dependencies missing from pyproject.toml: {missing_deps}")
            return False
    
    print("✅ pyproject.toml version and dependencies are correct")
    return True

def main(skip_update=False):
    """Run all verification checks."""
    print("=" * 60)
    print("TPHATE v1.2.1 Pre-Release Verification")
    print("=" * 60)
    
    # First, update pyproject.toml with current version and dependencies
    if not skip_update:
        try:
            if not update_pyproject_toml():
                print("❌ Failed to update pyproject.toml")
                return 1
        except Exception as e:
            print(f"❌ pyproject.toml update failed with exception: {e}")
            return 1
    
    checks = [
        ("Version Check", check_version),
        ("Dependencies Check", check_dependencies),
        ("PyProject.toml Check", check_pyproject_toml),
        ("Functionality Check", check_functionality),
        ("Unit Tests", check_tests),
        ("File Status", check_files),
    ]
    
    all_passed = True
    
    for name, check_func in checks:
        try:
            if not check_func():
                all_passed = False
        except Exception as e:
            print(f"❌ {name} failed with exception: {e}")
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL CHECKS PASSED - Ready for release!")
        if not skip_update:
            print("\nUpdated files:")
            print("- pyproject.toml (version and dependencies synced)")
        print("\nNext steps:")
        print("1. Review docs/CHANGELOG.md")
        print("2. Follow docs/RELEASE_GUIDE.md")
        print("3. Run: python setup.py sdist bdist_wheel")
        print("4. Run: twine upload dist/*")
    else:
        print("❌ SOME CHECKS FAILED - Fix issues before releasing")
        return 1
    
    print("=" * 60)
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="TPHATE Pre-Release Verification and pyproject.toml Update",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python verify_release.py                    # Run all checks and update pyproject.toml
  python verify_release.py --update-only      # Only update pyproject.toml
  python verify_release.py --no-update        # Run checks without updating pyproject.toml
        """
    )
    parser.add_argument("--update-only", action="store_true",
                        help="Only update pyproject.toml without running verification checks")
    parser.add_argument("--no-update", action="store_true",
                       help="Run verification checks without updating pyproject.toml")
    
    args = parser.parse_args()
    
    if args.update_only:
        print("🔄 Updating pyproject.toml only...")
        try:
            if update_pyproject_toml():
                print("✅ pyproject.toml successfully updated!")
                sys.exit(0)
            else:
                print("❌ Failed to update pyproject.toml")
                sys.exit(1)
        except Exception as e:
            print(f"❌ pyproject.toml update failed: {e}")
            sys.exit(1)
    else:
        sys.exit(main(skip_update=args.no_update))
