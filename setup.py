from setuptools import setup, find_packages



PROJECT_NAME="housing_predictor"
VERSION="0.0.3"
AUTHOR="yuvraj singh"
DESCRIPTION="This is my first proper project"
PACKAGES=["housing"]


setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    packages=find_packages()
)