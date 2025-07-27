#!/usr/bin/env python3
"""Setup script for PDF Outline Extractor."""

from setuptools import setup, find_packages

setup(
    name="pdf_outline_extractor",
    version="1.0.0",
    description="A tool to extract structured outlines from PDF documents",
    packages=find_packages(),
    install_requires=[
        "pdfplumber==0.9.0",
        "numpy==1.24.3",
    ],
    python_requires=">=3.7",
    entry_points={
        'console_scripts': [
            'extract-pdf-outline=main:main',
        ],
    },
)
