"""Sending markers

Sending markers requires a MarkerServer running. This markerserver is used as a man-in-the-middle to forward all markers into an already existing LSLOutlet.
This allows easier recording, reduces computational load on your main script, and prevents forgetting to record a MarkerStream with LabRecorder. It adds a little bit more complexity and a miniscule delay.

You can safeguard your script to make sure a MarkerServer is running in at least these two ways:

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
