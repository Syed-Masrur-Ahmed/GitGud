from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gitgud-cli",
    version="1.0.1",
    description="AI-powered Git assistant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Syed Masrur Ahmed",
    author_email="ahmedsyedmasrur@gmail.com",
    url="https://github.com/Syed-Masrur-Ahmed/GitGud",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "click>=8.1.0",
        "rich>=13.0.0",
        "GitPython>=3.1.0",
        "requests>=2.31.0",
        "PyYAML>=6.0",
        "inquirer>=3.1.0",
    ],
    entry_points={
        "console_scripts": [
            "gitgud=gitgud.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Version Control :: Git",
    ],
    python_requires=">=3.9",
)
