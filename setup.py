# setup.py

from setuptools import setup, find_packages

# Read the README for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="course-model",
    version="0.1.0",
    author="Nneji Chidi Ben", # Replaced with your name
    author_email="chidiisking7@gmail.com", # Replaced with your email
    description="A lightweight, plug-and-play Python package for universal course modeling.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Chidi09/course-model", # Replaced with your GitHub repo URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Education",
    ],
    python_requires='>=3.7',
    # No external dependencies as per plan
    install_requires=[],
)
