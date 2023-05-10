from setuptools import setup

setup(name='crawler',
      version='0.1',
      description='Crawls the web',
      url='None',
      author='dslab',
      author_email='dslab-ideias@googlegroups.com',
      license='BSD',
      packages=['crawler'],
      install_requires=[
          'selenium',
          'jsonpickle'
      ],
      zip_safe=False)
