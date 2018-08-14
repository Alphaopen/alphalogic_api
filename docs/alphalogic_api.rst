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
| ParameterBool, ParameterLong, ParameterDouble, ParameterDatetime, ParameterString

Example of using:
::
    hostname = ParameterString(visible=Visible.setup, access=Access.read_write, default='1', choices=('1', '2'))

Arguments of parameter are optional.

.. table:: Values of parameter's arguments

+-------------+----------------------+--------------------------+
| Argument    | Default value        | Possible values          |
+=============+======================+==========================+
| default     | ParameterLong - 0    | | Any values of types    |
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

Names and values of arguments are passed by using tuple.
::
   alarm = MajorEvent(('where', unicode), ('when', datetime.datetime), ('why', long))

First value of tuple is name of event's argument , second is type of event's argument.

| List of possible type of arguments to create:
| unicode, datetime.datetime, long, float, bool

Example of event emit:
::
    alarm.emit(where=where, when=when, why=why)

If event without arguments:
::
    alarm.emit()



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

Handlers
-------

Three handlers may be installed by users:

1) Handle for request available children of node:
::
    def handle_get_available_children(self):
    return [
        (Controller, 'Controller')
    ]

This function are should be define for all node who may to create children nodes.

2) A handler that fires after parameter is changed:
::
    def handle_after_set_double(node, parameter):
        node.log.info('double changed')
        node.after_set_value_test_event.emit(value=parameter.val)

    param_double = ParameterDouble(default=2.3, callback=handle_after_set_double)

If param_double is changed, then function handle_after_set_double will be called.

3) A handler that fires before node will be deleted:
::
        def handle_before_remove_device(self):
            do something


Exceptions
----------

.. autoclass:: IncorrectRPCRequest

.. autoclass:: RequestError

.. autoclass:: ComponentNotFound

.. autoclass:: Exit

