Home-made Redundant Thin-provisioned SAN
########################################
:tags:  storage

The inspiration for this came from a mixture of problems I was having
with my HP P2000, ideas that have been floating around my head for a
while, plus a post over at Bauer-power.net. Basically I got given a
bunch of warranty returned Supermicro servers from our Customer Service
guys and got tasked with making it our secondary VMware store and DR
snapshot storage. Incidentally, the Supermicro servers are used for our
Channel-in-a-box product for those you in the broadcast world. They are
not ideal, the 2U 12 disk models that Pablo uses are far more suitable.

Plenty of companies already build their arrays on commodity hardware
like these, so I am not doing anything new:

-  Dell Compellent (Supermicro, soon to be Dell)
-  CoRAID (Supermicro)
-  EMC Clarion and VNX
-  HP P4000 (HP DL180)
-  3Par
-  Pure Storage
-  Nutanix
-  Solid Fire

My set up is basically the same as that used by Pablo in the second
iteration of his array:

-  Linux
-  GlusterFS
-  Tgtd
-  Heartbeat

There are a couple of differences:

-  Mine uses a new version of GlusterFS which is currently in beta. This
   has several new features, the one I am interested in is Granular
   Locking. As I am storing VM images, I do not want these being locked
   during a self-heal – a problem in 3.2 and before. There are also
   other things such as object-storage (Amazon S3 compatible) for use
   with Open Stack. I’d love that, but I am not using it in my
   environment :( .
-  I am building on top of CentOS. I started with Red Hat and will
   continue to use it for server environments in the forceeable future.
-  I do not have de-duplication as I am not using ZFS, I am running on
   top of Ext4 and will use XFS or BTRFS if I need to. I am only using
   8x 1TB drives as that is what I got given for free.

I have had to build a couple of custom RPMS which I have made available
in my Yum repository.

I did investigate de-duplication using LessFS, but sadly that is a no go
as it does not currently support Extended Attributes, which are required
by GlusterFS.

Installation
------------

Install a basic CentOS 6 system on each node – the base system will be
fine.

The two servers are

-  server1 192.168.1.1(eth0),10.0.0.1(eth1)
-  server2 192.168.1.2(eth0),10.0.0.2(eth1)

They connect to the rest of your network using eth0 and eth1 is a
dedicated link between the 2. I would put them via a seperate
switches/vLANs rather than a direct link, that way you can scale out
your pool easily.

In the hosts file add:

::

    10.0.0.1 server1.example.com
    10.0.0.2 server2.example.com

Add my repository:

::

    rpm --import https://yum.chriscowley.me.uk/RPM-GPG-KEY-ChrisCowley
    yum install https://yum.chriscowley.me.uk/el/6/x86_64/RPMS/chriscowley-release-1-1.noarch.rpm
    rpm --import https://fedoraproject.org/static/0608B895.txt
    yum install https://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-5.noarch.rpm 

Now you can install the necessary packages, which is not many. :

::

    yum install glusterfs-core glusterfs-fuse heartbeat scsi-target-utils

Now you can add create a pool of servers:

GlusterFS
---------

From server1:

::

    gluster peer probe server2

You next step is to configure a Gluster Volume. Gluster’s documentation
for this is excellent. For our simple 2-node cluster we just want a
simple replicated volume. As you grow, you can simple add extra pairs of
nodes to expand your storage pool.

On each node create a folder to store the data and a mount-point for the
replicated data:

::

    mkdir /exp1
    mkdir /mnt/test-volume

Now create your volume and activate it(on a single node):

::

    gluster volume create test-volume replica 2 transport tcp server1:/exp1 server2:/exp1
    gluster volume start test-volume

Now you need to mount that volume on each of your nodes.

::

    echo "`hostname`:/test-volume /mnt/test-volume glusterfs defaults,noauto,_netdev 0 0" >> /etc/fstab
    echo "mount /mnt/test-volume" >> /etc/rc.local
    mount /mnt/test-volume

Heartbeat
---------

Now you need to configure heartbeat to control a floating IP address and
the associated TGTD service. You need to create a few files on each
node.

/etc/ha.d/authkeys:

::

    auth 2
    2 crc

/etc/ha.d/ha.cf

::

    logfacility     local0
    keepalive 500ms
    deadtime 5
    warntime 10
    initdead 120
    bcast eth1
    node server1
    node server2
    auto_failback no

/etc/ha.d/haresources:

::

    server1 IPaddr::192.168.1.3/24/eth0 tgtd

There are a couple of considerations. The Gluster filesystems need to be
mounted before tgtd starts. Tgtd is in turn controled by Heartbeat (see
the above haresources file). To this end make sure both heartbeat and
tgtd are disabled and start heartbeat from /etc/rc.local.

::

    echo "/etc/init.d/heartbeat start" >> /etc/rc.local

With all this done on both nodes, you can now start heartbeat on each
node:

::

    /etc/init.d/heartbeat start

Checking ifconfig will show that one of your nodes now has an *eth0:0*
address.You will also find that tgtd is also running on that same node.

iSCSI Target
------------

First create yourself a file to use as the backend for your iSCSI
target:

::

    dd if=/dev/zero bs=1M count=40000 of=/mnt/test-volume/test.img

or, if you prefer thin provisioned:

::

    dd if=/dev/zero bs=1M seek=40000 count=0 of=/mnt/test-volume/test.img

You now need to define this file as a target. This requires the editting
of 2 files.

/etc/sysconfig/tgtd:

::

    TGTD_CONFIG=/etc/tgt/targets.conf

/etc/tgtd/targets.conf, make sure there is an entry such as:

::

    <target iqn.2012-02.com.example.gluster:isci>
        backing-store /mnt/test-volume/test.img
        initiator-address 192.168.1.10
    </target>

This will make that image file you created available to the client with
the address 192.168.1.10. This targets.conf file is extremely well
commented, so have a read. Now just tell tgtd to reload its
configuration from the live node:

::

    /etc/init.d/tgtd reload

Conclusion
----------

Nothing here is particularly complicated, but it does give you a lot of
storage for a very low price, using a very enterprise friendly OS.
