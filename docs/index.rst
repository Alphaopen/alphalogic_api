.. alphalogic_api documentation master file, created by
   sphinx-quickstart on Mon Aug 06 17:59:42 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Alphalogic API
==============

The official library for creating the Alphalogic system adapter

Compatibility
-------------

The library is compatible with Alphalogic adapter versions since ``.0315``

The recommended way to set your requirements in your `setup.py` or
`requirements.txt` is::

    # Protobuf
    protobuf==3.6.0

    # gRPC
    grpcio==1.12.1
    grpcio-tools==1.12.1


Installation
------------

Install the ``alphalogic_api`` package with `pip
<https://pypi.python.org/pypi/alphalogic-api>`_::

    pip install alphalogic-api



Overview
-------------
Alphalogic adapter is program in alphalogic platform.
One side's adapter implements described programmed protocol or device(user code via the this library), and
the other side is integrated in alphalogic platform.

Adapter has entities that represent objects(nodes), parameters, events, commands.
Adapter is a tree of objects.

:ref:`object_link` is a unit that has specific technical functions.
Adapter has :ref:`root_link` object is a root of tree.
Other node inherits from class Object.


There are types of interactions with adapter: commands, parameters, and events.

| :ref:`parameter_link`
| Corresponds to a current value of the system object's property.

| :ref:`event_link`
| Corresponds to a state that indicates what has happened with the system object

| :ref:`command_link`
| Corresponds to a state that indicates what has happened with the system object


Example Usage
-------------

Create ``stub.py`` file in the Alphalogic adapter folder.

::

    # -*- coding: utf-8 -*-
    from __future__ import unicode_literals

    from alphalogic_api.attributes import Visible, Access
    from alphalogic_api.objects import Root, Object
    from alphalogic_api.objects import MajorEvent
    from alphalogic_api.objects import ParameterLong
    from alphalogic_api import init
    from alphalogic_api.decorators import command


    class MyRoot(Root):
        param_int = ParameterLong(default=2, visible=Visible.runtime, access=Access.read_only)
        simple_event = MajorEvent()

        def handle_get_available_children(self):
            return [
                (Controller, 'Controller')
            ]

        @command(result_type=bool)
        def cmd_alarm(self):
            # do smth
            return True

    class Controller(Object):

        counter = ParameterLong(default=0)

        @run(period_one=1)
        def run_one(self):
            self.counter.val += 1

        # python loop
    if __name__ == '__main__':
        host, port = init()
        root = MyRoot(host, port)
        root.join()

...

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   alphalogic_api
   abstract_classes
   license


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
