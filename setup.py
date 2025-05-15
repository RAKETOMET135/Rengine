from setuptools import setup, find_packages

setup(
    name="Rengine",
    version="0.1.0",
    description="Game framework for simple 2D games",
    author="RAKETOMET135",
    packages=find_packages(),
    install_requires=[
        "pygame>=2.0.0",
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Games/Entertainment",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)