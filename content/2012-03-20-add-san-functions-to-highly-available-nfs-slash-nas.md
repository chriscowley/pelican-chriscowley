---
layout: post
title: "Add SAN functions to Highly Available NFS/NAS"
date: 2012-03-20 21:07
comments: true
published: true
categories: storage
---

This based on my last post where I documented building a Highly Available NFS/NAS server.

There is not a huge amount that needs to be done in order to add iSCSI functionality as well.
<!-- more -->

Add a file called _/etc/drbd/iscsi.res_ containing:

```
resource iscsi {
    on nfs1 {
        device /dev/drbd1;
        disk   /dev/vdc;
        meta-disk internal;
        address   10.0.0.1:7789;
    }
    on nfs2 {
        device /dev/drbd1;
        disk   /dev/vdc;
        meta-disk internal;
        address   10.0.0.2:7789;
    }
}
```

This differs from the previous resource in 2 ways. Obviously it using a different physical disk. Also the port number of the address is incremented; each resource has to have its own port to communicate on.

## Configure Heartbeat

Add a new resource to _/etc/ha.d/haresources_:

```
iscsi1.snellwilcox.local IPaddr::10.0.0.101/24/eth0 drbddisk::iscsi tgtd
```

Same primary host, new IP address, new drbd resource and of course the service to be controlled (tgtd in this case).

I also made a couple of changes to _/etc/ha.d/ha.cf_:

```
keepalive 500ms
deadtime 5
warntime 10
initdead 120
```

This changes the regularity of the heartbeat packets from every 2 seconds to 2 every second. We also say that a node is dead after only 5 seconds rather than after 30.

## Configure an iSCSI Target

Tgtd has a config file that you can use in _/etc/tgt/targets.conf_. It is an XML file, so add entry like:

```
<target iqn.2011-07.world.server:target0>
        # provided devicce as a iSCSI target
        backing-store /dev/vg_matthew/lv_iscsi1
        # iSCSI Initiator's IP address you allow to connect
        initiator-address 192.168.1.20
        # authentication info ( set anyone you like for "username", "password" )
</target>
```


The target name is by convention _iqn.year-month.reverse-domainname:hostname.targetname_. Each backing store will be a seperate LUN. A discussion of this is out of the scope of this article.

By default, this config file is disabled. Enable it by un-commenting the line `#TGTD_CONFIG=/etc/tgt/targets.conf` in _/etc/sysconfig/tgtd_. You can now enable the target with service tgtd reload.

Now when you run `tgtadm –mode target –op show` you should get something like:

```
Target 1: iqn.2012-03.com.example:iscsi.target1
    System information:
        Driver: iscsi
        State: ready
    I_T nexus information:
    LUN information:
        LUN: 0
            Type: controller
            SCSI ID: IET     00010000
            SCSI SN: beaf10
            Size: 0 MB, Block size: 1
            Online: Yes
            Removable media: No
            Readonly: No
            Backing store type: null
            Backing store path: None
            Backing store flags:
        LUN: 1
            Type: disk
            SCSI ID: IET     00010001
            SCSI SN: beaf11
            Size: 8590 MB, Block size: 512
            Online: Yes
            Removable media: No
            Readonly: No
            Backing store type: rdwr
            Backing store path: /dev/drbd/by-res/iscsi
            Backing store flags:
    Account information:
    ACL information:
        ALL
```

## Connect An Initiator

Install the iscsi utils:

```
yum install iscsi-initiator-utils
chkconfig iscsi on
chkconfig iscsid on
```

Discover the targets on the host and login to the target.
```
iscsiadm -m discovery -t sendtargets -p 10.0.0.101
iscsiadm -m node --login
```

If you run `cat /proc/partitions` you will see an new partition has appeared. You can do whatever you want with it.
