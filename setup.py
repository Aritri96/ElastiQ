from setuptools import setup, find_packages

setup(
    name="elastiq",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'elastiq=elastiq.main:main',
        ],
    },
    install_requires=[
        'numpy',
    ],
    description="A tool for calculating elastic constants of materials.",
    author="Your Name",
    license="NA",
)
