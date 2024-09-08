# Github: https://github.com/ibehii
# Telegram: https://T.me/dr_xz
# e-mail: BehnamH.dev@gmail.com
# ____________________________________________

from setuptools import setup, find_packages
from pathlib import Path

long_description: str = (Path(__file__).parent / "README.md").read_text()

setup(
        name="Rcolor",
        version='3.0.1',
        description='A library that makes your output colorful in Python',
        long_description=long_description,
        long_description_content_type='text/markdown',
        author='Behnam',
        author_email='Behii@tutanota.com',
        url='https://github.com/ibehii/RandomColorlib',
        license='MIT',
        keywords='Randomly change your output color',
        packages=find_packages(),
        package_data={'' : ['*.json']},
        include_package_data=True,                                                  
        install_requires=['colorama'],
        python_requires='~=3.6',
        classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
        )
