Highly Available NFS/NAS
########################
:tags:  storage

Take 2 Centos Servers (nfs1 and nfs2 will do nicely) and install ELrepo
and EPEL on them both:

::

    yum install \
        https://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-5.noarch.rpm \
        https://elrepo.org/elrepo-release-6-4.el6.elrepo.noarch.rpm --nogpgcheck

Each of them should ideally have 2 NICS, with the secondary ones just
used for DRBD sync purposes. We’ll give these the address 10.0.0.1/32
and 10.0.0.2/32.

I am also assuming that you have disabled the firewall and SELinux – I
do not recommend that for production, but for testing it is fine. ##
DRBD Configuration

Install DRBD 8.4 on the both:

::

    yum install drbd84-utils kmod-drbd84

On each node the file /etc/drbd.d/global\_common.conf should contain:

::

    global {
      usage-count yes;
    }
    common {
      net {
        protocol C;
      }
    }

and /etc/drbd.d/main.res should contain:

::

    resource main {
      on nfs1 {
        device    /dev/drbd0;
        disk      /dev/sdb;
        address   10.0.0.1:7788;
        meta-disk internal;
      }
      on nfs2 {
        device    /dev/drbd0;
        disk      /dev/sdb;
        address   10.0.0.2:7788;
        meta-disk internal;
      }
    }

On both nodes you will need to create the resource metadata:

::

    drbdadm create-md main

and start the daemons

::

    service drbd start
    chkconfig drbd on

Now ``service drbd status`` will give you:

::

    drbd driver loaded OK; device status:
    version: 8.4.1 (api:1/proto:86-100)
    GIT-hash: 91b4c048c1a0e06777b5f65d312b38d47abaea80 build by dag@Build64R6, 2011-12-21 06:08:50
    m:res   cs         ro                   ds                         p  mounted  fstype
    0:main  Connected  Secondary/Secondary  Inconsistent/Inconsistent  C

Both devices or secondary and inconsistent, this is normal at this
stage. Choose a node to be your primary and run:

::

    drbdadm primary --force main

And it start sync’ing, which will take a long time. You can temporarily
make it faster with (on one node:

::

    drbdadm disk-options --resync-rate=110M main

Put it back again with drbdadm adjust main

On your primary node you can now create a fiiesystem. I’m using ext4 for
no good reason other than it being the default. Use whatever you are
most comfortable with.

::

    mkfs.ext4 /dev/drbd0

Configure NFS
-------------

If you diid a minimal Centos install, then you willl need to install the
nfs-utils package (yum install nfs-utils). Prepare your mount points and
exports on both servers:

::

    mkdir /drbd
    echo "/drbd/main *(rw)" >> /etc/exports

Now we do the actual NFS set up. We previously choose nfs1 as our master
when you used it to trigger the initial sync. On nfs1 mount the
replicated volumes, move the NFS data to it, then create symlinks to our
replicated data.

::

    mount /dev/drbd0 /drbd
    mkdir /drbd/main
    mv /var/lib/nfs/ /drbd/
    ln -s /drbd/nfs/ /var/lib/nfs
    umount /drbd

If you get errors about not bring able to remove directories in
/var/lib/nfs do not worry.

Now a little preparation on nfs2:

::

    mv /var/lib/nfs /var/lib/nfs.bak
    ln -s /drbd/nfs/ /var/lib/nfs

This will create a broken symbolic link, but it will be fixed when
everything fails over.

Heartbeat Configuration
-----------------------

Heartbeat is in the EPEL repository, so enable that and install it on
both nodes:

::

    yum -y install heartbeat

Make sure that */etc/ha.d/ha.cf* contains:

::

    keepalive 2
    deadtime 30
    bcast eth0
    node nfs1 nfs2

The values in node should be whatever ``uname -n`` returns.

Now create */etc/ha.d/haresources*:

::

    nfs1 IPaddr::10.0.0.100/24/eth0 drbddisk::main Filesystem::/dev/drbd0::/drbd::ext4 nfslock nfs

That is a little cryptic, so I’ll explain; nfs1 is the primary node,
IPaddr sets up a floating address on eth0 that our clients will connect
to. This has a resource drbddisk::main bound to it, which sets our main
to resource to primary on nfs1. Filesystem mounts /dev/drbd0 at /drbd on
nfs1. Finally the the services nfslock and nfs are started on nfs1.

Finally, it needs an authentication file in /etc/ha.d/authkeys, which
should be chmod’ed to 600 to be only readable by root.

::

    auth 3
    3 md5 mypassword123

You should also make sure that nfslock and nfs do not start up by
themselves:

::

    chkconfig nfs off
    chkconfig nfslock off

Now you can start heartbeat and check it is working:

::

    service heartbeat start
    chkconfig heartbeat on

Testing
-------

Running ``ifconfig`` on nfs1 should give you something like:

::

    eth0      Link encap:Ethernet  HWaddr 52:54:00:84:73:BD  
              inet addr:10.0.0.1  Bcast:10.0.0.255  Mask:255.255.255.0
              inet6 addr: fe80::5054:ff:fe84:73bd/64 Scope:Link
              UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
              RX packets:881922 errors:0 dropped:0 overruns:0 frame:0
              TX packets:1302012 errors:0 dropped:0 overruns:0 carrier:0
              collisions:0 txqueuelen:1000
              RX bytes:239440621 (228.3 MiB)  TX bytes:5791818459 (5.3 GiB)

    eth0:0    Link encap:Ethernet  HWaddr 52:54:00:84:73:BD  
              inet addr:10.0.0.100  Bcast:10.0.0.255  Mask:255.255.255.0
              UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1

    lo        Link encap:Local Loopback  
              inet addr:127.0.0.1  Mask:255.0.0.0
              inet6 addr: ::1/128 Scope:Host
              UP LOOPBACK RUNNING  MTU:16436  Metric:1
              RX packets:2 errors:0 dropped:0 overruns:0 frame:0
              TX packets:2 errors:0 dropped:0 overruns:0 carrier:0
              collisions:0 txqueuelen:0
              RX bytes:224 (224.0 b)  TX bytes:224 (224.0 b)

Note an entry for *eth0:0* has miraculously appeared.

Also ``df`` should include the entry:

::

    /dev/drbd0             20G  172M   19G   1% /drbd

Reboot nfs1 and the services should appear on nfs2.

Connect an NFS client to you floating address (10.0.0.100) and you
should be able to kill the live node and it will carry on.
