from distutils.core import setup

setup(
    name='pq',
    version='0.1',
    packages=['pq'],
    url='',
    license='GPLv3',
    author='granitas',
    author_email='',
    entry_points="""
        [console_scripts]
        pq=pq.cli:cli
    """,
    description='Like jq but with xpath par parsel'
)
