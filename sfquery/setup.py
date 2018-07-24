import setuptools

setuptools.setup(
    name="sfquery",
    version="0.0.18",
    author="Antonio Menarde",
    author_email="amenarde@gmail.com",
    description="A package to query reliable collections in python notebooks",
    url="https://github.com/amenarde/service-fabric-queryable-indexing",
    packages=setuptools.find_packages(),
	install_requires=['xmljson', 'sfctl', 'ipywidgets'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)