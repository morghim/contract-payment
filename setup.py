from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in contract_payment/__init__.py
from contract_payment import __version__ as version

setup(
	name="contract_payment",
	version=version,
	description="This app for make payment based on contracts",
	author="Ibrahim Morghim",
	author_email="morghim@outlook.sa",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
