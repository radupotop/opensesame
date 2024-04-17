from pathlib import Path
from setuptools import setup, find_packages


def read_requirements(filename) -> list:
    reqlist = Path(filename).read_text().splitlines()
    return list(filter(lambda line: '==' in line, reqlist))


setup(
    name='OpenSesame',
    version='0.4.3',
    packages=find_packages(),
    install_requires=read_requirements('requirements.txt'),
    extras_require=dict(tests=read_requirements('requirements.test.txt')),
)
