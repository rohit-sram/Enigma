from setuptools import setup, find_packages

setup(
    name='SE Project',
    version='1.0',
    description='Developed a bot for Software Engineering Course',
    author='Group 86 (Rohit, Adithya, Veera)',
    author_email='rsriram3@ncsu.edu',
    zip_safe=False,
    classifiers=('Development Status :: Development',
                 'Intended Audience :: Engineers',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3.9'),
    tests_require=['pytest'],
    exclude_package_data={
        '': ['.gitignore'],
        'images': ['*.xcf', '*.blend']
    },
)
