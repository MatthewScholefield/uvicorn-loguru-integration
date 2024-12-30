from setuptools import setup

setup(
    name='uvicorn-loguru-integration',
    version='0.3.1',
    description='Code to integrate uvicorn.run with Loguru logging',
    url='https://github.com/MatthewScholefield/uvicorn-loguru-integration',
    author='Matthew D. Scholefield',
    author_email='matthew331199@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='uvicorn loguru integration',
    py_modules=['uvicorn_loguru_integration'],
    install_requires=[
        'uvicorn',
        'loguru-logging-intercept'
    ],
)
