---
layout: post
title: "Something from the shadows"
date: 2013-02-21 16:06
comments: true
categories: storage
---
An intriguing startup came out of stealth mode a few days ago. [Pernix Data](http://pernixdata.com/) was founded by Pookan Kumar and Satyam Vaghani, both of who were pretty near top of the pile in VMware's storage team.
<!--more -->

What they are offering is, to me at least, a blinding flash of the obvious. It is a softweare layer that runs on a VMware hypervisor that uses local flash as a cache for whatevery is coming off your main storage array. {% img right http://pernixdata.com/images/home_graphic3.png 300 217 %}. That could be an SSD (or multiple) or a PCI-e card.

Reading what they have to say, it is completely transparent to the hypervisor, so everything just works. Obviously me being an Open Source fanatic I imediately started thinking how I could do this with Linux; it took me about 5 minutes.

You take your SAN array and give your LUN to your Hypervisors (running KVM obviously, and with a local SSD). Normally you would stick a clustered file system (such as GFS2) on that shared LUN. Instead you use a tiered block device on top of that LUN. There are two that come immediately to mind: [Flashcache](https://github.com/facebook/flashcache/) and [Btier](http://sourceforge.net/projects/tier/files/). 

Finally, you can put your clustered file system on that tiered device. I do not have the time or facilities to test this, but I cannot see why it would not work. Maybe someone at Red Hat (seeing as they do the bulk of KVM and GFS2 development) can run with this and see what happens.
What their plans are I do not know. It is very early days, maybe they will be a success maybe not. As they are both ex-VMware, I would not be at all surprised if they get bought back into the VMware fold. Certainly this is a functionality that I would have like to have seen in the past.
