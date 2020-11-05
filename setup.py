import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup( 
    name='Lotlan_Schedular',
    version='0.1.10', 
    author="Peter Detzner, Maximilian Hörstrup", 
    description="Scheduler for tasks generated from Lotlan files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'antlr4-python3-runtime',
        'tabulate',
        'snakes',
        'networkx',
        'matplotlib'
    ]
)