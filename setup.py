import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    "attrs>=18.1.0",
    "jinja2>=2.10"
]

setuptools.setup(
    name="attrs_to_sql",
    version="0.1.0",
    author="potykion",
    author_email="potykion@gmail.com",
    description="Convert attrs class to CREATE TABLE command.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/potykion/attrs_to_sql",
    install_requires=requirements,
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    include_package_data=True,
)
