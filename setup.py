from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
        name='ssearch',
        version='0.0.1',
        packages=['ssearch'],
        url='https://github.com/xyok/ssearch.git',
        license='MIT',
        author='xyok',
        author_email='xy___ok@163.com',
        description='sougo translate cli tool',
        keywords=['cli', 'translate', "chinese"],
        long_description=long_description,
        long_description_content_type="text/markdown",
        install_requires=[
            'requests'
        ],
        entry_points={
            'console_scripts': [
                's = ssearch.ssearch:main'
            ]
        },
        classifiers=[
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 2.7",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
)
