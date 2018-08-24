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
| visible     | | A parameter type that   | Visible.runtime      | | Visible.runtime - used   |
|             | | specifies its features  |                      | | to transfer data from    |
|             | | and visibility in the   |                      | | integrated device or     |
|             | | Alphalogic Studio       |                      | | subsystem into           |
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
| access      | | A parameter access type | Access.read_write    | Access.read_write          |
|             | | which specifies the     |                      |----------------------------|
|             | | permitted and prohibited|                      | Access.read_only           |
|             | | uses of the parameter   |                      |                            |
+-------------+---------------------------+----------------------+----------------------------+
| choices     | | Allows to set up a      | missing              | | The enumeration can be   |
|             | | predefined enumeration  |                      | | specified in one of two  |
|             | | of values for the       |                      | | different ways:          |
|             | | parameter               |                      | | 1) list of values of the |
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

Be careful to assign a value (not an enumeration member's name) to 'default' argument if the 'choices' argument provides enumeration with descriptions:
::
    param_tmp2 = ParameterBool(default=True, choices=((True, 'On'), (False, 'Off')))

Here is the class definition of the class Parameter:

.. autoclass:: Parameter
   :members:

.. _event_link:

Event
~~~~~
| You have to define event, depending on its severity type:
| TrivialEvent, MinorEvent, MajorEvent, CriticalEvent, BlockerEvent

To define an event with arguments, you must append a tuple of (argument name, argument type) pairs. The names of the arguments must be enclosed with single or double quotes.

Example of event definition:
::
   alarm = MajorEvent(('where', unicode), ('when', datetime.datetime), ('why', long))

| The possible value type are:
| unicode – used for string data,
| datetime.datetime – used for date and time,
| long – for integer values,
| float – to store real numbers,
| bool – used for boolean values.

The function that triggers an event occurence (emit) can be passed with the event arguments as a tuple of name/value pairs, each argument name followed by an equal sign:
::
    alarm.emit(where="Red Square, Moscow", when=datetime.datetime(2018, 12, 31), why=123456)

Python allows you to pass functions as a parameters to another functions. In the present case, function can be passed instead of the value for the event argument:
::
    alarm.emit(where="Red Square, Moscow", when=datetime.datetime.utcnow(), why=123456)


Example of event function without arguments:
::
    alarm.clear()


Here is the class definition of the class Event:

.. autoclass:: Event
   :members:


Decorators
----------
A decorator is any callable Python object that is used to modify a function, method or class definition.
A decorator is passed the original object being defined and returns a modified object, which is then bound to the name in the definition.
Decorators are used for creating class methods or static methods, adding function attributes, tracing, setting pre- and postconditions, etc.
The @ special character is used to indicate a decorator.

.. py:module:: alphalogic_api.decorators

.. _command_link:

Command
~~~~~~~
Here is the class definition of the class Command:

.. autoclass:: command
   :members:

run
~~~~~

.. autoclass:: run
   :members:


.. py:module:: alphalogic_api.exceptions

Handlers
-------

The handlers are executed when the corresponding condition occurs.
There are three types of handlers which can be installed to control the workflow of the adapter before or after calling some functions:

1) Request on child objects of the adapter object:
::
    def handle_get_available_children(self):
    return [
        (Controller, 'Controller'),
        (MyObject, 'MyObject')
    ]

You can define and implement this function in the object class to return an array of the child adapter objects.
You must use the exact name of the handler as in the example above.

2) Request on deletion of the adapter object(s):
::
        def handle_before_remove_device(self):
            do something

You can use this handler to do something before the node(s) from the tree of adapter objects will be deleted.
You must use the exact name of the handler as in the example above.

3) Changing the value of the parameter:
::
    def handle_after_set_double(node, parameter):
        node.log.info('double changed')
        node.after_set_value_test_event.emit(value=parameter.val)

    param_double = ParameterDouble(default=2.3, callback=handle_after_set_double)

The handler will be invoked when the specified parameter is changed.
In the example above, this means that the function handle_after_set_double will be called if param_double is changed.
In the case of parameter changes, you can use whichever name of the handler function you like.


Exceptions
----------

.. autoclass:: IncorrectRPCRequest

.. autoclass:: RequestError

.. autoclass:: ComponentNotFound

.. autoclass:: Exit

