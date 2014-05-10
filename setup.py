from setuptools import setup, find_packages


setup(
    name='snakerace',
    version='1.0-dev',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'sr-getlines = snakerace.scripts:run_getlines',
            'sr-tournament = snakerace.scripts:run_tournament',
        ]
    }
)
