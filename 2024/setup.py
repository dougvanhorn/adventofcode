from setuptools import setup

setup(
    name='adventofcode',
    version='2024',
    py_modules=['doit'],
    entry_points={
        'console_scripts': [
            'doit = doit:cli',
        ],
    },
)