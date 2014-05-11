from setuptools import setup, find_packages


setup(
    name='snakerace',
    version='1.0-dev',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'sr-getlines = snakerace.scripts:run_getlines',
            'sr-break-run-continue = snakerace.scripts:break_run_continue',
            'sr-cat = snakerace.scripts:cat_main',
        ]
    }
)
