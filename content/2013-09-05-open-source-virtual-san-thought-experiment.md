title: "Open Source Virtual SAN thought experiment"
date: 2013-09-05 21:19
comments: true
Okay, I know I am little slow on the uptake here, but I was on holiday at the time. The announcement of [Virtual SAN](https://www.vmware.com/products/virtual-san/) at VMWorld the last week got me thinking a bit. 
<!-- more -->

Very briefly, Virtual SAN takes locally attached storage on you hypervisors. It then turns it into a distributed object storage system which you can use to store your VMDKs. [Plenty](https://www.yellow-bricks.com/2013/09/05/how-do-you-know-where-an-object-is-located-with-virtual-san/) [of](https://www.computerweekly.com/news/2240166057/VMware-Virtual-SAN-vision-to-disrupt-storage-paradigm) [other](https://chucksblog.emc.com/chucks_blog/2013/08/considering-vsan.html) [people](https://architecting.it/2013/08/29/reflections-on-vmworld-2013/) have gone into a lot more detail. Unlike other systems that did a similar job previously this is not a Virtual Appliance, but runs on the hypervisors themselves.

The technology to do this sort of thing using purely Open Source exists. All this has added is a distributed storage layer on each hypervisor. There are plenty of these exist for Linux, with my preference probably being for GlusterFS. Something like this is what I would have in mind:

{% img center https://i.imgur.com/NHYdf78.png %}

Ceph is probably the closest to Virtual SAN, as it is fundamentally object-based. Yes there would be CPU and RAM overhead, but that also exists for Virtual SAN too. Something like DRBD/GFS2 is not really suitable here, because it will not scale-out as much. You would not have to have local storage in all your hypervisor nodes (as with Virtual SAN) too.

I honestly do not see any real problems with this.
