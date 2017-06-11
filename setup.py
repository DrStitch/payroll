from setuptools import setup

setup(
    name='payroll',
    packages=['payroll'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)