The Linux to Storage
####################
:tags:  storage

Martin "Storagebod" Glassborow recently wrote an interesting article
where he asked "Who'll do a Linux to Storage?". As someone who is equal
parts Storage and Linux, the same question runs around my head quite
often. Not just that, but how to do it. It is safe to say that all the
constituent parts are already in the Open Source Ecosystem. It just
needs someone to pull them all together wrap them up in an integrated
interface (be that a GUI, CLI, an API or all).

.. raw:: html

   <!--more -->

Linux, obviously, has excellent NFS support. Until recently it was a
little lacking in terms of block support. `iSCSI Enterprise
Target <https://sourceforge.net/projects/iscsitarget/>`__ is ok, but is
not packaged for RHEL, which for most shops makes it a big no-no.
Likewise `TGT <https://stgt.sourceforge.net/>`__ is not bad, I have
certainly used it to to good effect, but administering it is a bit like
pulling teeth. Additionally, neither are VMware certified and I am
pretty sure that TGT at least is missing a required feature for
certification as well (may be persistent reservations). There is a third
SCSI target in Linux though: `LIO Kernel
Target <https://www.linux-iscsi.org/>`__ by Rising Tide Systems. This is
a lot newer, but is already VMware Ready certified. Red Hat used it in
RHEL6 for FCoE target support, but not for iSCSI. in RHEL7 they will be
`using it for all block
storage <https://groveronline.com/2012/11/tgtd-lio-in-rhel-7/>`__. It
has a much nicer interface than the other targets on Linux, using a very
intuitive CLI, nice JSON config files and a rather handy API. Rising
Tide are a bit of an unknown however, or at least I thought so. It turns
our that both QNAP and Netgear use LIO Kernel Target in their larger
devices - hence the VMware certification. In any case, Red Hat are
behind it, although I think they are working on a fork of at least the
CLI, so I think success is assured there. That solves the problem of
block storage, be it iSCSI, Fibre-Channel, FCoE, Infiniband or even USB.

Another important building block in an enterprise storage system is some
way of distributing the data for both redunancy and performance. Marin
mentions `Ceph <https://ceph.com/>`__ which is an excellent system.
Personally I would put my money on
`GlusterFS <https://www.gluster.org/>`__ though. I have had slightly
better performance from it. Red Hat bought Gluster about a year ago, and
have put some serious development effort into it. As well as POSIX
access via Fuse, it has Object storage for use with OpenStack, a native
Qemu connector is coming in the next versions. Hadoop can also access it
directly. There is also a very good Puppet module for it, which gets
around one of Martin's critisms of Ceph.

Which brings me nicely to managing this theoretical system. Embedding
Puppet in this sort of solution would also make sense. There will be
need to a way of keep config sync'ed on all the nodes (I mentioned that
this disruptive product will be scale-out didn't I? NO? OK, it will be -
prediction for the day). Puppet does this already very well, so why
re-invent the wheel.

All this can sit on top of Btrfs allowing each node to have up to 16
exabytes of local storage. For now I am not convinced by it, at least on
RHEL 6 as I have seen numerous kernel panics, nor did I have a huge
amount of joy on Fedora 17, but there is no doubt that it will get
there. Alternatively, there is always the combination of XFS and LVM.
XFS is getting on a bit now, but it has been revived by Red Hat in
recent years and it is a proven performer with plenty of life left in it
yet.

After all that, who do I think is ripe to do some serious disrupting in
the storage market? Who will "Do a Red Hat" as Martin puts it? Simple:
it will be Red Hat! Look at the best of breed tools at every level of
the storage stack on Linux and you will find it is either from Red Hat
(Gluster) or they are heavily involved (LIO target). They have the
resources and the market/mind share to do it. Also they have a long
history of working with and feeding back to the community, so the
fortuitous circle will continue.
