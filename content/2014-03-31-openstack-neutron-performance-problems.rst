Openstack Neutron Performance problems
######################################
:tags: linux

.. figure:: https://i.imgur.com/fSMzOUE.jpg
    :align: right
    :alt: openstack logo

For the last few weeks I have been consulting on a private cloud 
project for a local company. Unsurprisingly this has been based
around the typical Openstack setup.

-  Nova - KVM
-  Neutron - Openvswitch
-  Cinder - LVM
-  Glance - local files

My architecture is nothing out of the ordinary. A pair of hosts each
with 2 networks that look something like this:

.. figure:: https://docs.google.com/drawings/d/11le0qu389WptC78_08Bh92qUCLiCBXiZOhDiESSCnxo/pub?w=960&h=720
    :alt: neutron architecture

All this is configured using Red Hat RDO. I had done all this under both
Grizzly and, using RDO, it was 30 minutes to set up.

Given how common and simple the setup, imagine my surprise when it did
not work. What do I mean did not work? From the outset I was worried
about Neutron. While I am fairly up to date with SDN in theory, I am
fairly green in practise. Fortunately, while RDO does not automate it's
configuration, there is at least an `accurate
document <https://openstack.redhat.com/Neutron_with_existing_external_network>`__
in how to configure it.

Now, if I was just using small images that would probably be fine,
however this project required Windows images. As a result some problems
quickly surfaced. Each time I deployed a new Windows image, everything
would lock up:

-  no network access to VM's
-  Openvswitch going mad (800-1000% CPU)
-  SSH access via eth0 completely dead

It has to be said that I initially barked up the wrong tree, pointing
the finger at disk access (usually the problem with shared systems).
However it turned out I was wrong.

A brief Serverfault/Twitter with @martenhauville brought up a few
suggestions, one of which caught my eye:


    https://ask.openstack.org/en/question/25947/openstack-neutron-stability-problems-with-openvswitch/
    there are known Neutron configuration challenges to overcome with GRE
    and MTU settings

This is where my problem lay: the external switch had an MTU of 1500,
Openvswitch also. Finally, ``ip link`` in a VM would give you

::

    2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast master br-ex state UP mode DEFAULT qlen 1000

Everything matches, however I was using GRE tunnels, which add a header
to each frame. This was pushing them over 1500 on entry to ``br-tun``
causing massive network fragmentation, which basically destroyed
Openvswitch every time I performed a large transfer. It showed up when
deploying an image, because that is hitting the Glance API over http.

Once armed with this knowledge, the fix is trivial. Add the following to
``/etc/neutron/dhcp_agent.ini``:

::

    dnsmasq_config_file=/etc/neutron/dnsmasq-neutron.conf

Now create the file ``/etc/neutron/dnsmasq-neutron.conf`` which contains
the following:

::

    dhcp-option-force=26,1454

Now you can restart the DHCP agent and all will be well:

::

    service neutron-dhcp-agent restart

I've gone on a bit in this post, as I feel the background is important.
By far the hardest part was diagnosing the problem, without knowing what
my background was it would be much harder to narrow down your problem to
being the same as mine.
