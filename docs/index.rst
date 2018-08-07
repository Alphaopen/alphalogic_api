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

Example Usage
-------------

Create ``stub.py`` file in the Alphalogic adapter folder.

::

    # -*- coding: utf-8 -*-
    from __future__ import unicode_literals

    from alphalogic_api.attributes import Visible, Access
    from alphalogic_api.objects import Root
    from alphalogic_api.objects import MajorEvent
    from alphalogic_api.objects import ParameterLong
    from alphalogic_api.options import host, port
    from alphalogic_api.decorators import command


    class MyRoot(Root):
        param_int = ParameterLong(default=2, visible=Visible.runtime, access=Access.read_only)
        simple_event = MajorEvent()

        @command(result_type=bool)
        def cmd_alarm(self):
            # do smth
            return True

    # python loop
    root = MyRoot(host, port)
    root.join()

...

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   alphalogic_api
   license


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
