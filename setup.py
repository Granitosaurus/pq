from distutils.core import setup

setup(
    name='pq',
    version='0.1',
    packages=['pq'],
    url='https://github.com/granitosaurus/pq',
    license='GPLv3',
    author='granitosaurus',
    author_email='bernardas.alisauskas@gmail.com',
    install_requires=[
        'parsel',
        'dicttoxml'
    ],
    entry_points="""
        [console_scripts]
        pq=pq.cli:cli
    """,
    description='Command line xml and json processor for xpath and css selectors.'
)
