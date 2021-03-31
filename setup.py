""" SURFtools

.. moduleauthor:: Daniel Weilandt



"""
from setuptools import setup, find_packages

version_tag = '0.0.1'

setup(name='SURFtools',
      version=version_tag,
      author='Daniel R. Weilandt',
      author_email='daniel.r.weilandt@gmail.com',
      url='https://github.com/weilandtd/SURFtools',
      download_url='https://github.com/weilandtd/SURFtools/archive/'+version_tag+'.tar.gz',
      install_requires=['numpy','scipy','matplotlib'
                        ],
      packages = find_packages(),
      python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4',
      description='Toolbox too characterize surface topography features',
      keywords=['surface data','topography','profilometer'],

      license='Apache2',

      # See https://PyPI.python.org/PyPI?%3Aaction=list_classifiers
      classifiers=[
          # How mature is this project? Common values are
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 3 - Alpha',

          # Indicate who your project is intended for
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Surface charaterization',
          'Topic :: Scientific/Engineering :: Surface topography'
          'Environment :: Console',

          # Pick your license as you wish (should match "license" above)
          'License :: OSI Approved :: Apache Software License',

          # Specify the Python versions you support here. In particular, ensure
          # that you indicate whether you support Python 2, Python 3 or both.
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
      ],
      )

