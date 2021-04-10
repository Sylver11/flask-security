from setuptools import setup

setup(
    name='Flask-Security',
    version='1.0',
    url='https://github.com/Sylver11/flask-security',
    license='BSD',
    author='Your Name',
    author_email='connectmaeuse@gmail.com',
    description='User management',
    long_description=__doc__,
    packages=['flask_security'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
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
