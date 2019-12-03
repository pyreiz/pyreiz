"""Sending markers

Sending markers requires a MarkerServer running. This markerserver is used as a man-in-the-middle to forward all markers into an already existing LSLOutlet. 
This MarkerServer opens an Outlet that can be detected independently from the experiments you are running. When you then run an experiment, it receives messages from this experiment, and redistributes them in LSL-format.

LabRecorder can only start recording Outlets that are existing. If you start a MarkerServer immediatly before you run the experiment, there might not be sufficient time for LabRecorder to detect the stream. Certainly, it adds some precious seconds for starting the Outlet, and delays your run.

We recommend to use a reiz-marker-Server as an independent process. Using reiz-marker allows easier recording, reduces computational load on your main script, and can prevent forgetting to record a MarkerStream with LabRecorder. It does though add a little bit more complexity and a miniscule delay.

From the terminal 
-----------------

You can start the MarkerServer as an independent process with `reiz-marker` from your terminal and shut it down gracefull with `reiz-marker --kill`.

.. code-block:: bash

    usage: reiz-marker [-h] [--port PORT] [--host HOST] [--name NAME] [--ping] [--kill]

    Reiz Marker Server

    optional arguments:
    -h, --help   show this help message and exit
    --port PORT  Marker Server port.
    --host HOST  Marker Server host ip.
    --name NAME  Marker Server name.
    --ping       test connection to Markerserver
    --kill       send a poison pill to the Markerserver


From within Python
------------------

Alternatively, :meth:`~.reiz._marker.safeguard.start` starts such a process from within Python, and you can kill it later with :meth:`~.reiz._marker.safeguard.stop`. You can additionally safeguard your script to make sure a MarkerServer is running in at least these two ways:

a) check whether the MarkerServer is avaible, and abort with a notice, if that is not the case.
b) start a throw-away MarkerServer with :meth:`~.start`. 

Sending markers
---------------

There is not much need to push markers for stimuli events manually, as you can create a :class:`~.Cue` and add the desired marker-string during instantiation. Often, you want to send additional information, e.g. the age and id of the subject, or the parameters with which the experiment was run. In these cases, pushing dictionaries or arbitrary strings during initialization of your experiment can be useful.  

.. currentmodule:: reiz._marker.client
.. autosummary::
   :template: module.rst

    push
    push_json



Safeguarding
------------
.. currentmodule:: reiz._marker.safeguard
.. autosummary::
   :template: module.rst

    available
    start
    stop

"""

from reiz._marker.client import push, push_json, available
from reiz._marker.safeguard import start, stop
