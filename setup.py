from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="fluid-stratos",
    version="0.1.0",
    author="Máté Róbert",
    author_email="",  # Add your email if desired
    description="A revolutionary cognitive architecture based on fluid dynamics and quantum mechanics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/fluid-stratos",  # Update with your GitHub username
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.950",
        ],
    },
    entry_points={
        "console_scripts": [
            "fluid-stratos=fluid_stratos:main",
        ],
    },
    keywords="artificial-intelligence cognitive-architecture fluid-dynamics quantum-mechanics consciousness ai",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/fluid-stratos/issues",
        "Source": "https://github.com/yourusername/fluid-stratos",
        "Documentation": "https://github.com/yourusername/fluid-stratos/blob/main/README.md",
    },
)
