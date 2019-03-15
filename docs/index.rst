.. alphalogic_api documentation master file, created by
   sphinx-quickstart on Mon Aug 06 17:59:42 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

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

Alphalogic API
==============

The Alphalogic API is an official library that provides developers with the tools for creating the Alphalogic system adapters in Python 2.

Compatibility
-------------

The library is compatible with Alphalogic adapters versions since ``.0315``.

Installation
------------

To install the ``alphalogic_api`` package with `pip
<https://pip.pypa.io/>`_, run this command in your terminal::
    pip install alphalogic-api

If you don't have pip installed, this `Python installation guide
<http://docs.python-guide.org/en/latest/starting/installation/>`_ can guide you through the process.

Dependencies
-------------

To start using this library you need the Alphalogic Service Manager (ASM) to be installed on your machine. Additionally, you also need the composite Alphalogic adapter (probably, engine) to be installed to provide a "shell" for your code to run in.
You can define the required dependencies by editing the 'requirements' parameter in the [pip] section in the ``stub.win32.ini`` file (for Windows) or ``stub.linux.ini`` file (for Linux). Navigate to the ``\bin`` folder of the installed composite Alphalogic adapter, and open appropriate file to edit.
After saving this file, you can access the necessary libraries via the ASM: go to Infrastructure > Adapters page, download and install the specific dependencies by clicking on the install button for the deployed adapter.

Overview
-------------
| Alphalogic adapter is a program for integrating third-party utilities/devices/subsystems/protocols into Alphalogic software platform. In the operating system, adapter runs as a stand-alone process and may be installed as a system service.
| Three types of adapters can be distinguished by the way they are generated:
* traditional C++ adapters;
* composite adapters of two different parts: a relatively unchangeable program core written in C++, supplemented by gRPC stub containing application-specific program code which can be written in almost any programming language (C++, Python, Go!, JavaScript, etc.).
* Java adapters.

The alphalogic_api library allows to access Alphalogic Integration API for easily developing composite adapters in Python 2, providing the integration developer with opportunity to code at once the functional part of the adapter, knowing nothing about the core.

Every adapter has a tree-like structure of the adapter objects represented as a set of linked nodes. The object tree has a Root object which will be generated automatically after the adapter instance is started, and a number of parent/child objects forming the object architecture of the adapter.

:ref:`object_link` is a unit that has specific information and/or implements the necessary technical functions of the integrated device/subsystem.
:ref:`root_link` object is a root node of the adapter object tree. Usually serves for specifying initial device/subsystem data or defining connection settings or just as a go-between node. Root object cannot be deleted separately from the adapter instance.
All other objects (not Root) – subobjects (dependent objects) – are inherited from class :ref:`object_link`.

Every adapter object has a name and a defined set of the specific types of interactions – parameters, events, and commands – which determine its behaviour in the adapter.

| :ref:`parameter_link`
| Represents a property or state of the adapter object. Each parameter has a name, (visible) type, value type and access type.

| :ref:`event_link`
| Corresponds to a state that indicates what has happened with the object. Each event has a severity level associated with it. Some types of events may have arguments.

| :ref:`command_link`
| A simple operation an object can perform. Some types of commands may have arguments. The command execution may trigger some event or affects the change of some parameter value.


Usage
-------------

Navigate to the ``\bin`` folder of the installed composite Alphalogic adapter and open ``stub.py`` file to edit. It contains the following code:
::

   # -*- coding: utf-8 -*-
   from __future__ import unicode_literals

   from alphalogic_api.objects import Root, Object
   from alphalogic_api.attributes import Visible, Access
   from alphalogic_api.objects import MajorEvent
   from alphalogic_api.objects import ParameterBool, ParameterLong, ParameterDouble, ParameterDatetime, ParameterString, ParameterList, ParameterDict
   from alphalogic_api.decorators import command, run
   from alphalogic_api.logger import log


   class Engine(Root):
      pass


   if __name__ == '__main__':
      # main loop
      root = Engine()
      root.join()

