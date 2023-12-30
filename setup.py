"""
Author            : Nohavye
Author's Email    : noha.poncelet@gmail.com
Repository        : https://github.com/vixen-shell/vixen-client.git
Description       : pip setup file.
License           : GPL3
"""

from setuptools import setup, find_packages

setup(
    name='vixen_api_lib',
    version='0.1a',
    description='Vixen Shell API.',
    packages=find_packages(),
    url='https://github.com/vixen-shell/vixen-api.git',
    license='GPL3',
    author='Nohavye',
    author_email='noha.poncelet@gmail.com',
    python_requires='>=3.11.6',
    install_requires=[
        'annotated-types==0.6.0',
        'anyio==3.7.1',
        'click==8.1.7',
        'fastapi==0.106.0',
        'h11==0.14.0',
        'httptools==0.6.1',
        'idna==3.6',
        'pydantic==2.5.3',
        'pydantic_core==2.14.6',
        'python-dotenv==1.0.0',
        'PyYAML==6.0.1',
        'sniffio==1.3.0',
        'starlette==0.27.0',
        'typing_extensions==4.9.0',
        'uvicorn==0.25.0',
        'uvloop==0.19.0',
        'watchfiles==0.21.0',
        'websockets==12.0'
    ]
)