from setuptools import find_packages, setup
from pathlib import Path

with open("README.md", "r") as f:
    description = f.read()
setup(
    name='adestis_netbox_certificate_management',
    version='1.0.12',
    description='ADESTIS Certificate Management',
    url = 'https://github.com/an-adestis/ADESTIS-Netbox-Certificate-Management',
    author='ADESTIS GmbH',
    author_email='pypi@adestis.de',
    install_requires=['adestis-netbox-applications', 'cert_utils', "josepy"],
    packages=find_packages(),
    include_package_data=True,
    license='GPL-3.0-only',
    keywords=['netbox', 'netbox-plugin', 'plugin'],
    package_data={
        "adestis_netbox_certificate_management": ["**/*.html"],
        '': ['LICENSE'],
    },
    long_description=description,
    long_description_content_type="text/markdown",
)