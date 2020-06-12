from setuptools import setup

setup(name='slimmer_grpc',
      version='0.1',
      description='Slimmer client/server stubs',
      url='http://github.com/fmarani/slimmer_grpc',
      author='Federico Marani',
      author_email='flagzeta@gmail.com',
      license='MIT',
      packages=['slimmer_grpc'],
      install_requires=[
          'grpcio==1.8.3'
      ],
      zip_safe=False)
