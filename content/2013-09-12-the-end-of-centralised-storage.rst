The End of Centralised Storage
##############################
:tags:  storage

{% img right /images/NetappClustering.jpg %}That is a pretty drastic
title, especially given that I spend a significant part of my day job
working with EMC storage arrays. The other day I replied to a tweet by
`Scott Lowe <https://blog.scottlowe.org>`__ :

.. raw:: html

   <blockquote class="twitter-tweet"><p>

@scott\_lowe with things like Gluster and Ceph what does shared storage
actually give apart from complications?

.. raw:: html

   </p>

— Chris Cowley (@chriscowleyunix) September 11, 2013

.. raw:: html

   </blockquote>
   <script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>
   <!-- more -->

Due to time-zone differences between France and the USA I missed out on
most of the heated conversation that ensued. From what I could see it
quickly got out of hand, with people replying to so many others that
they barely had any space to say anything. I am sure it has spawned a
load of blog posts, as Twitter is eminently unsuitable for that sort of
conversation (at least I have seen one by
`StorageZilla <https://storagezilla.typepad.com/storagezilla/2013/09/tomorrows-das-yesterday.html>`__.

The boundary between DAS (Direct Attached Storage) and remote storage
(be that a SAN or NAS) is blurring. Traditionally a SAN/NAS array is a
proprietary box that gives you bits of disk space that is available to
whatever server (or servers) that you want. Conversely, DAS is attached
either inside the server or to the back of it. Sharing between multiple
servers is possible, but not very slick - no switched fabric, no
software configuration, cables have to be physically moved.

Now everything is blurring. In the FLOSS world there is the like of Ceph
and GlusterFS, which take your DAS (or whatever) and turn that into a
shared pool of storage. You can put this on dedicated boxes, depending
on your workload that may well be the best idea. However you are not
forced to. To my mind this is a more elegant solution. I have a
collection of identical servers, I use some for compute, other for
storage, others for both. You can pick and choose, even doing it live.

The thing is, even the array vendors are now using DAS. An EMC VNX is
commodity hardware, as is the VMAX (mostly, I believe there is an ASIC
used in the encryption engine), Isilion, NetApp, Dell Compellent, HP
StoreVirtual (formerly Lefthand). What is the difference in the way they
attach their disks? Technically none I suppose, it is just hidden away.

Back to the cloud providers, when you provision a VM there is a process
that happens (I am considering Openstack, as that is my area of
interest/expertise). You provision an instance and it takes the template
you select and copies it to the local storage on that host. Yes you can
short-circuit that and use shared storage, but that is unnecessarily
complex and introduces a potential failure point. OK, the disk in the
host could fail, but then so would the host and it would just go to a
new host.

With Openstack, you can use either Ceph or GlusterFS for your block
storage (amongst others). When you create block storage for your
instance it is created in that pool and replicated. Again, these will in
most cases be distributing and replicating local storage. I have known
people use SAN arrays as the back-end for Ceph, but that was because
they already had them lying around.

There have been various products around for a while to share out your
local storage on VMware hosts. VMware's own VSA, HP StoreVirtual and now
Virtual SAN takes this even deeper, giving tiering and tying directly
into the host rather than using a VSA. It certainly seems that DAS is
the way forward (or a hybrid approach such as PernixData FVP). This
makes a huge amount of sense, especially in the brave new world of SSDs.
The latencies involved in spinning rust effective masked those of the
storage fabric. Now though SSDs are so fast, that the time it takes for
a storage object to transverse the SAN becomes a factor. Getting at
least the performance storage layer as physically close to the computer
layer as possible is now a serious consideration.

Hadoop, the darling of the Big Data lovers, uses HDFS, which also
distributes and replicates your data across local storage. GlusterFS can
also be used too. You can use EMC arrays, but I do not hear much about
that (other than from EMC themselves). The vast majority of Hadoop users
seem to be on local storage/HDFS. On a similar note Lustre, very popular
in the HPC world, is also designed around local storage.

{% pullquote %} So what am I getting at here? To be honest I am not
sure, but I can see a general move away from centralised storage. Even
EMC noticed this ages ago - they were talking about running the
hypervisor on the VNX/VMAX. At least that is how I remember it anyway, I
may well be wrong (if I am, then it is written on the internet now, so
it must be true). Red Hat own GlusterFS and are pushing it centre stage
for Openstack, Ceph is also an excellent solution and has the weight of
Mark Shuttleworth and Canonical behind it. VMware have been pushing
Virtual SAN hard and it seems to have got a lot of people really
excited. {" I just do not see anything really exciting in centralised
storage"}, everything interesting is based around DAS. {% endpullquote
%}
