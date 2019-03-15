.. _alphalogic_api:

API Documentation
*****************

.. py:module:: alphalogic_api.objects


Objects
=======

.. _root_link:

Root
~~~~
To specify a root object of the user-written adapter, you must create a class that inherits from class Root:
::
    from alphalogic_api.objects import Root
    ......
    class MyRoot(Root):
        ......

.. autoclass:: Root
   :members:

.. _object_link:

Object
~~~~~~
To specify an adapter object (not Root object), create a class that inherits from the class Object:
::
    from alphalogic_api.objects import Object
    ......
    class Controller(Object):
        ......

.. autoclass:: Object
   :members:



.. _parameter_link:

Parameter
~~~~~~~~~
| You have to define parameter, depending on its value type:
| ParameterBool, ParameterLong, ParameterDouble, ParameterDatetime, ParameterString, ParameterList, ParameterDict

Example of parameter definition:
::
    from alphalogic_api.objects import ParameterBool, ParameterLong, ParameterDouble, ParameterDatetime, ParameterString, ParameterList, ParameterDict
    ...

    message = ParameterString(default='Hello world!')

Read and write parameter value:
::
    self.message.val = 'Me too'
    self.param_str.val = self.message.val


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
|             |                           |----------------------|                            |
|             |                           | [] (ParameterList)   |                            |
|             |                           |----------------------|                            |
|             |                           | {} (ParameterDict)   |                            |
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
| choices     | | Allows to set up a      | -                    | | The enumeration can be   |
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
    param_tmp = ParameterLong(visible=Visible.setup, access=Access.read_write, default=1, choices=((1, 'First'), (2, 'Second')))

Second approach to build value list for parameter:
::
    param_tmp = ParameterLong(visible=Visible.setup, access=Access.read_write, default=1, choices=(1, 2))

Be careful to assign a value (not an enumeration member's name) to 'default' argument if the 'choices' argument provides enumeration with descriptions:
::
    param_tmp2 = ParameterBool(default=True, choices=((True, 'On'), (False, 'Off')))

Here is the definition of the class Parameter:

.. autoclass:: Parameter
   :members:

.. _event_link:

Event
~~~~~
| You have to define event, depending on its severity level:
| TrivialEvent, MinorEvent, MajorEvent, CriticalEvent, BlockerEvent

To define an event with arguments, you must append a tuple of (argument name, argument type) pairs. The names of the arguments must be enclosed with single or double quotes.

Example of event definition:
::
   alarm = MajorEvent(('where', unicode), ('when', datetime.datetime), ('why', long))

| The possible value types of the event arguments are:
* unicode – used for string data,
* datetime.datetime – used for date and time,
* long – for integer values,
* float – to store real numbers,
* bool – used for boolean values.

The function that triggers an event occurence (emit) can be passed with the event arguments as a tuple of name/value pairs, each argument name followed by an equal sign:
::
    alarm.emit(where="Red Square, Moscow", when=datetime.datetime(2018, 12, 31), why=123456)

Python allows you to pass functions as a parameters to another functions. In the present case, function can be passed instead of the value for the event argument:
::
    alarm.emit(where="Red Square, Moscow", when=datetime.datetime.utcnow(), why=123456)

Example of the event function without arguments:
::
    alarm.emit()


Here is the definition of the class Event:

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
Possible values for result type are: unicode, datetime.datetime, int, float, bool, list, dict.
Here is the definition of the class Command:

.. autoclass:: command
   :members:


Run functions
~~~~~~~
There is easy way to do some job periodicaly. You can define a lot of run functions in the root or object.

.. autoclass:: run
   :members:


.. py:module:: alphalogic_api.exceptions

Handlers
--------

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

You can use this handler to do something before the adapter object will be deleted.
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

4) Handler for configure Object after creation by user
::
    number = ParameterLong(visible=Visible.setup)
    def handle_defaults_loaded(self, **kwargs):
        self.displayName.val = str(self.number.val)

5) Handler is executed before work of object
::
    number = ParameterLong(visible=Visible.setup)
    def handle_prepare_for_work(self):
        self.displayName.val = str(self.number.val)


Оbject lifetime
~~~~~~~~~~~~~~

Created by user
--------------

1. ``__init__``. You can't do anything with parameters, events, commands here.
2. Create parameters, events, commands
3. Accept values from ``__init__`` kwargs. See `Advanced using` p.1.
4. ``handle_defaults_loaded`` handle
5. ``handle_prepare_for_work`` handle

Loaded from configuration
-----------------------
1. ``__init__``. You can't do anything with parameters, events, commands here.
2. Create parameters, events, commands
3. ``handle_prepare_for_work`` handle

Removed by user
---------------
1. ``handle_before_remove_device``

Advanced using
~~~~~~~~~~~~~~
1) Create a child object with predefault values:
::
    class Controller(Object, DiagHelper):
        some_parameter_title = ParameterLong(default=0)

    def handle_get_available_children(self):
        children = []  # return empty list if exception
        try:
            p = partial(Controller, some_parameter_title=0)
            p.cls = Controller
            children.append((p, 'Controller 0'))

            # You can set parameter values in
            p = partial(Controller, some_parameter_title=1, displayName=h['name'])
            p.cls = Controller
            children.append((p, 'Controller 1'))

        except Exception as err:
            log.error(err.message)
        return children

Handlers order example
----------------------
1) Situation 1: User creates object
::
    class Controller(Object):

        def __init__(self, type_device, id_device, **kwargs):
            super(Controller, self).__init__(type_device, id_device, **kwargs)
            # 1: Partial arguments in the kwargs

        def handle_defaults_loaded(self, **kwargs):
            # 2: Partial arguments in the kwargs

        def handle_prepare_for_work(self):
            # 3: Parameters, commands, events created and have default values

        def handle_before_remove_device(self):
            # remove object by user

2) Situation 2: Object has been loaded from configuration
::
    class Controller(Object):

        def __init__(self, type_device, id_device, **kwargs):
            super(Controller, self).__init__(type_device, id_device, **kwargs)
            # 1: nothing in the kwargs

        def handle_defaults_loaded(self, **kwargs):
            # Not called

        def handle_prepare_for_work(self):
            # 2: Parameters, commands, events created.
            #    Values from configuration loaded.


Exceptions
~~~~~~~~~~~~~~

.. autoclass:: IncorrectRPCRequest

.. autoclass:: RequestError

.. autoclass:: ComponentNotFound

.. autoclass:: Exit

