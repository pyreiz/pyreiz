from distutils.core import setup


setup(
    name='Reiz',
    version='0.2.0',
    description='Toolbox for visual and auditory stimulation.',
    long_description='A Python toolbox for visual and auditory stimulation based on pyglet and pylsl.',
    author='Robert Guggenberger',
    author_email='robert.guggenberger@uni-tuebingen.de',
    url='https://github.com/translationalneurosurgery/StimulationFramework/',
    download_url='https://github.com/translationalneurosurgery/StimulationFramework/',
    license='MIT',
    packages=['reiz'],
    install_requires=['pyglet==1.3', "pylsl>=1.13"],
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
