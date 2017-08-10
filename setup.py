from setuptools import setup

setup(name='web-extractor',
      version='0.1',
      description='Utils to extract data from webpages content',
      url='http://github.com/merfrei/web-extractor',
      author='Emiliano M. Rudenick',
      author_email='emr.frei@gmail.com',
      license='MIT',
      packages=['extractors'],
      install_requires=[
          'requests',
          'lxml',
          'extruct',
      ],
      zip_safe=False)
