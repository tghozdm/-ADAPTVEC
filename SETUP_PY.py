 SETUP_PY = """from setuptools import setup, find_packages
 setup(
 name="adaptvec",
 version="1.0.0",
 author="[tolgahan özdemir]",
 description="Word-Specific Dimension Selection for WSD",
 long_description=open("README.md").read(),
 long_description_content_type="text/markdown",
 url="https://github.com/tghozdme/adaptvec",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.21.0",
        "scikit-learn>=1.0.0",
    ],
    license="CC-BY-NC-ND-4.0",
 )
 ""