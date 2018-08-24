.. alphalogic_api documentation master file, created by
   sphinx-quickstart on Mon Aug 06 17:59:42 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Alphalogic API
==============

The Alphalogic API is the official library that provides developers with the tools for creating the Alphalogic system adapters in Python 2.

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

To install the ``alphalogic_api`` package with `pip
<https://pip.pypa.io/>`_:, run this command in your terminal::

    pip install alphalogic-api

If you don't have pip installed, this `Python installation guide<http://docs.python-guide.org/en/latest/starting/installation/>`_ can guide you through the process.

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
| A simple operation a system object can perform.


Usage
-------------

Navigate to the \bin folder of the installed composite Alphalogic adapter, and open ``stub.py`` file to edit.
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
from alphalogic_api.objects import ParameterBool, ParameterLong, ParameterDouble, ParameterDatetime, ParameterString
from alphalogic_api.decorators import command, run
from alphalogic_api.logger import log
from alphalogic_api import init


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
    host, port = init()
    root = MailAdapter(host, port)
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
