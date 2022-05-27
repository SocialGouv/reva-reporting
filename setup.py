from setuptools import setup, find_packages

setup(
    name='reva-reporting',
    version='0.1.0',
    packages=find_packages(),
    url='',
    license='',
    author='Fabien Roussel',
    author_email='fabien.roussel@octo.com',
    description='',
    install_requires=['alembic==1.7.5',
                      'pandas==1.4.2',
                      'psycopg2==2.9.2',
                      'python-dateutil==2.8.2',
                      'python-dotenv==0.19.1',
                      'requests==2.27.1',
                      'sqlalchemy==1.4.36',
                      'structlog==21.5.0',
                      'Unidecode==1.3.4'],

    extras_require={'dev': ['flake8==4.0.1',
                            'flake8-quotes==3.3.1',
                            'freezegun==1.1.0',
                            'pytest==6.2.5']},
    python_requires='>=3.9',
)
