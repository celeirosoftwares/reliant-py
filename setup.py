from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="reliant-py",
    version="1.0.0",
    author="Celeiro Softwares",
    author_email="hello@reliant.dev",
    description="Official Python SDK for Reliant — LLM Reliability Layer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://reliant.ia.br",
    project_urls={
        "Documentation": "https://reliant.ia.br/docs",
        "Source": "https://github.com/celeirosoftwares/reliant-py",
    },
    py_modules=["reliant"],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords=["reliant", "llm", "ai", "structured-output", "reliability", "anthropic", "openai"],
)
