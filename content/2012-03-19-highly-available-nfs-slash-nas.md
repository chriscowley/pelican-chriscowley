title: "Highly Available NFS/NAS"
date: 2012-03-19 16:59
comments: true
published: true
Take 2 Centos Servers (nfs1 and nfs2 will do nicely) and install ELrepo and EPEL on them both:
<!-- more -->

{% codeblock %}
yum install \
    https://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-5.noarch.rpm \
    https://elrepo.org/elrepo-release-6-4.el6.elrepo.noarch.rpm --nogpgcheck
{% endcodeblock %}

Each of them should ideally have 2 NICS, with the secondary ones just used for DRBD sync purposes. We’ll give these the address 10.0.0.1/32 and 10.0.0.2/32.

I am also assuming that you have disabled the firewall and SELinux – I do not recommend that for production, but for testing it is fine.
## DRBD Configuration

Install DRBD 8.4 on the both:
{% codeblock %}
yum install drbd84-utils kmod-drbd84
{% endcodeblock %}

On each node the file /etc/drbd.d/global_common.conf should contain:

{% codeblock %}
global {
  usage-count yes;
}
common {
  net {
    protocol C;
  }
}
{% endcodeblock %}

and /etc/drbd.d/main.res should contain:

{% codeblock %}
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
{% endcodeblock %}

On both nodes you will need to create the resource metadata:
{% codeblock %}
drbdadm create-md main
{% endcodeblock %}
and start the daemons
{% codeblock %}
service drbd start
chkconfig drbd on
{% endcodeblock %}
Now `service drbd status` will give you:

{% codeblock %}
drbd driver loaded OK; device status:
version: 8.4.1 (api:1/proto:86-100)
GIT-hash: 91b4c048c1a0e06777b5f65d312b38d47abaea80 build by dag@Build64R6, 2011-12-21 06:08:50
m:res   cs         ro                   ds                         p  mounted  fstype
0:main  Connected  Secondary/Secondary  Inconsistent/Inconsistent  C
{% endcodeblock %}
Both devices or secondary and inconsistent, this is normal at this stage. Choose a node to be your primary and run:
{% codeblock %}
drbdadm primary --force main
{% endcodeblock %}
And it start sync’ing, which will take a long time. You can temporarily make it faster with (on one node:
{% codeblock %}
drbdadm disk-options --resync-rate=110M main
{% endcodeblock %}
Put it back again with drbdadm adjust main

On your primary node you can now create a fiiesystem. I’m using ext4 for no good reason other than it being the default. Use whatever you are most comfortable with.
{% codeblock %}
mkfs.ext4 /dev/drbd0
{% endcodeblock %}

##Configure NFS

If you diid a minimal Centos install, then you willl need to install the nfs-utils package (yum install nfs-utils). Prepare your mount points and exports on both servers:
{% codeblock %}
mkdir /drbd
echo "/drbd/main *(rw)" >> /etc/exports
{% endcodeblock %}
Now we do the actual NFS set up. We previously choose nfs1 as our master when you used it to trigger the initial sync. On nfs1 mount the replicated volumes, move the NFS data to it, then create symlinks to our replicated data.
{% codeblock %}
mount /dev/drbd0 /drbd
mkdir /drbd/main
mv /var/lib/nfs/ /drbd/
ln -s /drbd/nfs/ /var/lib/nfs
umount /drbd
{% endcodeblock %}
If you get errors about not bring able to remove directories in /var/lib/nfs do not worry.

Now a little preparation on nfs2:
{% codeblock %}
mv /var/lib/nfs /var/lib/nfs.bak
ln -s /drbd/nfs/ /var/lib/nfs
{% endcodeblock %}
This will create a broken symbolic link, but it will be fixed when everything fails over.

## Heartbeat Configuration

Heartbeat is in the EPEL repository, so enable that and install it on both nodes:
{% codeblock %}
yum -y install heartbeat
{% endcodeblock %}
Make sure that _/etc/ha.d/ha.cf_ contains:
{% codeblock %}
keepalive 2
deadtime 30
bcast eth0
node nfs1 nfs2
{% endcodeblock %}
The values in node should be whatever `uname -n` returns.

Now create _/etc/ha.d/haresources_:
{% codeblock %}
nfs1 IPaddr::10.0.0.100/24/eth0 drbddisk::main Filesystem::/dev/drbd0::/drbd::ext4 nfslock nfs
{% endcodeblock %}
That is a little cryptic, so I’ll explain; nfs1 is the primary node, IPaddr sets up a floating address on eth0 that our clients will connect to. This has a resource drbddisk::main bound to it, which sets our main to resource to primary on nfs1. Filesystem mounts /dev/drbd0 at /drbd on nfs1. Finally the the services nfslock and nfs are started on nfs1.

Finally, it needs an authentication file in /etc/ha.d/authkeys, which should be chmod’ed to 600 to be only readable by root.
{% codeblock %}
auth 3
3 md5 mypassword123
{% endcodeblock %}
You should also make sure that nfslock and nfs do not start up by themselves:
{% codeblock %}
chkconfig nfs off
chkconfig nfslock off
{% endcodeblock %}
Now you can start heartbeat and check it is working:
{% codeblock %}
service heartbeat start
chkconfig heartbeat on
{% endcodeblock %}

##Testing

Running `ifconfig` on nfs1 should give you something like:
{% codeblock %}
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
{% endcodeblock %}

Note an entry for _eth0:0_ has miraculously appeared.

Also `df` should include the entry:
{% codeblock %}
/dev/drbd0             20G  172M   19G   1% /drbd
{% endcodeblock %}
Reboot nfs1 and the services should appear on nfs2.

Connect an NFS client to you floating address (10.0.0.100) and you should be able to kill the live node and it will carry on.

