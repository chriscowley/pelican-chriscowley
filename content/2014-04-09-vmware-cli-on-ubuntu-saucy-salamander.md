---
layout: post
title: "VMware CLI on Ubuntu Saucy Salamander"
date: 2014-04-09 10:51
comments: true
categories: ['linux', 'vmware']
---
{% img right http://www.datanalyzers.com/VMware-Data-Recovery.jpg %}The current project (as of this week) has me moving away from Openstack for a while. For the next couple of months I will be immersing myself in monitor, metrics and logging. Naturally, this being a shiney new environment, this involves a significant amount of VMware time.
<!-- more -->

I have inherited an Icinga install running on Ubuntu Server, so I will be needing to run CLI commands to create checks. Simply runnning the installer does not work, as the vmware-cli package is a mixture of 32 and 64 bit commands.

First you need to download the CLI from VMware. How to do that is an exercise for the reader, as I cannot be bothered to find the link (hint: it is not hard). Then you need to install a bunch of packages:

```
sudo apt-get install cpanminus libdata-dump-perl libsoap-lite-perl libclass-methodmaker-perl  libxml-libxml-simple-perl libssl-dev libarchive-zip-perl libuuid-perl lib32z1 lib32ncurses5 lib32bz2-1.0
```

This includes a bunch of Perl modules for munching through XML, plus some 32-bit libraries so that all the tools can work.

Finally, you can extract the tarball and install the CLI:

```
tar xvf VMware-vSphere-CLI-5.5.0-1549297.x86_64.tar.gz
cd vmware-vsphere-cli-distrib/
sudo ./vmware-install.pl
```

I have not tested it, but this will probably be the same process for Debian (at least Wheezy and Sid).
