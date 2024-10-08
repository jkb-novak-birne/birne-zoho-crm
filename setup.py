from setuptools import setup, find_packages

setup(
    name='birne-zoho-crm',
    version='0.4.0',
    description='A Python library for interacting with Zoho CRM',
    author='Jakub Novák',
    author_email='jakub.novak@birne.com',
    packages=find_packages(),
    install_requires=[
        'zohocrmsdk2-0>=1.0.0'
    ],
)