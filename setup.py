import os, re, ast, email.utils, sys
from setuptools import setup

here = os.path.dirname(__file__)

with open(os.path.join(here, 'README.rst')) as readme:
	long_description = readme.read()

setup(
	name='prune-ebs-snapshots',
	description='Prune EBS snapshots based on a simple backup retention policy',
	long_description=long_description,
	version='0.3.0',
	url='https://github.com/ammojamo/prune-ebs-snapshots',
	author='James Watmuff',
	author_email='james.watmuff@gmail.com',
	license='Apache2',
	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: System Administrators',
		'License :: OSI Approved :: Apache Software License',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3'
	],
	py_modules=[
		'prune_ebs_snapshots'
	],
	install_requires=[
		'boto3>=1.4.4',
		'pytz>=2017.2',
		'python-dateutil>=2.6.0'
	],
	entry_points={
		'console_scripts': [
			'prune-ebs-snapshots = prune_ebs_snapshots:main'
		]
	}
)
