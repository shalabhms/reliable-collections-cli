import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sfquery",
    version="0.2.0",
    author="Antonio Menarde, Shalabh Mohan Shrivastava",
    author_email="amenarde@gmail.com",
    description="A package to query reliable collections using python or jupyter notebook interfaces",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amenarde/reliable-collections-cli",
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    packages=setuptools.find_packages(),
	install_requires=['xmljson', 'sfctl', 'ipywidgets'],
)