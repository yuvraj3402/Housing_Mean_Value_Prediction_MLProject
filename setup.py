##TO SETUP THE FILE USE "python setup.py install" in the terminal


from setuptools import setup, find_packages



PROJECT_NAME="housing_predictor"
VERSION="0.0.3"
AUTHOR="yuvraj singh"
DESCRIPTION="This is my first proper project"
PACKAGES=["housing"]
REQUIREMENT_FILE_NAME="requirements.txt"

def get_requirements_lists():
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        return requirement_file.readlines().remove("-e .")


setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=get_requirements_lists()
    )
   