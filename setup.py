from setuptools import setup, find_packages

setup(
    name='django-enumeration',
    version='0.2.1',
    url='https://github.com/shulcsm/django-enumeration',
    author='Mārtiņš Šulcs',
    author_email='shulcsm@gmail.com',
    packages=find_packages(exclude=['tests*']),
    zip_safe=False,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
    install_requires=[
        'Django>=2.2',
        'django-enumfields==2.0.0'
    ]
)
