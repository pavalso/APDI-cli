from setuptools import setup, find_packages


setup(
    name='apdi-blobs-cli',
    version='1.0.0',
    description='CLI for APDI Blobs Service',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'blobs-cli = blobsapdicli.cli:main'
        ]
    }
)
