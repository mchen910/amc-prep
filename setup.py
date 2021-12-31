from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name="amc-prep",
    version="1.0.0",
    description="A prep tool for AMC Competitions",
    license="MIT",
    long_description=long_description,
    author="Matthew Chen",
    author_email="matthewchen910@gmail.com",
    packages=["amc-prep"],
    requires=["beautifulsoup4", "requests", "termcolor", "PyLaTeX"]
)