from setuptools import setup, find_packages

setup(
    name="elastiq",  # Your package name
    version="1.0.0",  # Version of your package
    description="A Python-based tool for calculating elastic constants using stress and strain data",
    author="Your Name",
    author_email="your_email@example.com",
    url="https://github.com/Aritri96/ElastiQ",  # Repository URL
    license="MIT",  # Choose a license (e.g., MIT, Apache-2.0, etc.)
    packages=find_packages(),  # Automatically find all packages
    install_requires=[
        "numpy",  # Add dependencies here
    ],
    entry_points={
        "console_scripts": [
            "elastiq=elastiq.main:main",  # Replace with your module and main function
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version
)
