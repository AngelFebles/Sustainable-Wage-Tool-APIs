from setuptools import setup

setup(
    name='SustainableWageTool',
    version='1.0.0',
    packages=['SustainableWageTool'],
    install_requires=[  
        'beautifulsoup4==4.12.3',
        'pdfplumber==0.11.4',
        'polars==1.9.0',
        'Requests==2.32.3',
        'selenium==4.25.0',
        'XlsxWriter==3.2.0',
        'fastexcel'
    ],
    author='Angel Febles'
)