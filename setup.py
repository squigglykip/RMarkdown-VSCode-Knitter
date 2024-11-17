from setuptools import setup, find_packages

setup(
    name="rmd_knitter",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "customtkinter>=5.2.0",
        "pyyaml>=6.0.1",
    ],
    author="squigglykip",
    author_email="",
    description="A GUI tool for knitting R Markdown files in VSCode",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/squigglykip/RMarkdown-VSCode-Knitter",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "rmd-knitter=src.main:main",
        ],
    },
)