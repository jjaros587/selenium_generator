import setuptools

with open("README.md", 'r') as f:
    long_description = f.read()

with open("requirements.txt", 'r') as f:
    install_requires = f.readlines()

setuptools.setup(
    name='selenium-generator',
    version='1.0',
    description='A useful module',
    url="https://github.com/jjaros587/selenium_generator",
    license="BSD",
    long_description=long_description,
    author='Jakub Jaroš',
    author_email='jjaros587@gmail.com',
    packages=['selenium_generator'],
    install_requires=install_requires,
    python_requires='>=3.6',
    platforms='any',
    tests_require=["unittest"],
    test_suite="tests",
    keywords=["selenium", "generator"],
    extras_require={
        'testing': ['unittest'],
    }
)
