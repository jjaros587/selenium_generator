import setuptools

with open("README.rst", 'r') as f:
    long_description = f.read()

with open("requirements.txt", 'r') as f:
    install_requires = f.readlines()

setuptools.setup(
    name='selenium-generator',
    version='0.3',
    description='A framework for automated generating of Selenim WebDriver tests from yaml based on unittest framework.',
    url="https://github.com/jjaros587/selenium_generator",
    license="MIT",
    long_description=long_description,
    author='Jakub Jaroš',
    author_email='jjaros587@gmail.com',
    packages=setuptools.find_packages(include=['selenium_generator', 'selenium_generator.*']),
    package_data={'selenium_generator': ['../test_runner/template/*.html', '../validators/schemas/*.json']},
    install_requires=install_requires,
    python_requires='>=3.2',
    platforms='any',
    tests_require=["unittest"],
    test_suite="tests",
    keywords=["selenium", "generator"],
    extras_require={
        'testing': ['unittest'],
    }
)
