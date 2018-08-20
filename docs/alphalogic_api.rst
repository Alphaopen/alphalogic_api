.. _alphalogic_api:


API Documentation
=================

.. py:module:: alphalogic_api.objects


Objects
-------

.. _root_link:

Root
~~~~
To specify a root object of the user-written adapter, you must create a class that inherits from class Root:
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
To specify an adapter object (not Root object), create a class that inherits from the class Object:
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
| All the declarations of the parameters of the adapter object must be placed inside the Object class body.
| You have to define parameter, depending on its value type:
| ParameterBool, ParameterLong, ParameterDouble, ParameterDatetime, ParameterString

Example of parameter definition:
::
    hostname = ParameterString(visible=Visible.setup, access=Access.read_write, default='1', choices=('1', '2'))

Parameter arguments are optional.

.. table:: Parameter arguments

+-------------+---------------------------+----------------------+----------------------------+
| Argument    | Description               | Default Value        | Possible Values            |
+=============+===========================+======================+============================+
| default     | Default parameter value   | 0 (ParameterLong)    | | All the values of the    |
|             |                           |----------------------| | corresponding type are   |
|             |                           | False (ParameterBool)| | allowed (for example,    |
|             |                           |----------------------| | a parameter of           |
|             |                           | 0.0 (ParameterDouble)| | ParameterDouble can      |
|             |                           |----------------------| | hold real numbers)       |
|             |                           | 0 (ParameterDatetime)|                            |
|             |                           |----------------------|                            |
|             |                           | "" (ParameterString) |                            |
+-------------+---------------------------+----------------------+----------------------------+
| visible     | A parameter type that     | Visible.runtime      | | Visible.runtime - used   |
|             | specifies its features    |                      | | to transfer data from    |
|             | and visibility in the     |                      | | integrated device or     |
|             | Alphalogic Studio         |                      | | subsystem into           |
|             |                           |                      | | Alphalogic               |
|             |                           |                      |----------------------------|
|             |                           |                      | | Visible.setup - used to  |
|             |                           |                      | | configure adapter        |
|             |                           |                      | | object's properties      |
|             |                           |                      |----------------------------|
|             |                           |                      | | Visible.hidden - used to |
|             |                           |                      | | store some data that     |
|             |                           |                      | | must be hidden for       |
|             |                           |                      | | target user, e.g.        |
|             |                           |                      | | adapter license key      |
|             |                           |                      |----------------------------|
|             |                           |                      | | Visible.common - a       |
|             |                           |                      | | hybrid of                |
|             |                           |                      | | Visible.runtime and      |
|             |                           |                      | | Visible.setup            |
|             |                           |                      | | parameter types          |
|             |                           |                      | | providing combined       |
|             |                           |                      | | functions                |
+-------------+---------------------------+----------------------+----------------------------+
| access      | A parameter access type   | Access.read_write    | Access.read_write          |
|             | which specifies the       |                      |----------------------------|
|             | permitted and prohibited  |                      | Access.read_only           |
|             | uses of the parameter     |                      |                            |
+-------------+---------------------------+----------------------+----------------------------+
| choices     | Allows to set up a        | missing              | | The enumeration can be   |
|             | predefined enumeration    |                      | | specified in one of two  |
|             | of values for the         |                      | | different ways:          |
|             | parameter                 |                      | | 1) list of values of the |
|             |                           |                      | | corresponding type in a  |
|             |                           |                      | | tuple as (value1,        |
|             |                           |                      | | value2, ..., valueN)     |
|             |                           |                      | | 2) list of enumeration   |
|             |                           |                      | | members in a tuple of    |
|             |                           |                      | | tuples as ((value1,      |
|             |                           |                      | | 'enum_name1'), (value2,  |
|             |                           |                      | | 'enum_name2'), ...,      |
|             |                           |                      | | (value2, 'enum_nameN'))  |
+-------------+---------------------------+----------------------+----------------------------+


To build a value list for the parameter, it is required that both arguments 'choices' and 'default' are specified.
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

