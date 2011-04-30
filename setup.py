from setuptools import setup, find_packages
 
setup(
    name='django-ipgeobase',
    version='0.1.1',
    description='Django IPGeoBase',
    author='Ildus Kurbangaliev',
    author_email='i.kurbangaliev@gmail.com',
    url='https://gitorious.org/django-ipgeobase',
    packages=find_packages(),
    requires = ['pytils', 'progressbar'],
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
)
