import setuptools

setuptools.setup(
    name="chemistry",
    version="0.0.1",
    description="Library for solving chemistry problems",
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'})