My Openstack clients stopped working
####################################

:slug: my-openstack-clients-stopped-working
:tags: openstack
:summary: My Openstack CLI clients stopped working, this is how I fixed them

A quicky, possibly note to self. The other day I ran ``nova list`` and instead of getting a list of the instances in my lab I got:

::

    Traceback (most recent call last):
      File "/usr/bin/nova", line 6, in <module>
        from novaclient.shell import main
      File "/usr/lib/python2.7/site-packages/novaclient/shell.py", line 33, in <module>
        from oslo.utils import strutils
      File "/usr/lib/python2.7/site-packages/oslo/utils/strutils.py", line 26, in <module>
        from oslo.utils._i18n import _
      File "/usr/lib/python2.7/site-packages/oslo/utils/_i18n.py", line 21, in <module>
        from oslo import i18n
      File "/usr/lib/python2.7/site-packages/oslo/i18n/__init__.py", line 13, in <module>
        from ._factory import *
      File "/usr/lib/python2.7/site-packages/oslo/i18n/_factory.py", line 26, in <module>
        from oslo.i18n import _message
      File "/usr/lib/python2.7/site-packages/oslo/i18n/_message.py", line 30, in <module>
        class Message(six.text_type):
      File "/usr/lib/python2.7/site-packages/oslo/i18n/_message.py", line 159, in Message
        if six.PY2:
    AttributeError: 'module' object has no attribute 'PY2'

A bit of DDGing did not reveal anyone else having this problem. A few Python developers had come accross it, but the fixes were not really relevant to me. The fix is quite simple though. Basically the Python `Six <https://pypi.python.org/pypi/six>`__ module got corrupted somehow.

I am using Fedora 22, and which uses DNF as its package manager. This depends on Six, so I had to do a reinstall of the module:

::

    sudo dnf reinstall python-six

Fixed! I have no idea what caused it to break as I do not really pay much attention on what is a fairly disposably workstation. 
