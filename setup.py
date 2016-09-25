try:
    from distutils.core import setup
except ImportError:
    from distutils.core import setup

setup(
    name='seq_pattern_miner',
    version='0.1',
    packages=['seq_pattern_miner'],
    url='https://github.com/project-stark/seq-pattern-miner',
    license='MIT',
    author='Divyesh Peshavaria',
    author_email='divyeshpeshavaria@gmail.com',
    description='A module to find sequential patterns in timestamped sensor data',
    requires=['pymysql']
)
