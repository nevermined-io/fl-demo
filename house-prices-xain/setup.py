#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()

install_requirements = [
    "nevermined-sdk-py==0.7.0",
    "joblib==0.14.1",
    "pandas==1.0.1",
    "py7zr==0.4.4",
    "scikit-learn==0.22.1",
    "scipy==1.4.1",
    "tensorflow==2.5.3",
    "numpy~=1.15",
    "tabulate~=0.8",
    "xain-sdk==0.8.0",
]

# Required to run setup.py:
setup_requirements = []

test_requirements = ["pytest==6.0.2"]

dev_requirements = []

docs_requirements = []

setup(
    author="nevermined-io",
    author_email="root@nevermined.io",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
    ],
    description="🐳 Nevermined Federated Learning Demo",
    extras_require={
        "test": test_requirements,
        "dev": dev_requirements + test_requirements + docs_requirements,
        "docs": docs_requirements,
    },
    install_requires=install_requirements,
    license="Apache Software License 2.0",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="nevermined-fl-demo",
    name="nevermined-fl-demo",
    packages=find_packages(exclude=["tests*"]),
    setup_requires=setup_requirements,
    tests_require=test_requirements,
    url="https://github.com/nevermined-io/fl-demo",
    version="0.1.0",
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "nevermined-fl-demo=nevermined_fl_demo.demo:main",
            "run-participant=nevermined_fl_demo.keras_house_prices.participant:main",
            "split-data=nevermined_fl_demo.keras_house_prices.data_handlers.regression_data:main",
        ]
    },
)
