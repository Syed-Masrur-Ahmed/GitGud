from setuptools import setup, find_packages

setup(
    name="gitgud-cli",
    version="1.0.0",
    description="AI-powered Git assistant",
    author="Your Name",
    author_email="your.email@example.com",
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
    python_requires=">=3.9",
)
