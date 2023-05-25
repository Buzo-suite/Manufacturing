from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in manufacturing/__init__.py
from manufacturing import __version__ as version

setup(
	name="manufacturing",
	version=version,
	description="Manufacturing Module",
	author="Buzosuite",
	author_email="info@buzosuite.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
