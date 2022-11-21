from setuptools import find_packages, setup

# TODO: need to figure out what packages to put here

setup(
    name="core",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
    ],
)
