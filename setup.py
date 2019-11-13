import setuptools
from distutils.core import setup
import os
__VERSION__ = os.popen("git describe ----abbrev=0").read().strip()
# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='Reiz',
    version="v0.3.1c5",
    description='A Python toolbox for visual and auditory stimulation based on pyglet and pylsl.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Robert Guggenberger',
    author_email='robert.guggenberger@uni-tuebingen.de',
    url='https://github.com/pyreiz/pyreiz',
    download_url='https://github.com/pyreiz/pyreiz.git',
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=[
                      'pyglet>=1.4',
                      'pylsl'
                     ],
    entry_points={"console_scripts":
                  ["reiz-marker=reiz.marker.__main__:main"]},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Multimedia',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Scientific/Engineering :: Medical Science Apps.'
    ]
)
