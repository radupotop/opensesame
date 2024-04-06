from pathlib import Path
from setuptools import setup, find_packages


def read_requirements(filename):
    contents = Path(filename).read_text().strip('\n')
    return [line for line in contents.split('\n') if not line.startswith('-')]


setup(
    name='OpenSesame',
    version='0.2.0',
    packages=find_packages(),
    install_requires=read_requirements('requirements.txt'),
    extras_require=dict(tests=read_requirements('requirements.test.txt')),
)
