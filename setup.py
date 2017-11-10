from setuptools import setup


setup(
    name='datetimewindow',
    packages=['datetimewindow'],
    version='0.1',
    description='Data type for windows of datetimes.',
    author='JBS',
    author_email='jbs@jbryanscott.com',
    url='https://github.com/jbryanscott/datetimewindow',
    download_url=('https://github.com/'
                  'jbryanscott/datetimewindow/archive/0.1.tar.gz'),
    keywords=['datetime', 'window', 'interval', 'range'],
    install_requires=['dateutil>=2.6.1'],
    classifiers=[],
)
