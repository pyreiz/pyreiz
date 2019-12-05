import setuptools
from distutils.core import setup

# read the contents of README.md
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()
long_description.replace(
    "basic-example.gif",
    "https://raw.githubusercontent.com/pyreiz/pyreiz/master/basic-example.gif",
)


setup(
    name="Reiz",
    version="v0.3.4.1",
    description="A Python toolbox for visual and auditory stimulation based on pyglet and pylsl.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Robert Guggenberger",
    author_email="robert.guggenberger@uni-tuebingen.de",
    url="https://github.com/pyreiz/pyreiz",
    download_url="https://github.com/pyreiz/pyreiz.git",
    license="MIT",
    include_package_data=True,
    package_data={"reiz": ["data/*.*"]},
    packages=setuptools.find_packages(),
    install_requires=["pyglet >= 1.4.7", "pylsl >= 1.13",],
    extras_require={"tts": ["pyttsx3 >= 2.7"]},
    entry_points={"console_scripts": ["reiz-marker=reiz._marker.__main__:main"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Multimedia :: Graphics :: Presentation",
        "Topic :: Multimedia :: Sound/Audio :: Players",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
    ],
)
