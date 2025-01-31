from setuptools import find_packages, setup

setup(
    name='adestis-netbox-certificate-management',
    version='1.0.0',
    description='ADESTIS Certificate Management',
    url='https://acme.com',
    author='ADESTIS GmbH',
    author_email='pypi@adestis.de',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    keywords=['netbox', 'netbox-plugin', 'plugin'],
    package_data={
        "adestis_netbox_certificate_management": ["**/*.html"],
        '': ['LICENSE'],
    }
)
