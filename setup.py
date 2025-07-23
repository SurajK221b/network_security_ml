'''
The setup.py file is an essential part of packaging and 
distributing Python projects. It is used by setuptools 
(or distutils in older Python versions) to define the configuration 
of your project, such as its metadata, dependencies, and more
'''

from setuptools import setup, find_packages
from typing import List

def get_requirements(file_path: str) -> List[str]:
    """
    This function reads a requirements file and returns a list of dependencies.
    It ignores any lines that start with '#', are empty, or contain 'git+'.
    """
    requirement_lst : List[str] = []

    try:
        with open(file_path, 'r') as file:
            # Read each line in the requirements file
            for line in file:
                requirement = line.strip()
                # Ignore empty line and -e .
                if requirement and requirement != '-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print(f"Warning: {file_path} not found. No requirements will be added.")

    return requirement_lst

setup(
    name='NetworkSecurity',
    version='0.1.0',
    author='Suraj Khodade',
    packages=find_packages('requirements.txt'),
    install_requires=get_requirements('requirements.txt')
)

