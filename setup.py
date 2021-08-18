import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="appimage-tools",
    version="0.0.1",
    author="Alexis Lopez Zubieta",
    author_email="contact@azubieta.net",
    description="Manage Type 3 AppImages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "appimage = cli.__main__:main",
        ]
    },
    url="https://github.com/AppImageCrafters/appimage-tools",
    project_urls={
        "Bug Tracker": "https://github.com/AppImageCrafters/appimage-tools/issues",
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "Operating System :: POSIX :: Linux",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    setup_requires="setuptools-pipfile",
    use_pipfile=True,
)
