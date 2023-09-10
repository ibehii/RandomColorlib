# Github: https://github.com/beh185
# Telegram: https://T.me/dr_xz
# e-mail: BehnamH.dev@gmail.com
# ____________________________________________

from setuptools import setup, find_packages

setup(
        name="Rcolor",
        version='2.0.0',
        description='A library that make your output colorful in python',
        long_description='A library that make your output colorful in python',
        author='Behnam',
        author_email='Behii@tutanota.com',
        url='https://github.com/beh185/RandomColorlib',
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