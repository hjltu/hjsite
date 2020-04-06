from setuptools import find_packages, setup

setup(
    name='mysite',
    version='29-may-19',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask_login',
        'pyOpenSSL',
        'Flask-Limiter',
    ],
)
