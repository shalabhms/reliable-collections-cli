# -----------------------------------------------------------------------------
# Adapted from Microsoft OSS
# see https://github.com/Microsoft/service-fabric-cli
# -----------------------------------------------------------------------------

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='rcctl',
    version='1.0.2',
    description='Azure Service Fabric Reliable Collections command line',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/shalabhms/reliable-collections-cli',
    author='Antonio Menarde, Shalabh Mohan Shrivastava',
    author_email='amenarde@gmail.com',
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
    keywords='servicefabric azure',
    python_requires='>=2.7,!=3.4,!=3.3,!=3.2,!=3.1,!=3.0,<3.7',
    packages=[
        'rcctl',
        'rcctl.helps'
    ],
    install_requires=[
        'knack==0.1.1',
        'msrest>=0.4.26',
        'msrestazure',
        'requests',
        'azure-servicefabric==6.2.0.0',
        'jsonpickle',
        'adal',
        'future',
	'sfquery>=0.1.0',
        'xmltodict',
        'xmljson',
        'pandas'
    ],
    extras_require={
        'test': [
            'coverage',
            'nose2',
            'pylint',
            'vcrpy',
            'mock',
            'contextlib2'
        ]
    },
    entry_points={
        'console_scripts': ['rcctl=rcctl:launch']
    }
)
