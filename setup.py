from setuptools import setup, find_packages

setup(
    name='Flask-Security',
    version='1.0',
    url='https://github.com/Sylver11/flask-security',
    license='BSD',
    author='Justus Voigt',
    author_email='connectmaeuse@gmail.com',
    description='User management',
    long_description=__doc__,
    packages=find_packages(),
#    packages=['flask_security'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask==1.1.2',
        'Flask-Blueprint==1.3.0',
        'Flask-login==0.5.0',
        'Flask-SQLAlchemy==2.4.4',
        'Sqlalchemy-utils==0.36.8',
        'Pytest==6.2.2',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
