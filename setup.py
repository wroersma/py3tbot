from setuptools import setup
#TODO this doesn't work yet
setup(
    name='py3tbot',
    version='0.1.2',
    packages=['app', 'app.lib', 'lib'],
    package_dir={'': 'app/lib'},
    url='https://github.com/wroersma/py3tbot',
    license='GNUv3',
    author='Wyatt Roersma',
    author_email='wyattroersma@gmail.com',
    description='Python3 twitch bot'
)
