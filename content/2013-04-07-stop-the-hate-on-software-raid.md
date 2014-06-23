---
layout: post
title: "Stop the hate on software RAID"
date: 2013-04-07 20:21
comments: true
categories: storage
---
{% img right /images/NetappClustering.jpg %}I've had a another bee in my bonnet recently. Specifically, it has been to do with hardware vs software RAID, but I think it goes deeper than that. It started a couple of months back with a discussion on [Reddit](http://redd.it/18dp63). Some of the comments were:

> Get out, get out now.

> while he still can..

>WHAT!?
>60 TB on software raid.
>Jeezus.

> Software raid? Get rid of it.

It then got re-awakened the other day when Matt Simmons (aka [The Standalone Sysadmin](http://www.standalone-sysadmin.com/blog/)) asked the following question on Twitter:

<blockquote class="twitter-tweet"><p>So what are the modern arguments for / against hardware / software RAID? I don't get out much. <a href="https://twitter.com/search/%23sysadmin">#sysadmin</a></p>&mdash; Matt Simmons (@standaloneSA) <a href="https://twitter.com/standaloneSA/status/319932013492703233">April 4, 2013</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>
<!-- more -->

At the time of writing, 2 people replied: myself and [Chris Siebenmann](http://utcc.utoronto.ca/~cks/space/blog/). Both of us basically said software RAID is better, hardware is at best pointless.

First of all, I need to define what I mean by hardware RAID. First, I do not care about what you are using for your c:\ drive in Windows, or your / partition in Linux. I am talking about the place where you store your business critical data. If you file server goes down, that is a bad day, but the business will live on. Lose your business data, then you will be out of a job (most likely alongside everyone else). Hardware RAID can thus fall into to categories:

  * a bunch of disks attached to a PCI-e card in a big server
  * an external storage array. This could be either SAN or NAS, once again I do not care in this instance.

I am firmly of the opinion that hardware RAID cards should no longer exist. They are at best pointless and at worst a liability. Modern systems are so fast that there is no real performance hit. Also management is a lot easier; if you have a hardware array then you will need to load the manufacturer's utilities in order to manage it. By manage, I mean to be told when a disk has failed. On Linux, there is no guarantee that will work. There is a couple of vendors that require packages from RHEL4 to be installed on RHEL6 systems to install their tools. Also, they are invariable closed source, will most likely taint my kernel with binary blobs and generally cause a mess on my previously clean system. By contrast, using software RAID means that I can do all the management with trivial little scripts that can easily be integrated with any monitoring system that I choose to use.

I can understand why people are skeptical of software RAID. There have been performance reasons and practical reasons for it not to be trusted. I'm not going to address the performance argument, suffice to say that RAID is now 25 years old - CPUs have moved on a lot in that time. I remember when the first Promise IDE controllers came out, that used a kind of pseudo-hardware RAID - it was not pretty. The preconceptions are compounded by the plethora of nasty controllers built in to consumer motherboards and (possibly worst of all) Window's built in RAID that was just bad.

The thing is, those days are now a long way behind us. For Linux there is absolutely no need for hardware RAID, even Windows will be just fine with an motherboard based RAID for its c: drive.

{% pullquote %}
In fact {"I would say that hardware RAID is a liability"}. You go to all that effort to safe-guard your data, but the card becomes a single-point-of-failure. It dies, then you spend your time searching Ebay for the same model of card. You buy it, then you pray that the RAID data is stored on the disks and not the controller (not always the case). By contrast, if you use software RAID and the motherboard dies, then you pull the disks and plug them into whatever box running Linux and you recover your data.
{% endpullquote %}

There is definitely a time and place for an external array. If you are using virtualisation properly, you need shared storage. The best way to do that, 9 times out of 10, is with an external array. However, even that may well not be as it seems. There are some that still develop dedicated hardware and come out with exciting gear (HP 3Par and Hitachi Data Systems spring to mind). However, the majority of storage is now on Software.

Let take a look at these things and see just how much "hardware" is actually involved.


The EMC VMAX is a big, big black box of storage. Even the "baby" 10k one scales up to 1.5PB and 4 engines. The 40k will go up to 3PB and 8 engines. Look a little deeper (one line further on the spec sheet) and you find that what those engines are: quad Xeons (dual on the 10/20k). The great big bad VMAX is a bunch of standard x86 servers running funky software to do all the management and RAID calculations.

{% pullquote %}
Like its big brother, the VNX is also a pair of Xeon servers. Even more, it runs Windows. In fact {" since the Clariion CX4 EMC has been using Windows Storage Server "} (based on XP) Move along to EMC's other lines we find Isilion is nothing more than a big pile of Supermicro servers running (IIRC) FreeBSD.
{% endpullquote %}

Netapp's famed FAS range similarly runs on commodity hardware,OnTAP is [BSD](https://en.wikipedia.org/wiki/NetApp_filer) based.

The list goes on, Dell Compellent? When I looked at it in early 2012, it was still running on Supermicro dual Xeons. The plan was to move it to Dell R-series servers as soon as possible. They were doing validation at the time, I suspect the move is complete now. Reading between the lines, I came away with the impression that it runs on FreeBSD, but I do not know for sure. CoRAID use Supermicro servers, they unusually run Plan9 as their OS. HP StoreVirtual (formerly Lefthand) runs or Proliant Gen8 servers or VMware. In all these cases, there is no extra hardware involved.

{% pullquote %}
{" The people that write the MD stack in the Linux kernel are not cowboys "}. It has proved over and over again that is both stable and fast. I have trusted some of the most important data under my care to their software:  for many years the ERP system at [Snell](http://www.snellgroup.com) has been running on MD devices quite happily. We found it much faster than the P410 cards in the DL360G5 servers that host it. Additionally, you do not need to load in any funky modules or utilities - everything you need to manage the devices is there in the distribution. 
{% endpullquote %}

ZFS also recommends to bypass any RAID devices and let it do everything in software, as does Btrfs. With *Storage Spaces* in Server 2012 Microsoft is definitely angling towards software controlled storage as well. 

As with everything in IT, hardware is falling by the wayside in storage. Modern processors can do the processing so fast that there is no performance need for hardware in between your OS and the disks any more. The OS layers (Storage Spaces on Windows and especially MD/LVM on Linux) are so mature now that their reliability can be taken as a given. With the management advantages, there really is no technical reason to stick with hardware RAID. In fact the closer you can get the raw disks to your OS the better.

{% pullquote %}
As I said at the start, the subject here is software vs hardware RAID, but my problem goes deeper than that particular argument. As technology professionals, we are technical people. We need to understand what is going on under the bonnet - that is our job! It may be fine for a vendor to pull the wool over a CFO's eyes, but {" we need to know what is inside that magic black box, especially when it is in the spec sheet"}.
{% endpullquote %}
