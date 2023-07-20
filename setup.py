from setuptools import find_packages, setup

setup(
    name='etl_data_crm',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'pyspark',
        'SQLAlchemy',
        'psycopg2'
    ],
    entry_points={
        'console_scripts': [
            'run=src:main'
        ]
    }
)

def run():
    from src import main
    main()