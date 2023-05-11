from setuptools import setup

setup(name='crawler',
      version='0.1',
      description='Python crawler based on Selenium',
      url='None',
      author='Jefry Sastre Perez',
      author_email='jefry.sastre@gmail.com',
      license='MIT',
      packages=['crawler'],
      install_requires=[
          'selenium==3.12.0',
          'jsonpickle'
      ],
      zip_safe=False)
