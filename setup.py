import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# typing library was introduced as a core module in version 3.5.0
requires = ["dirlistproc", "jsonasobj", "rdflib", "requests"]
if sys.version_info < (3, 5):
    requires.append("typing")

setup(
    name='FHIRShExTest',
    version='1.0.0',
    packages=['src'],
    url='http://github.com/caCDE-QA/FHIRShExTest',
    license='Apache License 2.0',
    author='Harold Solbrig',
    author_email='solbrig.harold@mayo.edu',
    description='FHIR ShEx test script',
    long_description='Test script for evaulating FHIR ShEx resource definitions against FHIR RDF Examples',
    install_requires=requires,
    scripts=['src/FHIRShExTest'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Healthcare Industry',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only']
)
