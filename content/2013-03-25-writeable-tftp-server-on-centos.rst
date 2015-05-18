Writeable TFTP Server On CentOS
###############################
:tags:   linux

Well this caught me out for an embarassingly long time. There are
`loads <https://blog.penumbra.be/tag/tftp/>`__
`of <https://www.question-defense.com/2008/11/13/linux-setup-tftp-server-on-centos>`__
`examples <https://wiki.centos.org/EdHeron/PXESetup>`__ of setting up a
TFTP server on the web. The vast majority of them assume that you are
using them read-only for PXE booting.

.. raw:: html

   <!-- more -->

I needed to make it writeable so that it could be used for storing
switch/router backups. It is trivially simple once you have read the man
page (pro tip: RTFM).

I am doing this on RHEL6, it should be fine on Centos, Scientific Linux
or Fedora as is. Any other distro it will require some modification.
First install it (install the client as well to test at the end:

::

    yum install tftp tftp-server xinetd
    chkconfig xinetd on

Now edit the file \`/etc/xinetd.d/tftp to read:

::

    service tftp
    {
        socket_type = dgram
        protocol    = udp
        wait        = yes
        user        = root
        server      = /usr/sbin/in.tftpd
        server_args = -c -s /var/lib/tftpboot
        disable     = no
        per_source  = 11
        cps         = 100 2
        flags       = IPv4
    }

There are 2 changes to this file from the defaults. The ``disable`` line
enables the service. Normally that is where you leave it. However, you
cannot upload to the server in this case without pre-creating the files.

The second change adds a ``-c`` flag to the ``server_args`` line. This
tells the service to create the files as necessary.

It still will not work though. You need to tweak the filesystem
permissions and SELinux:

::

    chmod 777 /var/lib/tftpboot
    setsebool -P tftp_anon_write 1

Of course you'll also need to open up the firewall. So add the following
line to ``/etc/sysconfig/iptables``:

::

    -A INPUT -m state --state NEW -m udp -p udp -m udp --dport 69 -j ACCEPT

If your IPtables set up is what comes out of the box, there will be a
similar line to allow SSH access (tcp:22), I would add this line just
after that one. If you have something more complicated, then you will
probably know how to add this one as well anyway.

You should now be able to upload something to the server

::

    echo "stuff" > test
    tftp localhost -c put test

Your test file should now be in ``var/lib/tftpboot``.

One final note with regards to VMware. This does not work if you are
using the VMXNET3 adapter, so make sure you are using the E1000. GETs
will work and the file will be created, but no data will be put on the
server. To annoy you even more, the test PUTting to localhost will work,
but PUTs from a remote host will not.

It has been noted in the VMware forums
`here <https://communities.vmware.com/thread/215456>`__
