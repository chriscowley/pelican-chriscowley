---
layout: post
title: "Dell Announces VRTX"
date: 2013-06-04 22:15
comments: true
categories: systems
---
{% img right http://en.community.dell.com/cfs-file.ashx/__key/communityserver-blogs-components-weblogfiles/00-00-00-37-45/6886.vrtx.JPG %} Dell has announced the new PowerEdge VRTX (pronounced Vertex). The name comes from a vertex being "the intersection of multiple lines", alluding to this being a mixture of a rack server, a blade server and a SAN.
<!-- more -->

It is aimed at branch offices, so it contains 4 servers, storage, networking and (unusually) the ability to add PCI-e cards (up to 8, including 3 FH/FL). These cards can be connected to which ever server you want. These features put in competition with the HP C3000 and the Supermicro OfficeBlade.

The other 2 are basically standard blade chassis that have been given quiet fans and IEC power connectors. You can pick and choose storage, PCI-E and compute blades depending on your needs. They also have the full array of networking options: anything from 2 1Gb uplinks to full on 40GB QDR infiniband. VRTX on the other hand is a fixed configuration of a 2U SAS array (either 2.5" or 3.5" disks) and 4 compute servers. You can add PCI-e cards, but support is limited. Basically, it expands the limited networking available in the blades themselves (no 10Gb at launch, max of 8x 1Gb uplink with no redundant fabric). There is support for a GPU, but it is AMD only with  no Nvidia Tesla support.

So what we have is a system that takes the same amount of space as it competitors and is less flexible. So why would you want it? In several cases I have wanted something that would give me a simple solution to run VMware (or similar) properly (i.e. shared storage and at least 2 nodes) and go in the corner of the office on a standard plug. The other solutions can do this with a bit of thought (more so with the Supermicro), but the VRTX will do that out-of-the-box.

If I could make 1 request of Dell, it would be to do a "VRTX lite" that drops the PCI-e slots and (perhaps) halves the number of disks and servers. To get a pair of computer servers and a small SAN in a 4 bay NAS sized box would be awesome for many a SMB branch office.

<iframe width="640" height="360" src="http://www.youtube.com/embed/16IlDQnIMrk?rel=0" frameborder="0" allowfullscreen></iframe>

