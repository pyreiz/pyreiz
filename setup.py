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
    version="v0.3.1b1",
    description='A Python toolbox for visual and auditory stimulation based on pyglet and pylsl.',
    long_description=long_description,
    author='Robert Guggenberger',
    author_email='robert.guggenberger@uni-tuebingen.de',
    url='https://github.com/pyreiz/pyreiz',
    download_url='https://github.com/pyreiz/pyreiz.git',
    license='MIT',
    packages=['reiz'],
    entry_points={"console_scripts":
                  ["reiz-marker=reiz.marker.__main__:main"]},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: Software Development :: Libraries',
    ]
)