In the beginning of the file, there is a line of the unicode_literals import, which makes all string literals of unicode type, instead of string type.
Then come import statements for the classes probably required by the code of the adapter.
Below, there is a declaration of the class Engine to implement the default root object, designed to be changed as needed.
Finally, you can see an “if__name__== “__main__” block used to run ``stub.py`` as a standalone program which cannot be imported as a reusable module.
In the act of writing Python code, you should follow the coding conventions, `PEP-8
<https://www.python.org/dev/peps/pep-0008/>`_.

Example Usage
-------------

The use of the library can be demonstrated via the following example of the SendMail Adapter:
::

   # -*- coding: utf-8 -*-
   from __future__ import unicode_literals

   import smtplib

   from email.MIMEMultipart import MIMEMultipart
   from email.MIMEText import MIMEText

   from operator import methodcaller

   from alphalogic_api import options
   from alphalogic_api.objects import Root, Object
   from alphalogic_api.attributes import Visible, Access
   from alphalogic_api.objects import ParameterBool, ParameterLong, ParameterDouble, ParameterDatetime, ParameterString, ParameterList, ParameterDict
   from alphalogic_api.decorators import command, run
   from alphalogic_api.logger import log


   #
   # How to send an email with Python
   # http://naelshiab.com/tutorial-send-email-python/
   #
   def send_mail(smtp, message, topic, recipients):
      host = smtp.ServerAddress.val
      port = smtp.Port.val
      user = smtp.Login.val
      password = smtp.Password.val
      timeout = smtp.TimeoutMillisec.val / 1000.0  # in seconds
      from_addr = smtp.SenderAddress.val
      to_addrs = map(methodcaller('strip'), recipients.split(','))  # 'mike@mail.com, tom@mail.com'

      msg = MIMEMultipart()
      msg['From'] = smtp.SenderName.val
      msg['To'] = recipients
      msg['Subject'] = topic

      body = message
      charset = dict(Smtp.ENCODING_CHOICES)[smtp.Encoding.val]
      msg.attach(MIMEText(body, 'plain', charset))

      server = smtplib.SMTP(host=host, port=port, timeout=timeout)
      server.starttls()
      server.login(user=user, password=password)
      text = msg.as_string()
      server.sendmail(from_addr, to_addrs, text)
      server.quit()
      return ''

   #
   # Adapter Stub.
   # Tree:
   # MailAdapter
   #     |
   #     |__Smtp
   #
   class MailAdapter(Root):

      def handle_get_available_children(self):
         return [
               (Smtp, 'Smtp'),
         ]

   class Smtp(Object):

      PORT_CHOICES = (
         (25, '25'),
         (465, '465'),
         (587, '587'),
         (2525, '2525'),
      )

      ENCODING_CHOICES = (
         (0, 'utf-8'),
         (1, 'koi8-r'),
         (2, 'windows-1251'),
         (3, 'windows-1252'),
      )

      # parameters
      ServerAddress = ParameterString(visible=Visible.setup)
      SenderAddress = ParameterString(visible=Visible.setup)
      Login = ParameterString(visible=Visible.setup)
      Password = ParameterString(visible=Visible.setup)
      SenderName = ParameterString(visible=Visible.setup)
      Port = ParameterLong(visible=Visible.setup, choices=PORT_CHOICES, default=587)
      TimeoutMillisec = ParameterLong(visible=Visible.common, default=5000)
      Encoding = ParameterLong(visible=Visible.common, choices=ENCODING_CHOICES, default=0)

      # commands
      @command(result_type=unicode)
      def SendMail(self, message='', topic='', recipients=''):
         return send_mail(self, message=message, topic=topic, recipients=recipients)


   if __name__ == '__main__':
      # main loop
      root = MailAdapter()
      root.join()


