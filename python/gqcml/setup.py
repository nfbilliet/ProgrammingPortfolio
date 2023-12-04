from setuptools import setup, find_packages

__version__ = '0.0.1'
url = 'https://github.com/GQCG/gqcml'

install_requires = [
    'h5py',
    'Keras',
    'numpy',
    'scikit-learn',
    'torch',
    'torch-geometric',
    'torch-scatter',
    'torch-sparse',
    'torch-cluster',
    'torch-spline-conv',
    'pandas',
]
setup_requires = ['pytest-runner']
tests_require = ['pytest', 'pytest-cov', 'mock']

setup(
    name='GQCML',
    version=__version__,
    description='Ghent Quantum Chemistry Machine Learning',
    author='GQCG',
    url=url,
    download_url='{}/archive/{}.tar.gz'.format(url, __version__),
    python_requires='>=3.6',
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    extras_require={'test': tests_require},
    packages=find_packages(),
    include_package_data=True,
)