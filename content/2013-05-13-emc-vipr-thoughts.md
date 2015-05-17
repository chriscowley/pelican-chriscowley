title: "EMC ViPR thoughts"
date: 2013-05-13 21:45
comments: true
I have been a little slow on the uptake on this one. I would like to say it is because I was carefully digesting the information, but that is not true; the reality is that I have just had 2 5 day weekends in 2 weeks :-).
<!-- more -->

The big announcement at this years EMC World is ViPR. Plenty of people with far bigger reputations than me in the industry have already made their comments:

-   [Chad Sakac](https://virtualgeek.typepad.com/virtual_geek/2013/05/storage-virtualization-platform-re-imagined.html) has really good and deep, but long.
-   [Chuck Hollis](https://chucksblog.emc.com/chucks_blog/2013/05/introducing-emc-vipr-a-breathtaking-approach-to-software-defined-storage.html) is nowhere near as technical but (as is normal for Chuck) sells it beautifully
-   [Scott Lowe](https://blog.scottlowe.org/2013/05/06/very-early-thoughts-about-emc-vipr/) has an excellent overview
-   [Kate Davies](https://h30507.www3.hp.com/t5/Around-the-Storage-Block-Blog/ViPR-or-Vapor-The-Software-Defined-Storage-saga-continues/ba-p/138013?utm_source=feedly#.UZCd_covj3w) gives HP's take on it, which I sort of agree with, but not completely. As she says, the StoreAll VSA is not really in the same market, but I think it is the closest thing HP have so comparisons will always be drawn.

ViPR is EMC's response to two major storage problems:
1.   Storage is missing some sort of abstraction layer, particularly for management (the Control Plane).
1.   There is more to storage than NFS and iSCSI. As well as NAS/SAN we now have multiple forms of object stores, plus important non-POSIX file systems such as HDFS.

Another problem I would add is that of *Openness*. For now there is not really any protocols for managing multiple arrays from different manufacturers, even at a basic level. They have been attempts in the past (SMI-S), but they have never taken off. ViPR attacks that problem as well, sort of.

In some respects I am quite excited about ViPR. The ability to completely abstract the management of my storage is potentially very powerful. For now it is not really possible to integrate storage with Configuration Management tools. ViPR gives all supported arrays a REST API, thus it would be very simple to create bindings for the scripting language of your choice. Low and behold, a Puppet module to manage all my storage arrays becomes possible. This very neatly solves problem #1.


This is where my excitement ends however. The problem is that issue of *Openness* I mentioned above. EMC has gone to great lengths to describe ViPR as open, but the fact remains that it is not. EMC have published the specifications of the REST API, they have also created a plugin interface for third-parties to add their own arrays; this is where it ends however. All development of ViPR is at the mercy of EMC, so why would other vendors support it?

A lot of the management tools in ViPR are already in Openstack Cinder, which supports a much wider range of backends than ViPR at present. In that vendors have a completely open source management layer to develop against. Why would they sell their souls to a competitor? Simple, they will not. EMC exclusive shops will find ViPR to be an excellent way integrating their storage with a DevOps style workflow. Unfortunately my experience is that the sort of organizations that buy EMC (especially the big ones like VMAX) are not really ready for DevOps yet.

Another feature that EMC has been touted is multi-protocol access to your data. Block volumes can be accessed via both iSCSI and FC protocols - nothing really clever there I'm afraid. Dot Hill has been doing that for several years with the [AssuredSAN 39x0](https://www.dothill.com/wp-content/uploads/2011/08/AssuredSAN-n-3920-3930-C-10.15.11.pdf) models (and by extension the the HP P2000 as well). That is also easy enough to do on commodity hardware using  [LIO target](https://linux-iscsi.org/wiki/Main_Page) plus a whole lot more. On the file side, it gives you not only access to your data via both CIFS and NFS, but it does add object access to that. They touted this as being very clever, but once again you can already do this using well respected, production proven open source. Glusterfs has an object translator, so that covers that super clever feature. All the data abstraction features it has are already there in in the open source world. If you want object and NAS access to the same peta-byte storage system, you have it in both Glusterfs and Ceph, both of which can easily be managed by CM tools such as Puppet.

{% pullquote %}
EMC has really pushed ViPR in the last couple of weeks, but it fails to impress me. This is a shame, because in general I like EMC's products. I don't like their marketing, but in their gear does just work. ViPR will probably do well with large EMC/NetApp shops, but it is by no means the ground-breaking product that EMC would have people believe (to be honest, I'm not sure anything ever is). It can never be the universal gateway to manage our storage, it is too tied in to EMC. {"To be a universal standard it would need to be an open (source) standard"}, which is not really part of EMC's culture (with the exception of the awesome Razor).
{% endpullquote %}
