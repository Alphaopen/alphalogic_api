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
| It will be possible to create types of parameter:
| ParameterBool, ParameterInt, ParameterDouble, ParameterDatetime, ParameterString

Example of using:
::
    hostname = ParameterString(visible=Visible.setup, access=Access.read_write, default='1', choices=('1', '2'))

Arguments of parameter are optional.

.. table:: Values of parameter's arguments

+-------------+----------------------+--------------------------+
| Argument    | Default value        | Possible values          |
+=============+======================+==========================+
| default     | ParameterInt - 0     | | Any values of types    |
|             |----------------------| | are allowed ( for      |
|             | ParameterBool - False| | ParameterDouble is     |
|             |----------------------| | real number)           |
|             | ParameterDouble -0.0 |                          |
|             |----------------------|                          |
|             | ParameterDatetime - 0|                          |
|             |----------------------|                          |
|             | ParameterString - "" |                          |
+-------------+----------------------+--------------------------+
| visible     | Visible.runtime      | Visible.runtime          |
|             |                      |--------------------------|
|             |                      | Visible.setup            |
|             |                      |--------------------------|
|             |                      | Visible.hidden           |
|             |                      |--------------------------|
|             |                      | Visible.common           |
+-------------+----------------------+--------------------------+
| access      | Access.read_write    | Access.read_write        |
|             |                      |--------------------------|
|             |                      | Access.read_only         |
+-------------+----------------------+--------------------------+
| choices     | missing              | | The two possibilities  |
|             |                      | | are allowed.           |
|             |                      | | 1) list of values:     |
|             |                      | | (val1, val2, ...)      |
|             |                      | | 2) list of tuple values|
|             |                      | | with description       |
|             |                      | | ((val1, "desc1"),      |
|             |                      | | (val2, "desc2"))       |
+-------------+----------------------+--------------------------+

| Description of parameter's arguments in constructor:
| 1) default is value of parameter by default
| 2) visible is method of display parameter in admin panel
| 3) access is method of access for user
| 4) choices is predefined values of parameter

In order to use predefined values for parameter need to
use two field default and choices.
::
    param_tmp = ParameterString(default='ster 31', choices=('ster 31', 'ster 25', 'ster 23'))

Case with value with description:
::
    param_tmp2 = ParameterBool(default=True, choices=((True, 'On'), (False, 'Off')))

Class Parameter is defined in class scope:


.. autoclass:: Parameter
   :members:

.. _event_link:

Event
~~~~~
| It will be possible to create types of event:
| TrivialEvent, MinorEvent, MajorEvent, CriticalEvent, BlockerEvent

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

