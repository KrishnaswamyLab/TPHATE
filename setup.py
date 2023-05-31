import os
import sys
from setuptools import setup, find_packages

install_requires = [
    "statsmodels>=0.13.5",
    "pytest>=7.2.1",
    "phate",
    "numpy>=1.16.0",
    "scipy>=1.1.0",
    "scikit-learn==0.24",
    "future",
    "tasklogger>=1.0",
    "graphtools>=1.5.3",
    "scprep>=1.0",
    "matplotlib>=3.0",
    "s_gd2>=1.8.1",
    "pygsp",
    "Deprecated"]


version_py = os.path.join(os.path.dirname(__file__),"tphate", "version.py")
version = open(version_py).read().strip().split("=")[-1].replace('"', "").strip()
print("Loaded version ",version)

if sys.version_info[:2] < (3, 7):
    raise RuntimeError("Python version >=3.7 required.")

readme = open("README.md").read()
setup(
    name="tphate",
    version=version,
    description="tphate",
    author="Erica Busch, Krishnaswamy Lab, Yale University",
    author_email="erica.busch@yale.edu",
    packages=find_packages(),
    python_requires=">=3.7",
    license="GNU General Public License Version 2",
    install_requires=install_requires,
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/KrishnaswamyLab/TPHATE",
    keywords=[
        "visualization",
        "big-data",
        "dimensionality-reduction",
        "embedding",
        "manifold-learning",
        "computational-biology",
        "fmri",
        "computational-neuroscience"
    ],
    classifiers=[
    	"License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python :: 3"
    ],
)

# # get location of setup.py
setup_dir = os.path.dirname(os.path.realpath(__file__))