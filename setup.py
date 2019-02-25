# Time-stamp: <2017-08-10>
'''
Copyright (c) 2017, 2018 Chongzhi Zang, Zhenjia Wang <zhenjia@virginia.edu>

This code is free software; you can redistribute it and/or modify it 
under the terms of the BSD License.

@status: release candidate
@version: $Id$
@author: Chongzhi Zang, Zhenjia Wang
@contact: zhenjia@virginia.edu

'''


import os,sys
from setuptools import setup, find_packages
from codecs import open
from os import path
import BART
#command_classes = {}


def main():
    if float(sys.version[:3])<3.0:
        sys.stderr.write("CRITICAL: Python version must be higher than or equal to 3.0!\n")
        sys.exit(1)
        
    setup(name="BART",
          version=BART.__version__,
          description="Binding Analysis for Regulatory Transcription Factors of Genes",
          author='Zhanjia Wang, Chongzhi Zang',
          author_email='zhenjia@virginia.edu, zang@virginia.edu',
          url='',
          #package_dir={'':'BART'},
          packages=find_packages(),#['BART'],
          package_data={'':['bart.conf'],
                        'BART':['hg38_library/*.dat','hg38_library/*.bed','hg38_library/hg38_TF_binding/*.txt','hg38_library/hg38_test_data/*',
                        'mm10_library/*.dat','mm10_library/*.bed','mm10_library/mm10_TF_binding/*.txt','mm10_library/mm10_test_data/*'],},
          #data_files=[('.',['bart.conf'])],
          #include_package_data=True,
          scripts=['bin/bart',],
          classifiers=[
              'Development Status :: 4 - Beta',
              'Environment :: Console',
              'Intended Audience :: Science/Research',
              'License ::',
              'Operating System :: MacOS :: MacOS X',
              'Operating System :: POSIX',
              'Topic :: Scientific/Engineering :: Bio-Informatics',
              'Programming Language :: Python',
              ],
          install_requires=[
              'argparse',
              'configparser',
              'numpy',
              'pandas',
              'scipy',
              'matplotlib',
#              'bz2',
              ],
          #cmdclass = command_classes,
          
          )

if __name__=='__main__': 
    main()         
