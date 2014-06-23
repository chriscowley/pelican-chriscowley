---
layout: post
title: "Connect to Fedora 19 with FreeNX"
date: 2013-08-01 10:17
comments: true
categories: linux
---
{% img right http://i.imgur.com/Z8LFhPUl.png 400 250 %} FreeNX is a great remote desktop protocol. I find it more responsive than VNC and it uses less bandwidth. The biggest advantage though (in my eyes) is that it uses SSH to do the authentication. With VNC, each user has to arrange another password to connect to their VNC session.
<!-- more -->

However, FreeNX is still not really working nicely with GNOME 3. If you use KDE you are fine, but I like GNOME and many of the programs are GTK as a result. This means that they look out of place on KDE, which causes my engineer OCD super-sensory powers to go mad.

My workaround is to effectively go back to the tried and tested Gnome 2 environment, nowadays know as MATE.

Get the server installed and configured along with the MATE desktop:

```
sudo yum -y groupinstall "MATE desktop"
sudo yum -y install freenx-server
sudo /usr/libexec/nx/nxsetup --install --setup-nomachine-key
sudo chkconfig freenx-server on
```

Now open `/etc/nxserver/node.conf` and un-comment the line that sets the `COMMAND_START_GNOME` variable. You need to edit this line to read:

```
COMMAND_START_GNOME=mate-session
```

and restart the server with `sudo service freenx-server restart`

Now connect to it using the NX client and chose to use a unix-gnome desktop. Instead of firing up `gnome-session` (which will fail) it will now run `mate-session` and you are happy. 
