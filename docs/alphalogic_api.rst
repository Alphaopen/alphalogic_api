.. _alphalogic_api:


API Documentation
=================

.. py:module:: alphalogic_api.objects


Objects
-------

.. _root_link:

Root
~~~~
User's root object must be inherits from class Root:
::
    ...
    from alphalogic_api.objects import Root
    ...
    class MyRoot(Root):
        ...

.. autoclass:: Root
   :members:

.. _object_link:

Object
~~~~~~
Nodes inherits from class Object, except root node:
::
    ...
    from alphalogic_api.objects import Object
    ...
    class Controller(Object):
        ...

.. autoclass:: Object
   :members:

.. _parameter_link:

Parameter
~~~~~~~~~

Parameter is defined in class scope:


.. autoclass:: Parameter
   :members:

.. _event_link:

Event
~~~~~

.. autoclass:: Event
   :members:


Decorators
----------

.. py:module:: alphalogic_api.decorators

.. _command_link:

Command
~~~~~~~

.. autoclass:: command
   :members:

run
~~~~~

.. autoclass:: run
   :members:


.. py:module:: alphalogic_api.exceptions

Exceptions
----------

.. autoclass:: IncorrectRPCRequest

.. autoclass:: RequestError

.. autoclass:: ComponentNotFound

.. autoclass:: Exit

