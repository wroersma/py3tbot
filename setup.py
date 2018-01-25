from setuptools import setup

setup(
    name='py3tbot',
    version='0.1.2',
    packages=['tbot', 'tbot.lib', 'lib'],
    package_dir={'': 'tbot/lib'},
    url='https://github.com/wroersma/py3tbot',
    license='GNUv3',
    author='Wyatt Roersma',
    author_email='wyattroersma@gmail.com',
    description='Python3 twitch bot'
)
