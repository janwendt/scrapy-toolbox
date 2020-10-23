import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scrapy-toolbox",
    version="0.0.4",
    author="Jan Wendt",
    description="Saves Scrapy exceptions in your Database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/janwendt/scrapy-toolbox",
    download_url="https://github.com/janwendt/scrapy-toolbox/archive/0.0.4.tar.gz",
    packages=setuptools.find_packages(),
    install_requires=[
          "sqlalchemy",
          "scrapy",
          "numpy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)