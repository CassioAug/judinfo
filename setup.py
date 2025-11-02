from setuptools import setup

setup(
    name='judinfo-cli',
    version='0.1.0',
    py_modules=['judinfo_cli', 'config'],
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=[
        'click>=8.0.0',
        'requests>=2.25.0',
        'Flask>=2.0.0',
    ],
    entry_points={
        "console_scripts": [
            "judinfo=judinfo_cli:main",
        ],
    },
)