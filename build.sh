#!/bin/bash
rm -rf dist/ &&
rm -rf netbox_certificate_management.egg-info/ &&
rm -rf build/
python setup.py sdist bdist_wheel && 
python -m twine upload dist/* &&
rm -rf dist/ &&
rm -rf netbox_certificate_management.egg-info/ &&
rm -rf build/