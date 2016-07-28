from setuptools import setup, find_packages


setup(
    name='gnss_visualization_tools',
    version="0.1",
    description='GNSS tools',
    author='AM,YD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Beta',
        'Environment :: GNSS',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ],
)
