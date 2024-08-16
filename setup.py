import os
import distutils.cmd
import subprocess
from setuptools.command.install import install
from setuptools import setup, find_packages

class PylintCommand(install):
    description = 'Check code convention'

    def run(self) -> None:
        install.run(self)
        path = get_current_path()
        os.system(f'sh {path}/run-pylint.sh')

def get_current_path() -> str:
    return os.getcwd().replace(" ", "\ ").replace("(","\(").replace(")","\)")

def read_file(file):
   with open(file) as f:
        return f.read()

def read_requirements(file):
    with open(file) as f:
        return f.read().splitlines()

version = read_file("VERSION")
requirements = read_requirements("requirements.txt")

setup(
    name='agapifa-data-extraction',
    version=version,
    description='Extract data to a file from html source',
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(include=['src']),
    python_requires = ">=3.10",
    cmdclass={
        'lint': PylintCommand,
    },
)
